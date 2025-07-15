from nicegui import ui
from contextlib import contextmanager
from menu import menu

#contextmanager decorator defines context manager function 'frame'
@contextmanager
def frame(navtitle: str):
    """Frame that all pages will follow"""
    #set colors for the UI
    ui.colors(primary='#b1cefc', secondary="#2d2b30", accent="#450927", positive="#5CD6C2")
    #create header with title and menu
    with ui.header().classes('replace="row items-center"') as header:
        ui.markdown('# Game Price Tracker')
        menu()
        ui.markdown(f'## {navtitle}')

    #create main content area
    with ui.column().classes('no-wrap w-full'):
        yield
        
    #create footer
    with ui.footer(value=False) as footer: #value=False hides the footer for now
        ui.label('This is the footer')

