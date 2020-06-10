"""From this file all simulation will be started."""
import kivy
from kivy.app import App
from simulation.tabs import MainWindow
from simulation import run
from kivy.config import Config
import sys
sys.dont_write_bytecode = True



class BluetoothMeshSimulation(App):
    def build(self):
        """Starts all application."""
        Config.set('graphics', 'window_state', 'maximized')
        Config.set('kivy', 'exit_on_escape', 0)
        return MainWindow()

if __name__ == "__main__":
    BluetoothMeshSimulation().run()
