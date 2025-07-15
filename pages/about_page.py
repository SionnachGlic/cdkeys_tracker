from theme import frame
from nicegui import ui

def about_page():
    with frame('About'):
        ui.label('This is the About page.')