import time
import serial
import numpy as np
import yaml

from pycaw.pycaw import AudioUtilities

class VolumeController():
    def __init__(self):

        with open("config.yaml", 'r') as file:
            self.config = yaml.safe_load(file)

        self.setup_sliders()
        self.setup_serial_connection()

    def reload(self):
        try:
            with open("config.yaml", 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception:
            pass
        self.setup_sliders()

    def setup_sliders(self):
        self.slider1_program = self.config['sliders']["slider1"]
        self.slider2_program = self.config['sliders']["slider2"]
        self.slider3_program = self.config['sliders']["slider3"]
        self.slider4_program = self.config['sliders']["slider4"]

    def setup_serial_connection(self):
        self.com_port = self.config['COMPort']
        self.baud_rate = 115200

    def read_slider_values(self):
        with serial.Serial(self.com_port, self.baud_rate) as ser:
            val = str(ser.readline()).replace("b'", "").replace("\\r\\n", "").strip().split("|")
        return val


    def run(self):
        while True:
            self.reload()
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session.SimpleAudioVolume
                slider_values = self.read_slider_values()
                if session.Process and session.Process.name() in self.slider1_program:
                    vol = np.interp(slider_values[0], [0, 4095], [0, 1])
                    volume.SetMasterVolume(vol, None)
                if session.Process and session.Process.name() in self.slider2_program:
                    vol = np.interp(slider_values[1], [0, 4095], [0, 1])
                    volume.SetMasterVolume(vol, None)
                if session.Process and session.Process.name() in self.slider3_program:
                    vol = np.interp(slider_values[2], [0, 4095], [0, 1])
                    volume.SetMasterVolume(vol, None)
                if session.Process and session.Process.name() in self.slider4_program:
                    vol = np.interp(slider_values[3], [0, 4095], [0, 1])
                    volume.SetMasterVolume(vol, None)
            time.sleep(self.config['UpdateSpeed'])

if __name__ == "__main__":
    volume_controller = VolumeController()
    volume_controller.run()
