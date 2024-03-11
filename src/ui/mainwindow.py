import webview

class App():
    Hello:int
    def __init__(self, master=None):
        self.Hello = 0

    def ShowMainWindow(self):
        webview.create_window('Hello world', './assets/mainwindow.html')
        webview.start()
