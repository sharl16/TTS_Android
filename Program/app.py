import kivy
import time
import threading
import os

kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.core.window import Window
from kivy.clock import Clock

from kivy.config import Config

# Backend Imports:
from backend import index_pdf

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', 0)
Window.size = (360, 640) 

def toggle_widget_visibility(widget, state):
    rgb_values = widget.color[:3]
    if state == False:
        widget.color = (*rgb_values, 0)
    else:
        widget.color = (*rgb_values, 1)

def initial_check_frontend(welcomeWidget):
    toggle_widget_visibility(welcomeWidget, True)
    welcomeWidget.text = 'Intiliazing..'
    time.sleep(1)
    if not os.path.exists(r"PDFs"):
        welcomeWidget.text=("Δεν υπάρχουν θέματα σε αυτο το κινητό..")
    welcomeWidget.text = 'Έλεγχος για ενημερώσεις..'
    time.sleep(1)
    welcomeWidget.text = 'Η εφαρμογή τρέχει στην τελεταία έδκοση!'

def handle_indexing(folder_path, input_widget, widget, loading_widget):
    toggle_widget_visibility(loading_widget, True)
    widget.text = ''
    result = None
    word = input_widget.text
    result = index_pdf(folder_path, word)
    if result:
        widget.text = str(result)
        widget.texture_update()  
        widget.height = widget.texture_size[1] 
        toggle_widget_visibility(loading_widget, False)
    else:
        widget.text = 'Δεν βρέθηκαν αποτελέσματα με αυτή την εκφώνηση.'
        widget.texture_update()  
        widget.height = widget.texture_size[1] 
        toggle_widget_visibility(loading_widget, False)
    print(str(result))

def handle_indexing_worker(folder_path, input_widget, widget, loading_widget):
    threading.Thread(target=handle_indexing, args=(folder_path, input_widget, widget, loading_widget)).start()

def handle_indexing_worker_dynamic(subject, folder_path, input_widget, widget, loading_widget):
    threading.Thread(target=handle_indexing, args=(folder_path, input_widget, widget, loading_widget)).start()

def create_tab(self, subject):
    tab = TabbedPanelItem(text=subject)
    tab_content = FloatLayout()

    label = Label(text=f'Επιλογή εκφώνησης: ', pos=(-90, 230))

    input_widget = TextInput(
        multiline=False,
        size_hint=(None, None),
        size=(145, 30),
        pos=(173, 482)
    )

    button = Button(
        text='Έναρξη',
        size_hint=(None, None),
        size=(330, 40),
        pos=(15, 420),
        background_color=(43/255, 111/255, 195/255, 1),
        background_normal='',
        background_down=''
    )

    results_scroll = ScrollView(
        size_hint=(None, None),
        size=(300, 400),
        pos=(15, 0)
    )

    results_label = Label(
        text='',
        text_size=(300, None),
        size_hint=(None, None),
        size=(300, 400),
        pos=(15, 0),
        halign='left',
        valign='top'
    )

    loading_label = Label(
        text='Loading..',
        text_size=(300, 400),
        size_hint=(None, None),
        size=(300, 400),
        pos=(15, 0),
        halign='left',
        valign='top'
    )

    toggle_widget_visibility(loading_label, False)

    results_scroll.add_widget(results_label)

    folder_path = f"PDFs\\B\\{subject}"

    button.bind(on_press=lambda instance: handle_indexing_worker_dynamic(subject, folder_path, input_widget, results_label, loading_label))

    tab_content.add_widget(label)
    tab_content.add_widget(input_widget)
    tab_content.add_widget(button)
    tab_content.add_widget(results_scroll)
    tab_content.add_widget(loading_label)

    tab.add_widget(tab_content)
    return tab

class MainApp(FloatLayout):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        
        Window.clearcolor = (1, 1, 1, 1)  
        self.tabbed_panel = TabbedPanel(do_default_tab=False)
        subjects = ["ΑΛΓΕΒΡΑ", "ΑΡΧΑΙΑ", "ΒΙΟΛΟΓΙΑ", "ΓΕΩΜΕΤΡΙΑ", "ΓΛΩΣΣΑ", "ΙΣΤΟΡΙΑ", "ΜΑΘ_ΘΕΤ", "ΦΥΣΙΚΗ"]

        for subject in subjects:
            tab = create_tab(self, subject)
            self.tabbed_panel.add_widget(tab)

        scroll_view = ScrollView(do_scroll_x=True, size_hint=(None, None), size=(360, 580), pos=(0, 0))
        scroll_view.add_widget(self.tabbed_panel)

        self.add_widget(scroll_view)


class TTS_Android(App):
    def build(self):
        return MainApp()


TTS_Android().run()