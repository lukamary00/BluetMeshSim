"""From this file all simulation will be started."""
import kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.app import App
from simulation.tabs import MainWindow, ScreenFileChooser
from simulation import run


class MyMainApp(App):
    def build(self):
        """Starts all application."""
        self.sm = ScreenManager()
        sim_runner = MainWindow(screen_manager=self.sm, name='main')
        self.sm.add_widget(sim_runner)
        self.sm.add_widget(ScreenFileChooser(screen_manager=self.sm,
                                             simulation_runner=sim_runner,
                                             name='chooser'))
        # TODO Fix size
        Window.size = (1600, 800)
        return self.sm

    # TODO Move to screen file chooser
    def open_chooser(self):
        """Open window for file selection."""
        self.sm.transition.duration = 1
        self.sm.transition = FadeTransition()
        self.sm.current = 'chooser'


if __name__ == "__main__":
    MyMainApp().run()
