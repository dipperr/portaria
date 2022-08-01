import tkinter as tk
from tkinter import ttk

import views.views as vw
import controller.controller as ct


class ViewUpdAuthentication(tk.Toplevel):
    def __init__(self, parent, controler, *args):
        super().__init__(parent)
        self.__set_window(parent)
        self.__init_labels()
        self.__init_entrys()
        self.__init_buttons()
        self.controler = controler
        self.values = args

    def __set_window(self, parent):
        logging.debug('instanciou view authentication')
        self.title('Autenticação')
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (300 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (100 / 2))
        self.geometry(f'300x100+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(background='#ececec')

    def __init_labels(self):
        self.label_senha = tk.Label(self, text='Senha', bg='#ececec', font=('Arial', 12))
        self.label_senha.place(relx=0.21, rely=0.4, anchor='center')

    def __init_entrys(self):
        self.senha = tk.StringVar()
        self.entry_senha = ttk.Entry(self, show='*', textvariable=self.senha)
        self.entry_senha.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.4)

    def __init_buttons(self):
        self.button_login = ttk.Button(self, text='alterar', command=self.authentication)
        self.button_login.place(relx=0.5, rely=0.8, anchor='center', relwidth=0.4)

    def authentication(self):
        logging.debug('entrou no método authentication')
        try:
            autent = Authentication(self.values[0], self.senha.get())
            consulta = autent.authentication()
        except Exception as error:
            ct.MessageBox.show_error(error, parent=self)
        else:
            if consulta:
                logging.debug('senhas são iguais')
                self.controler.update(self.values[0], self.values[1], self.values[2], self.values[3], self.values[4],
                                      self.values[5])
                self.destroy()
            else:
                ct.MessageBox.show_error('Senha invalida', parent=self)
