import time
import serial
import numpy as np
import yaml

from pycaw.pycaw import AudioUtilities

class VolumeController():
    def __init__(self):
        """
        Set up the Volume Controller object
        """

        # Load config file
        with open("config.yaml", 'r') as file:
            self.config = yaml.safe_load(file)

        self.setup_sliders()
        self.setup_serial_connection()

    def reload(self):
        """
        Reloads the config file and then updates the slider programs, this is done so you can update the config file
        and have the program accept those changes without having to restart.
        :return:
        """
        try:
            with open("config.yaml", 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception:
            pass
        self.setup_sliders()

    def setup_sliders(self):
        """
        Sets up the slider programs based on the config file.
        :return:
        """

        self.slider_programs = []
        for slider in self.config['sliders']:
            self.slider_programs.append(self.config['sliders'][slider])

    def setup_serial_connection(self):
        """
        Sets up the serial communication parameters
        :return:
        """
        self.com_port = self.config['COMPort']
        self.baud_rate = self.config['Baud']

    def read_slider_values(self):
        """
        Uses a context manager to communicate with the Arduino on the give com port.
        :return:
        """
        with serial.Serial(self.com_port, self.baud_rate) as ser:
            val = str(ser.readline()).replace("b'", "").replace("\\r\\n", "").strip().split("|")
        return val


    def run(self):
        """
        Runs the process for controlling volume of your applications
        :return:
        """
        while True:
            self.reload()
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session.SimpleAudioVolume
                slider_values = self.read_slider_values()
                i = 0
                for programs in self.slider_programs:
                    if session.Process and session.Process.name() in programs:
                        vol = np.interp(slider_values[i], [0, 4095], [0, 1])
                        volume.SetMasterVolume(vol, None)
                    i += 1

            # Read update rate, tested and this speed works pretty well.
            time.sleep(0.1)

if __name__ == "__main__":
    volume_controller = VolumeController()
    volume_controller.run()
