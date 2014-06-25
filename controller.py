from threading import Thread
import rumps
import gmail
import os
import datetime
import data_collector
from log import Log


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__(type(self).__name__, menu=['On',
                                                                 None])
        rumps.debug_mode(False)

        # log is opened using the log module. It is opened using the append
        # ('a') keyword, so no information is overwritten
        self.log = Log()

        # Send info details
        self.to = "habitus.data@gmail.com"
        self.subject = "Data from " + self.log.user
        self.text = self.log.user + " " + self.log.current_date

    @rumps.clicked('On')
    def button(self, sender):
        # Create thread for data collection
        data_collector_instance = data_collector
        thread_data_collector = Thread(target=data_collector_instance.run,
                                       args=(self.log, ))

        # Create thread for sending info
        thread_send_log = Thread(target=gmail.send_email,
                                 args=(self.to,
                                       self.subject,
                                       self.text,
                                       self.log.file_name))
        if sender.title == 'On':
            sender.title = 'Off'
            thread_data_collector.start()
        else:
            sender.title = 'On'
            data_collector_instance.stop()
            thread_send_log.start()
            # thread_send_log.join()

