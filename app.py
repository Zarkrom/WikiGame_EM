import json
import tkinter as tk
from screens.main import MainScreen
from screens.ChooseLang import ChooseLang
from Game import wikiRequest, getPageTitle, getHyperLinks, pagination


class windows(tk.Tk):
    windowWidth = 800
    windowHeight = 400
    currentFrame = None
    round = 1

    page = 1
    startPage = wikiRequest()
    currentPage = startPage
    endPage = wikiRequest()
    translation = 'en'

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.centerX = int(self.screenWidth / 2 - self.windowWidth / 2)
        self.centerY = int(self.screenHeight / 2 - self.windowHeight / 2)

        # Ajout d'un titre
        self.wm_title("WikiGame")

        # Taille + position de la fenêtre de l'application
        self.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, self.centerX, self.centerY))
        self.defaultSize = self.geometry()
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Location du conteneur avec grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Changement de frame
        self.show_frame(ChooseLang)

    def HomeFrame(self):
        self.show_frame(MainScreen)

    def show_frame(self, cont):
        self.currentFrame = cont
        frame = self.currentFrame(self.container, self, self.translate)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def updateRound(self):
        self.round += 1
        self.refreshFrame()

    def refreshFrame(self):
        self.show_frame(self.currentFrame)

    def getStartPage(self):
        return getPageTitle(self.startPage)

    def getCurrentPage(self):
        return getPageTitle(self.currentPage)

    def getEndPage(self):
        return getPageTitle(self.endPage)

    def getRound(self):
        return self.round

    def getItemsList(self):
        return [(idx + 1, page.get('title')) for idx, page in enumerate(getHyperLinks(self.currentPage))]

    def getPaginateList(self):
        return pagination(self.getItemsList(), self.page, 20)

    def changePage(self, page):
        self.page = page
        self.refreshFrame()

    def switchPage(self, newPage):
        self.currentPage = newPage
        self.updateRound()
        self.refreshFrame()

    def translate(self, key):
        file = open('translate/{}.json'.format(self.translation), encoding="utf-8")
        data = json.load(file)
        file.close()
        if key in data:
            return data[key]
        return key

    def setGameTranslation(self, translation):
        self.translation = translation


if __name__ == "__main__":
    app = windows()
    app.mainloop()
