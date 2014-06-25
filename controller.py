from threading import Thread
import rumps
import gmail
import data_collector


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__(type(self).__name__, menu=['On',
                                                                 None])
        rumps.debug_mode(False)

    @rumps.clicked('On')
    def button(self, sender):
        data_collector_instance = data_collector
        thread_data_collector = Thread(target=data_collector_instance.run)
        if sender.title == 'On':
            sender.title = 'Off'
            thread_data_collector.start()
        else:
            sender.title = 'On'
            data_collector_instance.stop()
            gmail.send_email("habitus.data@gmail.com",
                             "Hello from python!",
                             "This is a email sent with python")

