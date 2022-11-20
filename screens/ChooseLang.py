import tkinter as tk

translation = ["fr", "en"]


class ChooseLang(tk.Frame):
    def __init__(self, parent, controller, translate):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        titleGame = tk.Label(self, text=translate('CHOICE_YOUR_LANGUAGE'))
        titleGame.pack(padx=10, pady=10)

        gridPagesFrame = tk.Frame(self)
        gridPagesFrame.pack(expand=True, anchor=tk.CENTER, padx=10, pady=10)

        for idx, data in enumerate(translation):
            buttons = tk.Button(gridPagesFrame, text=translate(data.upper()), command=lambda data=data: self.startGame(data))
            buttons.grid(row=(idx // 3),
                         column=(idx % 3),
                         padx=2, pady=2)

    def startGame(self, data):
        self.controller.setGameTranslation(data)
        self.controller.HomeFrame()
