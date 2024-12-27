from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window

class SpinnerWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spinner = Image(source='spinner.png', size=(100, 100))  # Set your spinner image
        self.spinner.center = self.center  # Position the image at the center
        self.add_widget(self.spinner)
        Clock.schedule_interval(self.rotate_spinner, 1 / 60)  # Update every frame

    def rotate_spinner(self, dt):
        # Rotate the spinner by 5 degrees each frame
        self.spinner.angle += 5
        if self.spinner.angle >= 360:
            self.spinner.angle = 0  # Reset angle after a full rotation

class LoadingApp(App):
    def build(self):
        return SpinnerWidget()

if __name__ == '__main__':
    LoadingApp().run()
