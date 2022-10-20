from UI import ImageCryptApp as ica

# TODO: Documentation.

class Startup(object):
    def __init__(self):
        # do initial application registration here, along with any configuration reading
        self.__db_conn_string = ""
        self.__app = ica.ImageCryptApp()

    def initialize(self):
        self.__app.mainloop()