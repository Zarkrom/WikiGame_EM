import tkinter as tk
from tkinter.font import Font
from urllib import parse
from Game import wikiRequest

historyPagesVisited = []
navigationHistory = []
lastItemNavigationHistory = True
firstItemNavigationHistory = True


class MainScreen(tk.Frame):

    def __init__(self, parent, controller, translation):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        if len(navigationHistory) == 0 : self.addHistory(controller.getCurrentPage())
        gridTitleFrame = tk.Frame(self)
        gridTitleFrame.pack(pady=10)

        buttons = [
            {"title": "START", "fn": 'getStartPage()'},
            {"title": "TARGET", "fn": 'getEndPage()'},
            {"title": "CURRENT_PAGE", "fn": 'getCurrentPage()'},
            {"title": "ROUND", "fn": 'getRound()'}
        ]

        font = Font(size=10, family="Helvetica")
        font2 = Font(size=10, family="Helvetica", weight='bold')

        for idx, items in enumerate(buttons):
            titleGame = tk.Label(gridTitleFrame, font=font, text=translation(items['title']), justify=tk.RIGHT)
            titleGame.grid(row=(idx // 1), column=(idx % 1), sticky="E")
            fn = tk.Label(gridTitleFrame, font=font2, text=eval('controller.'+items['fn']), justify=tk.LEFT)
            fn.grid(row=(idx // 1), column=2, sticky="W")

        gridPagesFrame = tk.Frame(self)
        gridPagesFrame.pack(expand=True, anchor=tk.CENTER, padx=10, pady=10)
        self.pagination = controller.getPaginateList()
        for idx, items in enumerate((self.pagination['items'])):
            number = items[0]
            name = items[1]
            buttons = tk.Button(gridPagesFrame, text='{} - {}'.format(number, name),command=lambda number=number,
                                name=name: self.clickLink(number, name),fg='#3366cc' if name not in historyPagesVisited else '#795cb2', bd=0)
            buttons.grid(row=(idx // 3),
                         column=(idx % 3),
                         padx=2, pady=2)

            def enter_in(e: tk.Event):
                f = Font(e.widget, e.widget.cget("font"))
                f.configure(underline=True)
                e.widget.configure(font=f)

            def leave_out(e):
                f = Font(e.widget, e.widget.cget("font"))
                f.configure(underline=False)
                e.widget.configure(font=f)

            buttons.bind("<Enter>", enter_in)
            buttons.bind("<Leave>", leave_out)

        gridButtonFrame = tk.Frame(self)
        gridButtonFrame.pack(side='bottom', pady=(0, 10))

        titleGame = tk.Label(self,
                             text=translation('PAGES').format(self.pagination['page'], self.pagination['maxPage']))
        titleGame.pack(padx=10, pady=10, side='bottom')

        backHistoryButton = tk.Button(gridButtonFrame, text=translation('BACK'),
                                      state=tk.DISABLED if firstItemNavigationHistory else tk.NORMAL,
                                      command=lambda: self.switchHistoryNavigation('back'), width=15, height=1)
        backHistoryButton.grid(row=1, column=1, padx=2)

        forwardHistoryButton = tk.Button(gridButtonFrame, text=translation('FORWARD'),
                                         state=tk.DISABLED if lastItemNavigationHistory else tk.NORMAL,
                                         command=lambda: self.switchHistoryNavigation('forward'), width=15, height=1)
        forwardHistoryButton.grid(row=1, column=2, padx=2)

        prevPageButton = tk.Button(gridButtonFrame, text=translation('PREVIOUS_PAGE'),
                                   state=tk.DISABLED if self.pagination['page'] == 1 else tk.NORMAL,
                                   command=self.previousPage, width=15, height=1)
        prevPageButton.grid(row=2, column=1, padx=2)

        nextPageButton = tk.Button(gridButtonFrame, text=translation('NEXT_PAGE'),
                                   state=tk.DISABLED if self.pagination['maxPage'] == self.pagination[
                                       'page'] else tk.NORMAL, command=self.nextPage, width=15, height=1)
        nextPageButton.grid(row=2, column=2, padx=2)

    def addHistory(self, newVal: str):
        global navigationHistory
        data = [x for x in navigationHistory if x["active"] == True]

        idx = navigationHistory.index(data[0]) if data else 0
        newData = navigationHistory[:idx + 1] + [
            {"name": newVal, "active": True if len(navigationHistory) == 0 else False}]
        navigationHistory.clear()
        navigationHistory = newData
        if len(navigationHistory) >= 2: self.switchHistoryNavigation('forward')

    def switchHistoryNavigation(self, type: str):
        global newVal
        global firstItemNavigationHistory
        global lastItemNavigationHistory

        t = [x for x in navigationHistory if x["active"] == True]

        if not len(t): return
        data = t[0]
        data['active'] = False

        if type == "back":
            newVal = navigationHistory.index(data) - 1
        elif type == "forward":
            newVal = navigationHistory.index(data) + 1

        if newVal < 0 or newVal > len(navigationHistory): return

        navigationHistory[newVal]['active'] = True

        if newVal == 0:
            firstItemNavigationHistory = True
        else:
            firstItemNavigationHistory = False

        if newVal + 1 >= len(navigationHistory):
            lastItemNavigationHistory = True
        else:
            lastItemNavigationHistory = False

        self.changePage(1)
        self.controller.switchPage(wikiRequest(parse.quote(navigationHistory[newVal]['name'])))

    def clickLink(self, number, name):
        if name not in historyPagesVisited:
            historyPagesVisited.append(name)
        self.switchPage(self.controller.getItemsList()[int(number) - 1][1])

    def previousPage(self):
        self.changePage(self.pagination['page'] - 1)

    def nextPage(self):
        self.changePage(self.pagination['page'] + 1)

    def changePage(self, newPage):
        if newPage > self.pagination['maxPage']: return
        if newPage < 1: return
        self.controller.changePage(newPage)

    def switchPage(self, page):
        self.addHistory(page)
        # self.controller.switchPage(wikiRequest(parse.quote(page)))
