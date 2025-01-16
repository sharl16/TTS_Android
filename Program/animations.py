from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate
from kivy.animation import Animation

class LoadingSpinner(Widget):
    def __init__(self, target_widget, **kwargs):
        super().__init__(**kwargs)
        self.target_widget = target_widget

        with self.canvas:
            # Rotation transform that will rotate the widget
            self.rotation = Rotate(origin=self.target_widget.center)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        # Update rotation origin to keep it centered
        self.rotation.origin = self.target_widget.center

    def start(self):
        # Start animation
        anim = Animation(angle=360, duration=1)
        anim.repeat = True
        anim.start(self.rotation)

def animate_spinner(widget_to_rotate):
    spinner = LoadingSpinner(target_widget=widget_to_rotate)
    spinner.start()
