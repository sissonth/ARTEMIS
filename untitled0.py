from kivy.uix.spinner import Spinner
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

#Clock.schedule_once(change_spinner,10)


class spinner_test(BoxLayout):

    def __init__(self,**kwargs):
        super(spinner_test,self).__init__(**kwargs)
        #Clock.schedule_once(self.change_spinner,10)
            
    def show_selected_value(spinner, text):
        print 'The spinner', spinner, 'have text', text
    
    def change_spinner(self):
        #self.ids.main_spinner.values=('hey','hey','hey')
        print 'change executed'


class spinner_testApp(App):
    App.title='ARTEMIS v1.0'

    
    def build(self):
        artemis=spinner_test()
        return artemis
        
            
        
        
    def on_start(self):
        #Logger.info('App: ARTEMIS ALIVE')
        pass
    def on_stop(self):
        #Logger.info('App: ARTEMIS STOPPED')
        pass
        
        
if __name__ == '__main__':
    spinner_testApp().run()
