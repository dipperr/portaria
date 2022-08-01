import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip

import views.views as vw
import controller.controller as ct
from utils import Session
from utils import VideoSurveillance


class Views:
    def __init__(self, conteiner):
        self.conteiner = conteiner

    def reg_visitor(self):
        reg_visitor = vw.ViewRegVisitor(self.conteiner)
        reg_visitor.mainloop()

    def reg_habitant(self):
        reg_habitant = vw.ViewRegHabitant(self.conteiner)
        reg_habitant.mainloop()

    def reg_enterprise(self):
        reg_enterprise = vw.ViewRegEnterprise(self.conteiner)
        reg_enterprise.mainloop()

    def reg_doorman(self):
        reg_doorman = vw.ViewRegDoorman(self.conteiner)
        reg_doorman.mainloop()

    def search_visitor(self):
        search_visitor = vw.ViewSearchVisitor(self.conteiner)
        search_visitor.mainloop()

    def search_habitant(self):
        search_habitant = vw.ViewSearchHabitant(self.conteiner)
        search_habitant.mainloop()

    def search_enterprise(self):
        search_enterprise = vw.ViewSearchEnterprise(self.conteiner)
        search_enterprise.mainloop()

    def search_doorman(self):
        search_doorman = vw.ViewSearchDoorman(self.conteiner)
        search_doorman.mainloop()


class ViewVideo:
    def __init__(self, conteiner):
        self.conteiner = conteiner

    def surveillance(self):
        surveillance = VideoSurveillance(cam=0)
        surveillance.run_video()
        setattr(self.conteiner.session, 'comunication', surveillance.comunication)
        self.monitor(surveillance)

    def monitor(self, video):
        if video.window.winfo_exists():
            self.conteiner.after(1000, lambda: self.monitor(video))
        else:
            delattr(self.conteiner.session, 'comunication')


