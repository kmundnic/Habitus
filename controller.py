from threading import Thread
import rumps
import gmail
import data_collector
from log import Log


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['On', None]
        rumps.debug_mode(False)

        # log is opened using the log module. It is opened using the append
        # ('a') keyword, so no information is overwritten
        self.log = Log()

    @rumps.clicked('On')
    def button(self, sender):
        # Create thread for data collection
        data_collector_instance = data_collector
        thread_data_collector = Thread(target=data_collector_instance.run,
                                       args=(self.log, ))

        # Create thread for sending log
        thread_send_log = Thread(target=gmail.send_email,
                                 args=("habitus.data@gmail.com",
                                       "Data from " + self.log.user,
                                       self.log.user,  # Used by ifttt.com
                                       self.log.file_name))

        if sender.title == 'On':
            sender.title = 'Off'
            thread_data_collector.start()
        else:
            sender.title = 'On'
            data_collector_instance.stop()
            self.log.close_log()
            thread_send_log.start()
