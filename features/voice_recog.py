import os
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from PySide6.QtCore import QThread, Signal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model_tagalog_vr_capstone")


class OfflineVoiceWorker(QThread):
    text_recognized = Signal(str)
    status_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.is_listening = True
        self.sample_rate = 16000
        self.q = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        """Pushes raw audio buffer into the thread-safe queue."""
        if status:
            print(f"Audio status: {status}")
        self.q.put(bytes(indata))

    def run(self):
        if not os.path.exists(MODEL_DIR):
            self.status_changed.emit("Error: Vosk model folder not found!")
            return

        try:
            model = Model(MODEL_DIR)
            rec = KaldiRecognizer(model, self.sample_rate)

            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=self.audio_callback
            ):
                self.status_changed.emit("Nakikinig... Magsalita na!")
                last_partial = ""

                while self.is_listening:
                    try:
                        data = self.q.get(timeout=0.5)
                    except queue.Empty:
                        continue

                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").strip()
                        if text:
                            self.text_recognized.emit(text)
                            return
                    else:
                        partial = json.loads(rec.PartialResult())
                        p_text = partial.get("partial", "").strip()
                        if p_text:
                            last_partial = p_text
                            self.status_changed.emit(f"Narinig: {p_text}")

                # If loop ended without full Result(), check FinalResult or last partial text
                final_res = json.loads(rec.FinalResult())
                final_text = final_res.get("text", "").strip() or last_partial
                
                if final_text:
                    self.text_recognized.emit(final_text)
                else:
                    self.status_changed.emit("Walang narinig. Subukan ulit.")

        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}")

    def stop(self):
        """Stops the audio loop cleanly."""
        self.is_listening = False