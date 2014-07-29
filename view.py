import rumps
import controller
import threading


class Habitus(rumps.App):

    def __init__(self):
        # super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        super(Habitus, self).__init__("H")
        self.menu = ['Start', 'Stop', None]

    def set_menu_status(self):
        """
        Changes an element in the menu for the user to know if the application
        is running or is stopped.
        It is called by the callback functions of the MenuItems 'Start' and
        'Stop', and checks if the application is running by checking if the
        data retrieving thread is alive.
        :return: None
        """
        if not controller.retriever.is_paused():
            try:
                del self.menu['Stopped']
            except KeyError:
                "Has never stopped yet"
            self.menu.insert_after('Stop', 'Running...')
        else:
            try:
                del self.menu['Running...']
                self.menu.insert_after('Stop', 'Stopped')
            except KeyError:
                print "Already stopped"


    @rumps.clicked('Start')
    def start_data_collection(self, sender):
        """
        Callback function for MenuItem 'Start'. self, sender are used as
        arguments to differentiate between this app (self) and the sender object
        (MenuItem).
        :param sender: MenuItem
        :return: None
        """
        if controller.retriever.is_alive():
            controller.retriever.restart()
            controller.handler.restart()
        else:
            controller.retriever.start()
            controller.handler.start()
        self.set_menu_status()

    @rumps.clicked('Stop')
    def stop_data_collection(self, sender):
        """
        Callback function for MenuItem 'Stop'. self, sender are used as
        arguments to differentiate between this app (self) and the sender object
        (MenuItem).
        :param sender: MenuItem
        :return: None
        """
        controller.retriever.pause()
        controller.handler.pause()
        self.set_menu_status()