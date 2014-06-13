import rumps
import data_collector
from threading import Thread


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__(type(self).__name__, menu=['On'])
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
            # thread_data_collector.join()


if __name__ == "__main__":
    Habitus().run()