class FrameMenu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.view = Views(container)
        self.video = ViewVideo(container)
        self.__icons()
        self.__set_menu()
        self.__flags()

    def __flags(self):
        self.list_sub_menu = []

    def __icons(self):
        self.i_menu = tk.PhotoImage(file='../icons/icons_32/icons8-menu-32.png')
        self.i_close = tk.PhotoImage(file='../icons/icons_32/icons8-close-32.png')
        self.i_cad = tk.PhotoImage(file='../icons/icons_32/icons8-add-user-male-32.png')
        self.i_user = tk.PhotoImage(file='../icons/icons_32/icons8-user-32.png')
        self.i_pesq = tk.PhotoImage(file='../icons/icons_32/icons8-find-user-male-32.png')
        self.i_config = tk.PhotoImage(file='../icons/icons_32/icons8-settings-32.png')
        self.i_key = tk.PhotoImage(file='../icons/icons_32/icons8-unlock-32.png')
        self.i_video = tk.PhotoImage(file='../icons/icons_32/icons8-video-call-32.png')
        self.i_enterprise = tk.PhotoImage(file='../icons/icons_32/icons8-organization-32.png')
        self.i_recog = tk.PhotoImage(file='../icons/icons_32/icons8-facial-recognition-32.png')
        self.i_hist = tk.PhotoImage(file='../icons/icons_32/icons8-event-accepted-tentatively-32.png')

    def __set_menu(self):
        self.b_menu = ttk.Button(self, image=self.i_menu, command=lambda: self.__sub('sub'))
        self.b_menu.grid(row=0, column=0, pady=2, padx=5)
        self.b_cad = ttk.Button(self, image=self.i_cad, command=lambda: self.__sub('reg'))
        self.b_cad.grid(row=0, column=1, pady=2, padx=5)
        self.b_pesq = ttk.Button(self, image=self.i_pesq, command=lambda: self.__sub('search'))
        self.b_pesq.grid(row=0, column=2, pady=2, padx=5)
        self.b_key = ttk.Button(self, image=self.i_key)
        self.b_key.grid(row=0, column=3, pady=2, padx=5)
        self.b_video = ttk.Button(self, image=self.i_video, command=self.video.surveillance)
        self.b_video.grid(row=0, column=4, pady=2, padx=5)
        self.b_recog = ttk.Button(self, image=self.i_recog)
        self.b_recog.grid(row=0, column=5, pady=2, padx=5)
        self.b_hist = ttk.Button(self, image=self.i_hist)
        self.b_hist.grid(row=0, column=6, pady=2, padx=5)
        self.__tooltip_menu()

    def __add_sub_menu(self):
        self.b_config = ttk.Button(self, image=self.i_config)
        self.b_config.grid(row=1, column=0, pady=2, padx=5)
        self.b_close = ttk.Button(self, image=self.i_close, command=lambda: self.container.destroy())
        self.b_close.grid(row=1, column=1, pady=2, padx=5)
        self.list_sub_menu.extend([self.b_config, self.b_close])
        self.__tooltip_sub_menu()

    def __add_menu_cad(self):
        self.b_visit = ttk.Button(self, image=self.i_user, command=self.view.reg_visitor)
        self.b_visit.grid(row=1, column=0, pady=2)
        self.b_habitant = ttk.Button(self, image=self.i_user, command=self.view.reg_habitant)
        self.b_habitant.grid(row=1, column=1, pady=2)
        self.b_doorman = ttk.Button(self, image=self.i_user, command=self.view.reg_doorman)
        self.b_doorman.grid(row=1, column=2, pady=2)
        self.b_enterprise = ttk.Button(self, image=self.i_enterprise, command=self.view.reg_enterprise)
        self.b_enterprise.grid(row=1, column=3, pady=2)
        self.list_sub_menu.extend([self.b_visit, self.b_habitant, self.b_doorman, self.b_enterprise])
        self.__tooltip_menu_crud()

    def __add_menu_search(self):
        self.b_visit = ttk.Button(self, image=self.i_user, command=self.view.search_visitor)
        self.b_visit.grid(row=1, column=0, pady=2)
        self.b_habitant = ttk.Button(self, image=self.i_user, command=self.view.search_habitant)
        self.b_habitant.grid(row=1, column=1, pady=2)
        self.b_doorman = ttk.Button(self, image=self.i_user, command=self.view.search_doorman)
        self.b_doorman.grid(row=1, column=2, pady=2)
        self.b_enterprise = ttk.Button(self, image=self.i_enterprise, command=self.view.search_enterprise)
        self.b_enterprise.grid(row=1, column=3, pady=2)
        self.list_sub_menu.extend([self.b_visit, self.b_habitant, self.b_doorman, self.b_enterprise])
        self.__tooltip_menu_crud()

    def __sub(self, flag):
        if self.list_sub_menu:
            for i in self.list_sub_menu: i.grid_remove()
            self.list_sub_menu.clear()
        else:
            if flag == 'reg':
                self.__add_menu_cad()
            elif flag == 'search':
                self.__add_menu_search()
            elif flag == 'sub':
                self.__add_sub_menu()

    def __tooltip_menu(self):
        ToolTip(self.b_cad, msg='Cadastrar', bg='white')
        ToolTip(self.b_pesq, msg='Pesquisar', bg='white')
        ToolTip(self.b_menu, msg='Menu', bg='white')
        ToolTip(self.b_key, msg='Liberar Acesso', bg='white')
        ToolTip(self.b_video, msg='Monitoramento', bg='white')
        ToolTip(self.b_recog, msg='Reconhecer', bg='white')
        ToolTip(self.b_hist, msg='Historico\nDe Acesso', bg='white')

    def __tooltip_menu_crud(self):
        ToolTip(self.b_visit, msg='Visitante', bg='white')
        ToolTip(self.b_habitant, msg='Morador', bg='white')
        ToolTip(self.b_doorman, msg='Porteiro', bg='white')
        ToolTip(self.b_enterprise, msg='Empresa', bg='white')

    def __tooltip_sub_menu(self):
        ToolTip(self.b_config, msg='Configurações', bg='white')
        ToolTip(self.b_close, msg='Encerrar', bg='white')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__set_window()
        self.__frame()
        self.__style()
        self.session = Session('00877165221')
        self.session.set_infos()
        self.resizable(False, False)

    def __set_window(self):
        self.configure(background='white')

    def __frame(self):
        self.frame = FrameMenu(self)
        self.frame.grid(row=0, column=0)

    def __tree(self):
        columns = ('Nome Visitante', 'Hora')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for i in columns:
            self.tree.heading(i, text=i.title())
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree2 = ttk.Treeview(self, columns=columns, show='headings')
        for i in columns:
            self.tree2.heading(i, text=i.title())
        self.tree2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def __style(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Arial', 12), background='white')
        self.style.configure('TButton', background='white', font=('Arial', 10), padding=1, bordercolor='#8a8a8a')
        self.style.configure('TFrame', background='white')


if __name__ == '__main__':
    app = App()
    app.mainloop()
