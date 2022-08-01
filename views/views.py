from random import choice
from tkinter import Menu
import tkinter as tk
from tkinter import ttk
from random import randint
from tkinter.messagebox import askokcancel
from tkinter.messagebox import askyesno
from tkinter.messagebox import WARNING
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import showwarning
from tktooltip import ToolTip
import logging
import PIL
from PIL import ImageTk
from PIL import Image
import cv2
import numpy as np

import controller.controller as ct
from utils import VideoSurveillance
from utils import Comunication
from utils import Authentication
from utils import Session
import models.models as md
import views.view_update as vu

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class MainWindow(tk.Tk):
    logging.info('start of program')

    def __init__(self, cpf):
        super().__init__()
        self.session = Session(cpf)
        self.session.set_infos()
        print(self.session)

    def init(self):
        self.__set_window()
        self.__init_menu_bar()
        self.__init_frames()
        self.__init_tree_views()
        self.__init_scrollbars()
        self.__init_labels()
        self.__init_entrys()
        self.__init_buttons()
        self.__set_styles()
        self.itemns()
        self.mainloop()

    def __set_window(self):
        self.title('Portaria')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (500 / 2))
        center_y = int((screen_height / 2) - (300 / 2))
        self.geometry(f'800x600+{center_x}+{center_y}')
        self.minsize(width=800, height=600)
        self.configure(background='#ececec')
        self.fvideo = False

    def __init_menu_bar(self):
        self.menubar = Menu(self, bg='#ececec')
        self.config(menu=self.menubar)

        self.opcoes_menu = Menu(self.menubar, bg='#ececec', tearoff=False)
        self.cadastro_menu = Menu(self.menubar, bg='#ececec', tearoff=False)
        self.consulta_menu = Menu(self.menubar, bg='#ececec', tearoff=False)
        self.monitor_menu = Menu(self.menubar, bg='#ececec', tearoff=False)

        self.cadastro_menu.add_command(label='Cadastrar Visitante', command=self.open_window_reg_visitor)
        self.cadastro_menu.add_command(label='Cadastrar Morador', command=self.open_window_reg_habitant)
        self.cadastro_menu.add_command(label='Cadastrar Porteiro', command=self.open_window_reg_doorman)
        self.cadastro_menu.add_command(label='Cadastrar Empresa', command=self.open_window_reg_enterprise)
        self.consulta_menu.add_command(label='Consultar Visitante', command=self.open_window_search_visitor)
        self.consulta_menu.add_command(label='Consultar Morador', command=self.open_window_search_habitant)
        self.consulta_menu.add_command(label='Consultar Porteiro', command=self.open_window_search_doorman)
        self.consulta_menu.add_command(label='Consultar Empresa', command=self.open_window_search_enterprise)
        self.monitor_menu.add_command(label='Iniciar Monitoramento', command=self.init_video_surveillance)
        self.opcoes_menu.add_command(label='Sair', command=self.destroy)

        self.menubar.add_cascade(label='Opções', menu=self.opcoes_menu, underline=0)
        self.menubar.add_cascade(label='Cadastro', menu=self.cadastro_menu, underline=0)
        self.menubar.add_cascade(label='Consulta', menu=self.consulta_menu, underline=0)
        self.menubar.add_cascade(label='Monitoramento', menu=self.monitor_menu, underline=0)

    def __init_labels(self):
        self.lb_cpf = ttk.Label(self, text='Cpf')
        self.lb_cpf.place(x=10, y=10)

    def __init_entrys(self):
        self.entry_cpf = ttk.Entry(self)
        self.entry_cpf.place(x=10, y=35, relwidth=0.3)

    def __init_buttons(self):
        self.button_pesquisar = ttk.Button(self, text='Pesquisar')
        self.button_pesquisar.place(relx=0.35, y=31)
        self.button_capturar = ttk.Button(self, text='Capturar', command=self.get_image)
        self.button_capturar.place(relx=0.85, y=31)

    def __init_frames(self):
        self.frame_1 = ttk.Frame(self)
        self.frame_1.place(relx=0.02, rely=0.13, relwidth=0.96, relheight=0.38)

        self.frame_2 = ttk.Frame(self)
        self.frame_2.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.43)

    def __init_tree_views(self):
        self.tree_entrada = ttk.Treeview(self.frame_2, columns=('nome', 'hora_entrada'), show='headings')
        self.tree_entrada.heading('nome', text='Nome Visitante')
        self.tree_entrada.column('nome', width=100)
        self.tree_entrada.heading('hora_entrada', text='entrada')
        self.tree_entrada.column('hora_entrada', anchor='center', width=30)
        self.tree_entrada.place(relx=0, rely=0, relwidth=0.48, relheight=1)

        self.tree_saida = ttk.Treeview(self.frame_2, columns=('nome', 'hora_saida'), show='headings')
        self.tree_saida.heading('nome', text='Nome Visitante')
        self.tree_saida.column('nome', width=100)
        self.tree_saida.heading('hora_saida', text='saída')
        self.tree_saida.column('hora_saida', anchor='center', width=30)
        self.tree_saida.place(relx=0.50, rely=0, relwidth=0.48, relheight=1)

    def __init_scrollbars(self):
        self.scrollbar_frame_1 = ttk.Scrollbar(self.frame_2, orient=tk.VERTICAL, command=self.tree_entrada.yview)
        self.tree_entrada.configure(yscrollcommand=self.scrollbar_frame_1.set)
        self.scrollbar_frame_1.place(relx=0.48, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_frame_2 = ttk.Scrollbar(self.frame_2, orient=tk.VERTICAL, command=self.tree_saida.yview)
        self.tree_saida.configure(yscrollcommand=self.scrollbar_frame_2.set)
        self.scrollbar_frame_2.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)

    def __set_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Arial', 13), background='#ececec')
        self.style.configure('TFrame', background='#ececec')
        self.style.configure('TButton', font=('Arial', 10), background='#d9d9d9', padding=2)
        self.style.configure('Treeview')

    def itemns(self):
        p_nomes = ['ana', 'maria', 'juliana', 'helena', 'madalena', 'carlos', 'francisco',
                   'joão', 'afonso', 'bruna', 'camila']
        s_nomes = ['barros', 'braz', 'bonfim', 'caldas', 'carvalho', 'chavier']

        itemns_1 = [(f'{choice(p_nomes)} {choice(s_nomes)}', f'{randint(1, 24)}:{randint(0, 60)}') for _ in
                    range(20)]
        itemns_2 = [(f'{choice(p_nomes)} {choice(s_nomes)}', f'{randint(1, 24)}:{randint(0, 60)}') for _ in
                    range(20)]
        for item1 in itemns_1:
            self.tree_entrada.insert('', tk.END, values=item1)

        for item2 in itemns_2:
            self.tree_saida.insert('', tk.END, values=item2)

    def open_window_reg_habitant(self):
        logging.info('Instanciou view register habitant')
        view = ViewRegHabitant(self)
        view.grab_set()
        controller = ct.ControllerHabitant(view)
        view.set_control(controller)

    def open_window_reg_visitor(self):
        logging.info('Instanciou view register visitor')
        view = ViewRegVisitor(self)
        view.grab_set()
        controler = ct.ControllerVisitor(view)
        view.set_control(controler)

    def open_window_reg_doorman(self):
        logging.info('Instanciou view register doorman')

        view = ViewRegDoorman(self)
        view.grab_set()

        controler = ct.ControllerDoorman(view)
        view.set_control(controler)

    def open_window_reg_enterprise(self):
        logging.info('Instanciou view register enterprise')
        view = ViewRegEnterprise(self)
        view.grab_set()
        controler = ct.ControllerEnterprise(view)
        view.set_control(controler)

    def open_window_search_visitor(self):
        logging.info('Instanciou view search visitor')
        view = ViewSearchVisitor(self)
        view.grab_set()

        controller = ct.ControllerVisitor(view)
        view.set_control(controller)

    def open_window_search_habitant(self):
        logging.info('Instanciou view search habitant')
        view = ViewSearchHabitant(self)
        view.grab_set()
        controller = ct.ControllerHabitant(view)
        view.set_control(controller)

    def open_window_search_doorman(self):
        logging.info('Instanciou view search habitant')
        view = ViewSearchDoorman(self)
        view.grab_set()

        controller = ct.ControllerDoorman(view)
        view.set_control(controller)

    def open_window_search_enterprise(self):
        logging.info('Instanciou view search Enterprise')
        view = ViewSearchEnterprise(self)
        view.grab_set()
        controller = ct.ControllerEnterprise(view)
        view.set_control(controller)

    def init_video_surveillance(self):
        self.comunication = Comunication()
        video = VideoSurveillance(cam=0)
        video.run_video()
        self.fvideo = True
        self.monitor(video)

    def get_image(self):
        if self.fvideo:
            self.img = self.comunication.get()
            if self.img is not None:
                try:
                    img_pill = PIL.Image.fromarray(np.uint8(self.img))
                except ValueError as error:
                    print(error)
                else:
                    img_pill.show()

    def monitor(self, video):
        if video.window.winfo_exists():
            self.after(1000, lambda: self.monitor(video))
        else:
            self.fvideo = False


# Views Search
class ViewSearchPerson(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set_base(parent)

    def __set_base(self, parent):
        self.__set_window(parent)
        self.__set_frames()

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (850 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (500 / 2))
        self.geometry(f'850x400+{center_x}+{center_y}')
        self.minsize(width=850, height=400)
        self.maxsize(width=1100, height=700)
        self.configure(background='white')
        self.controller = None
        self.session = Session()

    def __set_frames(self):
        self.frame = ttk.Frame(self)
        self.frame.place(x=0, rely=0.15, relwidth=1, relheight=0.85)


class ViewSearchDoorman(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set()

    def __set(self):
        self.title('Consultar Porteiro')
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.__set_entrys()
        self.__set_tree_views()
        self.__set_vars()
        self.__set_option_menu()
        self.controller = ct.ControllerDoorman(self)
        print(self.session)

    def __set_entrys(self):
        self.entry_nome = PlaceHolderEntry(self, "Nome")
        self.entry_nome.place(relx=0.01, rely=0.02, relwidth=0.4)

    def __set_buttons(self):
        self.bpesquisar = ttk.Button(self, image=self.isearch, command=self.pesquisar)
        self.bpesquisar.place(relx=0.43, rely=0.01)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_tree)
        self.blimpar.place(relx=0.48, rely=0.01)
        self.bapagar = ttk.Button(self, image=self.itrash, command=self.delete)
        if self.session.apagar:
            self.bapagar.place(relx=0.53, rely=0.01)
            self.bapagar.state(['disabled'])
        self.beditar = ttk.Button(self, image=self.iedit, command=self.editar)
        if self.session.editar:
            self.beditar.place(relx=0.58, rely=0.01)
            self.beditar.state(['disabled'])

    def __set_icons(self):
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-erase-24.png')
        self.itrash = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')
        self.iedit = tk.PhotoImage(file='../icons/icons_24/icons8-edit-24.png')

    def __set_tooltip(self):
        ToolTip(self.bpesquisar, msg='Pesquisar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bapagar, msg='Apagar', bg='white')
        ToolTip(self.beditar, msg='Editar', bg='white')

    def __set_tree_views(self):
        columns = ('uuid', 'nome', 'cpf', 'telefone', 'sexo', 'email', 'adicionar', 'editar', 'apagar', 'adm')
        display = ('nome', 'cpf', 'telefone', 'sexo', 'email', 'adicionar', 'editar', 'apagar', 'adm')
        params = (200, 180, 100, 100, 200, 100, 100, 100, 80)
        self.tree = TreView(self.frame, columns, display, 'headings')
        self.tree.set_tree_views(params, False)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(relx=0, rely=0, relwidth=0.98, relheight=0.96)
        self.__set_scrollbar()

    def __set_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_h = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.04)

    def __set_vars(self):
        self.select_search = tk.StringVar()

    def __set_option_menu(self):
        opcoes = ('Todos',)
        self.option_menu = ttk.OptionMenu(self, self.select_search, '', *opcoes, command=self.search_changed)
        self.option_menu.place(relx=0.8, rely=0.01)

    def search_changed(self, *args):
        if self.select_search.get() == 'Todos':
            self.search_all()

    def pesquisar(self):
        self.clear_tree()
        self.controller.search(
            self.entry_nome.get_value()
        )

    def search_all(self):
        self.controller.search_all()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?',
            icon=WARNING,
            parent=self
        )
        if answer:
            if self.doorman.adm == 'sim' and  not self.session.adm:
                showerror('Erro', 'Você não pode apagar\na conta do administrador', parent=self)
            else:
                self.controller.delete(self.doorman.uuid_id)
                showinfo(
                    title='Info',
                    message='Registro Apagado',
                    parent=self
                )

    def editar(self):
        if self.doorman.adm == 'sim' and not self.session.adm:
            showerror('Erro', 'Você não pode editar\na conta do administrador', parent=self)
        else:
            view = ViewUpdDoorman(self, self.doorman.uuid_id)
            controller = ct.ControllerUpdDoorman(view)
            view.set_controller(controller)
            view.grab_set()
            view.insert_infos()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.bapagar.state(['disabled'])
        self.beditar.state(['disabled'])

    def item_select(self, event):
        if self.tree.selection():
            self.bapagar.state(['!disabled'])
            self.beditar.state(['!disabled'])
            values = self.tree.item(self.tree.selection()[0], 'values')
            uuid, nome, cpf, telefone, sexo, email, adicionar, editar, apagar, adm = values
            self.doorman = TypeDoorman(uuid, nome, cpf, telefone, sexo, email, adicionar, editar, apagar, adm)


class ViewSearchEnterprise(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set()

    def __set(self):
        self.title('Consultar Empresa')
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.__set_entrys()
        self.__set_tree_views()
        self.__set_vars()
        self.__set_option_menu()
        self.controller = ct.ControllerEnterprise(self)
        self.list_values = None

    def __set_entrys(self):
        self.entry_nome = PlaceHolderEntry(self, "Nome")
        self.entry_nome.place(relx=0.01, rely=0.02, relwidth=0.4)

    def __set_buttons(self):
        self.bpesquisar = ttk.Button(self, image=self.isearch, command=self.pesquisar)
        self.bpesquisar.place(relx=0.43, rely=0.01)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_tree)
        self.blimpar.place(relx=0.48, rely=0.01)
        self.bvisualizar = ttk.Button(self, image=self.ibinoculus, command=self.viewinfo)
        self.bvisualizar.place(relx=0.65, rely=0.01)
        self.bvisualizar.state(['disabled'])
        self.bapagar = ttk.Button(self, image=self.itrash, command=self.delete)
        self.beditar = ttk.Button(self, image=self.iedit, command=self.editar)
        if self.session.apagar:
            self.bapagar.place(relx=0.53, rely=0.01)
            self.bapagar.state(['disabled'])
        if self.session.editar:
            self.beditar.place(relx=0.58, rely=0.01)
            self.beditar.state(['disabled'])

    def __set_icons(self):
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-erase-24.png')
        self.itrash = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')
        self.iedit = tk.PhotoImage(file='../icons/icons_24/icons8-edit-24.png')
        self.ibinoculus = tk.PhotoImage(file='../icons/icons_24/icons8-binoculars-24.png')

    def __set_tooltip(self):
        ToolTip(self.bpesquisar, msg='Pesquisar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bvisualizar, msg='Visualizar', bg='white')
        ToolTip(self.bapagar, msg='Apagar', bg='white')
        ToolTip(self.beditar, msg='Editar', bg='white')

    def __set_tree_views(self):
        columns = ('uuid', 'nome', 'cnpj', 'telefone', 'veiculo', 'rua', 'numero', 'bairro', 'cidade', 'cep')
        display = ('nome', 'cnpj', 'telefone', 'rua', 'numero', 'bairro', 'cidade', 'cep')
        params = (200, 150, 100, 200, 70, 150, 150, 130)
        self.tree = TreView(self.frame, columns, display, 'headings')
        self.tree.set_tree_views(params, False)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(relx=0, rely=0, relwidth=0.98, relheight=0.96)
        self.__set_scrollbar()

    def __set_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_h = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.04)

    def __set_vars(self):
        self.select_search = tk.StringVar()

    def __set_option_menu(self):
        opcoes = ('Todos', 'Com Veiculo')
        self.option_menu = ttk.OptionMenu(self, self.select_search, '', *opcoes, command=self.search_changed)
        self.option_menu.place(relx=0.8, rely=0.01)

    def search_changed(self, *args):
        if self.select_search.get() == 'Todos':
            self.search_all()
        elif self.select_search.get() == 'Com Veiculo':
            self.search_enterprise_veiculo()

    def pesquisar(self):
        self.clear_tree()
        self.controller.search(self.entry_nome.get_value())

    def search_all(self):
        self.clear_tree()
        self.controller.search_all()

    def search_enterprise_veiculo(self):
        self.clear_tree()
        self.controller.search_enterprise_veiculo()

    def viewinfo(self):
        if self.enterprise.fveiculo:
            viewveiculo = ViewWindowVeiculo(self, self.enterprise.nome)
            controller = ct.ControllerEnterprise(viewveiculo)
            controller.search_veiculo(self.enterprise.uuid_id)

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?\n{}'.format(self.enterprise.nome),
            icon=WARNING, parent=self
        )
        if answer:
            self.controller.delete(self.enterprise.uuid_id)
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def editar(self):
        view = ViewUpdEnterprise(self, self.enterprise)
        view.grab_set()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.bapagar.state(['disabled'])
        self.beditar.state(['disabled'])
        self.bvisualizar.state(['disabled'])

    def item_select(self, event):
        if self.tree.selection():
            self.bvisualizar.state(['disabled'])
            self.bapagar.state(['!disabled'])
            self.beditar.state(['!disabled'])
            uuid_id, nome, cnpj, tel, fveic, rua, num, bairro, cit, cep = self.tree.item(
                self.tree.selection()[0], 'values')
            self.enterprise = TypeEnterprise(uuid_id, nome, cnpj, tel, int(fveic), rua, num, bairro, cit, cep)
            if self.enterprise.fveiculo:
                self.bvisualizar.state(['!disabled'])


class ViewSearchHabitant(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set()

    def __set(self):
        self.title('Consultar Morador')
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.__set_entrys()
        self.__set_tree_views()
        self.__set_vars()
        self.__set_option_menu()
        self.controller = ct.ControllerHabitant(self)

    def __set_entrys(self):
        self.entry_nome = PlaceHolderEntry(self, "Nome")
        self.entry_nome.place(relx=0.01, rely=0.02, relwidth=0.4)

    def __set_buttons(self):
        self.bpesquisar = ttk.Button(self, image=self.isearch, command=self.pesquisar)
        self.bpesquisar.place(relx=0.43, rely=0.01)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_tree)
        self.blimpar.place(relx=0.48, rely=0.01)
        self.bvisualizar = ttk.Button(self, image=self.ibinoculus, command=self.viewinfo)
        self.bvisualizar.place(relx=0.65, rely=0.01)
        self.bvisualizar.state(['disabled'])
        self.bapagar = ttk.Button(self, image=self.itrash, command=self.delete)
        self.beditar = ttk.Button(self, image=self.iedit, command=self.editar)
        if self.session.apagar:
            self.bapagar.place(relx=0.53, rely=0.01)
            self.bapagar.state(['disabled'])
        if self.session.editar:
            self.beditar.place(relx=0.58, rely=0.01)
            self.beditar.state(['disabled'])

    def __set_icons(self):
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-erase-24.png')
        self.itrash = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')
        self.iedit = tk.PhotoImage(file='../icons/icons_24/icons8-edit-24.png')
        self.ibinoculus = tk.PhotoImage(file='../icons/icons_24/icons8-binoculars-24.png')

    def __set_tooltip(self):
        ToolTip(self.bpesquisar, msg='Pesquisar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bvisualizar, msg='Visualizar', bg='white')
        ToolTip(self.bapagar, msg='Apagar', bg='white')
        ToolTip(self.beditar, msg='Editar', bg='white')

    def __set_tree_views(self):
        columns = ('uuid', 'nome', 'cpf', 'telefone', 'residencia', 'fveiculo')
        display = ('nome', 'cpf', 'telefone', 'residencia')
        params = (270, 190, 180, 170)
        self.tree = TreView(self.frame, columns, display, 'headings')
        self.tree.set_tree_views(params, True)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(relx=0, rely=0, relwidth=0.98, relheight=0.96)
        self.__set_scrollbar()

    def __set_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_h = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.04)

    def __set_vars(self):
        self.select_search = tk.StringVar()

    def __set_option_menu(self):
        opcoes = ('Todos', 'Com Veiculo')
        self.option_menu = ttk.OptionMenu(self, self.select_search, '', *opcoes, command=self.search_changed)
        self.option_menu.place(relx=0.8, rely=0.01)

    def pesquisar(self):
        self.clear_tree()
        if self.controller:
            self.controller.search(
                self.entry_nome.get_value()
            )

    def search_all(self):
        if self.controller:
            self.clear_tree()
            self.controller.search_all()

    def search_pessoa_veiculo(self):
        if self.controller:
            self.clear_tree()
            self.controller.search_pessoa_veiculo()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?\n{}'.format(self.habitant.nome),
            icon=WARNING, parent=self
        )
        if answer:
            self.controller.delete(self.habitant.uuid_id)
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def viewinfo(self):
        if self.habitant.fveiculo:
            viewveiculo = ViewWindowVeiculo(self, self.habitant.nome)
            controller = ct.ControllerHabitant(viewveiculo)
            controller.search_veiculo(self.habitant.uuid_id)

    def editar(self):
        view = ViewUpdHabitant(self, self.habitant)
        view.grab_set()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.bapagar.state(['disabled'])
        self.beditar.state(['disabled'])
        self.bvisualizar.state(['disabled'])

    def search_changed(self, *args):
        if self.select_search.get() == 'Todos':
            self.search_all()
        elif self.select_search.get() == 'Com Veiculo':
            self.search_pessoa_veiculo()

    def item_select(self, event):
        if self.tree.selection():
            self.bvisualizar.state(['disabled'])
            self.bapagar.state(['!disabled'])
            self.beditar.state(['!disabled'])
            uuid_id, nome, cpf, telefone, residencia, fveiculo = self.tree.item(self.tree.selection()[0], 'values')
            self.habitant = TypeHabitante(uuid_id, nome, cpf, telefone, residencia, int(fveiculo))
            if self.habitant.fveiculo:
                self.bvisualizar.state(['!disabled'])


class ViewSearchVisitor(ViewSearchPerson):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set()

    def __set(self):
        self.title('Consultar Visitantes')
        self.__set_vars()
        self.__set_option_menu()
        self.__set_entrys()
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.__set_tree_views()
        self.controller = ct.ControllerVisitor(self)

    def __set_entrys(self):
        self.entry_nome = PlaceHolderEntry(self, "Nome")
        self.entry_nome.place(relx=0.01, rely=0.02, relwidth=0.4)

    def __set_buttons(self):
        self.bpesquisar = ttk.Button(self, image=self.isearch, command=self.pesquisar)
        self.bpesquisar.place(relx=0.43, rely=0.01)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_tree)
        self.blimpar.place(relx=0.48, rely=0.01)
        self.bvisualizar = ttk.Button(self, image=self.ibinoculus, command=self.viewinfo)
        self.bvisualizar.place(relx=0.65, rely=0.01)
        self.bvisualizar.state(['disabled'])
        self.bapagar = ttk.Button(self, image=self.itrash, command=self.delete)
        if self.session.apagar:
            self.bapagar.place(relx=0.53, rely=0.01)
            self.bapagar.state(['disabled'])
        self.beditar = ttk.Button(self, image=self.iedit, command=self.editar)
        if self.session.editar:
            self.beditar.place(relx=0.58, rely=0.01)
            self.beditar.state(['disabled'])

    def __set_icons(self):
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-erase-24.png')
        self.itrash = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')
        self.iedit = tk.PhotoImage(file='../icons/icons_24/icons8-edit-24.png')
        self.ibinoculus = tk.PhotoImage(file='../icons/icons_24/icons8-binoculars-24.png')

    def __set_tooltip(self):
        ToolTip(self.bpesquisar, msg='Pesquisar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bvisualizar, msg='Visualizar', bg='white')
        ToolTip(self.bapagar, msg='Apagar', bg='white')
        ToolTip(self.beditar, msg='Editar', bg='white')

    def __set_tree_views(self):
        columns = ('uuid', 'nome', 'cpf', 'telefone', 'sexo', 'flag_veiculo', 'flag_empresa')
        display = ('nome', 'cpf', 'telefone', 'sexo')
        params = (270, 190, 180, 170)
        self.tree = TreView(self.frame, columns, display, 'headings')
        self.tree.set_tree_views(params, True)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(relx=0, rely=0, relwidth=0.98, relheight=0.96)
        self.__set_scrollbar()

    def __set_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_h = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.04)

    def __set_vars(self):
        self.select_search = tk.StringVar()

    def __set_option_menu(self):
        opcoes = ('Todos', 'Com Empresa', 'Com Veiculo', 'Empresa e Veiculo')
        self.option_menu = ttk.OptionMenu(self, self.select_search, '', *opcoes, command=self.search_changed)
        self.option_menu.place(relx=0.8, rely=0.01)

    def viewinfo(self):
        if self.visitor.fveiculo and self.visitor.fempresa:
            view = ViewWindowInfos(self, self.visitor.nome, self.visitor.uuid_id)
        elif self.visitor.fempresa:
            viewenterprise = ViewWindowEnterprise(self, self.visitor.nome)
            controller = ct.ControllerVisitor(viewenterprise)
            controller.search_enterprise(self.visitor.uuid_id)
        elif self.visitor.fveiculo:
            viewveiculo = ViewWindowVeiculo(self, self.visitor.nome)
            controller = ct.ControllerVisitor(viewveiculo)
            controller.search_veiculo(self.visitor.uuid_id)

    def pesquisar(self):
        self.clear_tree()
        if self.entry_nome.get_value():
            print(self.entry_nome.get_value())
            self.controller.search(self.entry_nome.get_value())

    def search_changed(self, *args):
        if self.select_search.get() == 'Todos':
            self.search_all()
        elif self.select_search.get() == 'Com Empresa':
            self.search_pessoa_work()
        elif self.select_search.get() == 'Empresa e Veiculo':
            self.search_with_ent_veic()
        else:
            self.search_pessoa_veiculo()

    def search_all(self):
        self.clear_tree()
        self.controller.search_all()

    def search_with_ent_veic(self):
        self.clear_tree()
        self.controller.search_with_ent_veic()

    def search_pessoa_work(self):
        self.clear_tree()
        self.controller.search_pessoa_work()

    def search_pessoa_veiculo(self):
        self.clear_tree()
        self.controller.search_pessoa_veiculo()

    def delete(self):
        answer = askokcancel(
            title='confirmação',
            message='Deseja Apagar?\n{}'.format(self.visitor.nome),
            icon=WARNING, parent=self
        )
        if answer:
            self.controller.delete(self.visitor.uuid_id)
            showinfo(
                title='Info',
                message='Registro Apagado',
                parent=self
            )

    def editar(self):
        view = ViewUpdVisitor(self, self.visitor)
        view.grab_set()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.bapagar.state(['disabled'])
        self.beditar.state(['disabled'])
        self.bvisualizar.state(['disabled'])

    def item_select(self, event):
        if self.tree.selection():
            self.bvisualizar.state(['disabled'])
            self.bapagar.state(['!disabled'])
            self.beditar.state(['!disabled'])
            uuid_id, nome, cpf, telefone, sexo, fveiculo, fempresa = self.tree.item(self.tree.selection()[0], 'values')
            self.visitor = TypeVisitor(uuid_id, nome, cpf, telefone, sexo, int(fveiculo), int(fempresa))
            if self.visitor.fempresa or self.visitor.fveiculo:
                self.bvisualizar.state(['!disabled'])


# View Registration
class ViewRegDoorman(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set_window(parent)
        self.session = Session()
        self.__create_notebook()
        self.__set_icons()
        self.__create_buttons()
        self.__set_tooltip()
        self.base = ViewDoormanBase(self.frame1)
        self.controller = ct.ControllerDoorman(self)
        self.__check_button_adm()

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (270 / 2))
        self.geometry(f'750x270+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Cadastrar Porteiro')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Porteiro')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def __create_buttons(self):
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        if self.session.adicionar:
            self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.save_button)
            self.bsalvar.place(relx=0.1, rely=0.8)

    def __set_icons(self):
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')

    def __set_tooltip(self):
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')

    def __check_button_adm(self):
        if not self.session.adm:
            self.base.check_adm.configure(state='disabled')

    def limpar_tela(self):
        self.base.limpar_tela()

    def set_control(self, controller):
        self.controller = controller

    def save_button(self):
        self.controller.save(
            self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.sexo.get(),
            self.base.email.get(), self.base.senha.get(), self.base.adicionar.get(), self.base.apagar.get(),
            self.base.editar.get(), self.base.adm.get()
        )


class ViewRegEnterprise(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set_window(parent)
        self.session = Session()
        self.__create_notebook()
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.base = ViewEnterpriseBase(self.frame1)
        self.veiculo_flag = False
        self.controller = ct.ControllerEnterprise(self)

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (300 / 2))
        self.geometry(f'750x280+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Cadastrar Empresa')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Empresa')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def __set_buttons(self):
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8,)
        self.bsearch = ttk.Button(self.frame1, image=self.isearch, command=self.search_cep)
        self.bsearch.place(relx=0.86, rely=0.46)
        if self.session.adicionar:
            self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.save_button)
            self.bsalvar.place(relx=0.1, rely=0.8)
            self.badd_veiculo = ttk.Button(self.frame1, image=self.icar, command=self.add_veiculo)
            self.badd_veiculo.place(relx=0.93, rely=0.8)

    def __set_icons(self):
        self.icar = tk.PhotoImage(file='../icons/icons_32/icons8-car-32.png')
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')

    def __set_tooltip(self):
        ToolTip(self.badd_veiculo, msg='Cadastrar\nVeiculo', bg='white')
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bsearch, msg='Pesquisar CEP', bg='white')

    def __add_settings(self):
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.place(relx=0, rely=0.35, relwidth=1)

    def limpar_tela(self):
        self.base.limpar_tela()

    def add_veiculo(self):
        self.veiculo = ViewFrameVeiculo(self.notebook, 800, 280, self)
        self.veiculo.pack(fill='both', expand=True)
        self.notebook.add(self.veiculo, text='Veiculo')
        self.notebook.select(self.veiculo)
        self.badd_veiculo.state(['disabled'])
        self.veiculo_flag = True

    def save_button(self):
        if self.veiculo_flag and self.veiculo.list_veiculos:
            self.controller.save(
                self.base.cnpj.get(), self.base.nome.get(), self.base.telefone.get(), self.base.address.rua.get(),
                self.base.address.numero.get(), self.base.address.bairro.get(), self.base.address.cidade.get(),
                self.base.address.cep.get(), self.veiculo.list_veiculos
            )
        else:
            self.controller.save(
                self.base.cnpj.get(), self.base.nome.get(), self.base.telefone.get(), self.base.address.rua.get(),
                self.base.address.numero.get(), self.base.address.bairro.get(), self.base.address.cidade.get(),
                self.base.address.cep.get()
            )

    def search_cep(self):
        self.base.address.search_cep(None)


class ViewRegHabitant(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__set_window(parent)
        self.session = Session()
        self.__create_notebook()
        self.__set_icons()
        self.__create_buttons()
        self.__set_tooltip()
        self.base = ViewHabitantBase(self.frame1)
        self.veiculo_flag = False
        self.controller = ct.ControllerHabitant(self)

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (270 / 2))
        self.geometry(f'750x270+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Cadastrar Morador')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Morador')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def __create_buttons(self):
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        if self.session.adicionar:
            self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.save_button)
            self.bsalvar.place(relx=0.1, rely=0.8)
            self.badd_veiculo = ttk.Button(self.frame1, image=self.icar, command=self.add_veiculo)
            self.badd_veiculo.place(relx=0.93, rely=0.8)

    def __set_icons(self):
        self.icar = tk.PhotoImage(file='../icons/icons_32/icons8-car-32.png')
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')

    def __set_tooltip(self):
        ToolTip(self.badd_veiculo, msg='Cadastrar\nVeiculo', bg='white')
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')

    def limpar_tela(self):
        self.base.limpar_tela()

    def add_veiculo(self):
        self.veiculo = ViewFrameVeiculo(self.notebook, 800, 280, self)
        self.veiculo.pack(fill='both', expand=True)
        self.notebook.add(self.veiculo, text='Veiculo')
        self.notebook.select(self.veiculo)
        self.badd_veiculo.state(['disabled'])
        self.veiculo_flag = True

    def save_button(self):
        if self.veiculo_flag and self.veiculo.list_veiculos:
            self.controller.save(
                self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.residencia.get(),
                list_veiculos=self.veiculo.list_veiculos
            )
        else:
            self.controller.save(
                self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.residencia.get()
            )


class ViewRegVisitor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__set_window(parent)
        self.session = Session()
        self.__create_notebook()
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.base = ViewVisitorBase(self.frame1)
        self.veiculo_flag = False
        self.controller = ct.ControllerVisitor(self)

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (270 / 2))
        self.geometry(f'750x270+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Cadastrar Visitante')

    def __set_buttons(self):
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        self.bsearch = ttk.Button(self.frame1, image=self.isearch, command=self.search_enterprise)
        self.bsearch.place(relx=0.83, rely=0.31)
        if self.session.adicionar:
            self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.save_button)
            self.bsalvar.place(relx=0.1, rely=0.8)
            self.badd_veiculo = ttk.Button(self.frame1, image=self.icar, command=self.add_veiculo)
            self.badd_veiculo.place(relx=0.93, rely=0.8)
            self.bcapturar = ttk.Button(self.frame1, image=self.icamera, command=self.get_image)
            self.bcapturar.place(relx=0.18, rely=0.8)
            if not hasattr(self.session, 'comunication'):
                self.bcapturar.state(['disabled'])

    def __set_icons(self):
        self.icar = tk.PhotoImage(file='../icons/icons_32/icons8-car-32.png')
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')
        self.icamera = tk.PhotoImage(file='../icons/icons_32/icons8-câmera-32.png')
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')

    def __set_tooltip(self):
        ToolTip(self.badd_veiculo, msg='Cadastrar\nVeiculo', bg='white')
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bcapturar, msg='Capturar Foto', bg='white')
        ToolTip(self.bsearch, msg='Procurar\nEmpresa', bg='white')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Visitante')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def search_enterprise(self):
        self.enterprise = ViewFrameEnterprise(self.notebook, 800, 280, self)
        self.enterprise.pack(fill='both', expand=True)
        self.notebook.add(self.enterprise, text='Empresa')
        controler = ct.ControllerEnterprise(self.enterprise)
        self.enterprise.set_controller(controler)
        self.notebook.select(self.enterprise)
        self.bsearch.state(['disabled'])

    def add_veiculo(self):
        self.veiculo = ViewFrameVeiculo(self.notebook, 800, 280, self)
        self.veiculo.pack(fill='both', expand=True)
        self.notebook.add(self.veiculo, text='Veiculo')
        self.notebook.select(self.veiculo)
        self.badd_veiculo.state(['disabled'])
        self.veiculo_flag = True

    def get_image(self):
        imgview = ViewImage(self, self.session.comunication)

    def save_button(self):
        if self.veiculo_flag and self.veiculo.list_veiculos:
            self.controller.save(
                self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.sexo.get(),
                self.base.uuid_empresa, list_veiculos=self.veiculo.list_veiculos
            )
        else:
            self.controller.save(
                self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.sexo.get(),
                self.base.uuid_empresa
            )

    def limpar_tela(self):
        self.base.limpar_tela()


class ViewImage(tk.Toplevel):
    def __init__(self, parent, comunication):
        super().__init__(parent)
        self.comunication = comunication
        self.image = None
        self.__image()
        self.__set_icon()
        self.__set_buttons()

    def __image(self):
        imagem = self.comunication.get()
        if imagem is not None:
            try:
                imagem_pill = PIL.Image.fromarray(np.uint8(imagem))
            except ValueError as error:
                print(error)
            else:
                width, height = imagem_pill.size
                imagem_pill = imagem_pill.resize((int(width * 1.50), int(height * 1.50)))
                self.__set_canvas(imagem_pill)

    def __set_canvas(self, imagem):
        width, height = imagem.size
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.img = ImageTk.PhotoImage(imagem)
        self.image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def __replace(self):
        self.canvas.delete(self.image)
        imagem = self.comunication.get()
        if imagem is not None:
            try:
                imagem_pill = PIL.Image.fromarray(np.uint8(imagem))
            except ValueError as error:
                print(error)
            else:
                width, height = imagem_pill.size
                imagem_pill = imagem_pill.resize((int(width * 1.50), int(height * 1.50)))
                self.img = ImageTk.PhotoImage(imagem_pill)
                self.image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def __set_buttons(self):
        self.badd = ttk.Button(self, image=self.iadd)
        self.badd.pack(side='left', padx=5, pady=5)
        self.bclose = ttk.Button(self, image=self.iclose, command=self.__exit)
        self.bclose.pack(side='left', padx=5, pady=5)
        self.breplace = ttk.Button(self, image=self.ireplace, command=self.__replace)
        self.breplace.pack(side='left', padx=5, pady=5)

    def __set_icon(self):
        self.iadd = tk.PhotoImage(file='../icons/icons_24/icons8-done-24.png')
        self.iclose = tk.PhotoImage(file='../icons/icons_24/icons8-close-24.png')
        self.ireplace = tk.PhotoImage(file='../icons/icons_24/icons8-replace-24.png')

    def __exit(self):
        self.destroy()


class ViewUpdDoorman(tk.Toplevel):
    def __init__(self, parent, uuid_id):
        super().__init__(parent)
        self.__set_window(parent, uuid_id)
        self.__create_notebook()
        self.base = ViewDoormanBase(self.frame1)
        self.__entry_senha()
        self.__check_button_adm()
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()

    def __set_window(self, parent, uuid_id):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (800 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (300 / 2))
        self.geometry(f'800x300+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Editar Porteiro')
        self.controller = None
        self.senha = None
        self.uuid_id = uuid_id
        self.session = Session()

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Porteiro')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def __set_buttons(self):
        self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.atualizar)
        self.bsalvar.place(relx=0.1, rely=0.8)
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        if self.uuid_id == self.session.uuid_id or self.session.adm:
            self.bsenha = ttk.Button(self.frame1, image=self.ikey, command=self.alterar_senha)
            self.bsenha.place(relx=0.27, rely=0.58)

    def __set_icons(self):
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')
        self.ikey = tk.PhotoImage(file='../icons/icons_24/icons8-key-2-24.png')

    def __set_tooltip(self):
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        ToolTip(self.bsenha, msg='Alterar Senha', bg='white')

    def __entry_senha(self):
        self.base.entry_senha['state'] = 'disabled'

    def __check_button_adm(self):
        if not self.session.adm:
            self.base.check_adm.configure(state='disabled')

    def alterar_senha(self):
        resposta = askyesno('Confirmação', 'Deseja alterar\nsua senha?', parent=self)
        if resposta:
            self.base.entry_senha['state'] = 'normal'

    def set_controller(self, controller):
        self.controller = controller

    def insert_infos(self):
        self.controller.insert_infos(self.uuid_id)

    def limpar_tela(self):
        self.base.limpar_tela()

    def atualizar(self):
        if self.base.senha.get():
            self.controller.update(
                self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.sexo.get(),
                self.base.email.get(), self.base.senha.get(), self.base.adicionar.get(), self.base.editar.get(),
                self.base.apagar.get(), self.base.adm.get(), self.uuid_id)
        else:
            self.controller.update(
                self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(), self.base.sexo.get(),
                self.base.email.get(), self.senha, self.base.adicionar.get(), self.base.editar.get(),
                self.base.apagar.get(), self.base.adm.get(), self.uuid_id)


class ViewUpdEnterprise(tk.Toplevel):
    def __init__(self, parent, enterprise):
        super().__init__(parent)
        self.__set_window(parent)
        self.__create_notebook()
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.base = ViewEnterpriseBase(self.frame1)
        self.enterprise = enterprise
        self.uuid_id = enterprise.uuid_id
        self.controller = ct.ControllerEnterprise(self)
        self.insert_infos()

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (270 / 2))
        self.geometry(f'750x270+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Editar Empresa')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Empresa')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def __set_buttons(self):
        self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.atualizar)
        self.bsalvar.place(relx=0.1, rely=0.8)
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        self.badd_veiculo = ttk.Button(self.frame1, image=self.icar, command=self.edit_veiculo)
        self.badd_veiculo.place(relx=0.93, rely=0.8)

    def __set_icons(self):
        self.icar = tk.PhotoImage(file='../icons/icons_32/icons8-car-32.png')
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')

    def __set_tooltip(self):
        ToolTip(self.badd_veiculo, msg='Cadastrar\nVeiculo', bg='white')
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')

    def edit_veiculo(self):
        self.veiculo = ViewUpdVeiculo(self.notebook, 800, 280, self)
        controller = ct.ControllerVeiculoEnterprise(self.veiculo)
        self.veiculo.set_controller(controller)
        self.veiculo.pack(fill='both', expand=True)
        self.notebook.add(self.veiculo, text='Veiculo')
        self.veiculo.insert_infos(self.uuid_id)
        self.notebook.select(self.veiculo)
        self.badd_veiculo.state(['disabled'])

    def insert_infos(self):
        self.base.entry_nome.insert('end', self.enterprise.nome)
        self.base.entry_cnpj.insert('end', self.enterprise.cnpj)
        self.base.entry_telefone.insert('end', self.enterprise.telefone)
        self.base.address.entry_rua.insert('end', self.enterprise.rua)
        self.base.address.entry_numero.insert('end', self.enterprise.numero)
        self.base.address.entry_bairro.insert('end', self.enterprise.bairro)
        self.base.address.entry_cidade.insert('end', self.enterprise.cidade)
        self.base.address.entry_cep.insert('end', self.enterprise.cep)

    def limpar_tela(self):
        self.base.limpar_tela()

    def atualizar(self):
        self.controller.update(
            self.base.cnpj.get(), self.base.nome.get(), self.base.telefone.get(), self.base.address.rua.get(),
            self.base.address.numero.get(), self.base.address.bairro.get(), self.base.address.cidade.get(),
            self.base.address.cep.get(), self.enterprise.uuid_id)


# Views Update
class ViewUpdHabitant(tk.Toplevel):
    def __init__(self, parent, habitant):
        super().__init__(parent)
        self.__set_window(parent)
        self.__create_notebook()
        self.base = ViewHabitantBase(self.frame1)
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.habitant = habitant
        self.uuid_id = habitant.uuid_id
        self.controller = ct.ControllerHabitant(self)
        self.insert_infos()

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (270 / 2))
        self.geometry(f'750x270+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Editar Morador')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Empresa')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def __set_buttons(self):
        self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.atualizar)
        self.bsalvar.place(relx=0.1, rely=0.8)
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        self.badd_veiculo = ttk.Button(self.frame1, image=self.icar, command=self.edit_veiculo)
        self.badd_veiculo.place(relx=0.93, rely=0.8)

    def __set_icons(self):
        self.icar = tk.PhotoImage(file='../icons/icons_32/icons8-car-32.png')
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')

    def __set_tooltip(self):
        ToolTip(self.badd_veiculo, msg='Cadastrar\nVeiculo', bg='white')
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')

    def edit_veiculo(self):
        self.veiculo = ViewUpdVeiculo(self.notebook, 800, 280, self)
        controller = ct.ControllerVeiculoHabitant(self.veiculo)
        self.veiculo.set_controller(controller)
        self.veiculo.pack(fill='both', expand=True)
        self.notebook.add(self.veiculo, text='Veiculo')
        self.veiculo.insert_infos(self.uuid_id)
        self.notebook.select(self.veiculo)
        self.badd_veiculo.state(['disabled'])

    def insert_infos(self):
        self.base.entry_nome.insert('end', self.habitant.nome)
        self.base.entry_cpf.insert('end', self.habitant.cpf)
        self.base.entry_telefone.insert('end', self.habitant.telefone)
        self.base.entry_residencia.insert('end', self.habitant.residencia)

    def limpar_tela(self):
        self.base.limpar_tela()

    def atualizar(self):
        self.controller.update(self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(),
                               self.base.residencia.get(), self.habitant.uuid_id)


class ViewUpdVisitor(tk.Toplevel):
    def __init__(self, parent, visitor):
        super().__init__(parent)
        self.__set_window(parent)
        self.__create_notebook()
        self.base = ViewVisitorBase(self.frame1)
        self.visitor = visitor
        self.uuid_id = visitor.uuid_id
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.controller = ct.ControllerVisitor(self)
        self.insert_infos()
        print(visitor.uuid_id)

    def __set_window(self, parent):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (750 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (270 / 2))
        self.geometry(f'750x270+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title('Editar Visitante')

    def __set_buttons(self):
        self.blimpar = ttk.Button(self.frame1, image=self.ieraser, command=self.limpar_tela)
        self.blimpar.place(relx=0.02, rely=0.8)
        self.bsalvar = ttk.Button(self.frame1, image=self.isave, command=self.atualizar)
        self.bsalvar.place(relx=0.1, rely=0.8)
        self.bsearch = ttk.Button(self.frame1, image=self.isearch, command=self.search_enterprise)
        self.bsearch.place(relx=0.83, rely=0.31)
        if not self.visitor.fempresa:
            self.bsearch.state(['disabled'])
        self.badd_veiculo = ttk.Button(self.frame1, image=self.icar, command=self.edit_veiculo)
        self.badd_veiculo.place(relx=0.93, rely=0.8)

    def __set_icons(self):
        self.icar = tk.PhotoImage(file='../icons/icons_32/icons8-car-32.png')
        self.ieraser = tk.PhotoImage(file='../icons/icons_32/icons8-erase-32.png')
        self.isave = tk.PhotoImage(file='../icons/icons_32/icons8-save-32.png')
        self.icamera = tk.PhotoImage(file='../icons/icons_32/icons8-câmera-32.png')
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')

    def __set_tooltip(self):
        ToolTip(self.badd_veiculo, msg='Cadastrar\nVeiculo', bg='white')
        ToolTip(self.bsalvar, msg='Salvar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')
        # ToolTip(self.bcapturar, msg='Capturar Foto', bg='white')
        ToolTip(self.bsearch, msg='Procurar\nEmpresa', bg='white')

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Visitante')

    def __create_frames(self):
        self.frame1 = ttk.Frame(self.notebook, width=800, height=280)
        self.frame1.pack(fill='both', expand=True)

    def insert_infos(self):
        self.base.enome.insert('end', self.visitor.nome)
        self.base.ecpf.insert('end', self.visitor.cpf)
        self.base.etelefone.insert('end', self.visitor.telefone)
        self.base.combox.set(self.visitor.sexo)
        if self.visitor.fempresa:
            empresa = self.controller.search_enterprise_nome(self.visitor.uuid_id)
            self.base.eempresa['state'] = 'normal'
            self.base.eempresa.insert('end', empresa[0])

    def search_enterprise(self):
        self.enterprise = ViewFrameEnterprise(self.notebook, 800, 280, self)
        self.enterprise.pack(fill='both', expand=True)
        self.notebook.add(self.enterprise, text='Empresa')
        controler = ct.ControllerEnterprise(self.enterprise)
        self.enterprise.set_controller(controler)
        self.notebook.select(self.enterprise)
        self.bsearch.state(['disabled'])

    def edit_veiculo(self):
        self.viewveiculo = ViewUpdVeiculo(self.notebook, 800, 280, self)
        controller = ct.ControllerVeiculoVisitante(self.viewveiculo)
        self.viewveiculo.set_controller(controller)
        self.viewveiculo.pack(fill='both', expand=True)
        self.notebook.add(self.viewveiculo, text='Veiculo')
        self.viewveiculo.insert_infos(self.visitor.uuid_id)
        self.notebook.select(self.viewveiculo)
        self.badd_veiculo.state(['disabled'])

    def limpar_tela(self):
        self.base.limpar_tela()

    def atualizar(self):
        self.controller.update(self.base.cpf.get(), self.base.nome.get(), self.base.telefone.get(),
                               self.base.sexo.get(), self.visitor.uuid_id, self.base.uuid_empresa)


class ViewUpdVeiculo(ttk.Frame):
    def __init__(self, container, width, height, objectt):
        super().__init__(container, width=width, height=height)
        self.objectt = objectt
        self.__init()

    def __init(self):
        self.base = ViewVeiculoBase(self)
        self.__set_icons()
        self.__set_buttons()
        self.__set_tooltip()
        self.__set_styles()
        self.__tree_view()
        self.list_veiculos = []
        self.veiculo = None
        self.controller = None

    def __tree_view(self):
        self.base.tree.bind('<Double-1>', self.item_select)

    def __set_buttons(self):
        self.badd = ttk.Button(self, image=self.iadd, command=self.add_veiculo)
        self.badd.place(relx=0.78, rely=0.02)
        self.bdeletar = ttk.Button(self, image=self.itrash, command=self.delete)
        self.bdeletar.place(relx=0.88, rely=0.02)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_entrys)
        self.blimpar.place(relx=0.83, rely=0.02)
        self.bx = ttk.Button(self, text='X', style='Veiculo.TButton', command=self.exit)
        self.bx.place(relx=0.97, rely=0.05, width=25, height=25, anchor=tk.CENTER)

    def __set_icons(self):
        self.iadd = tk.PhotoImage(file='../icons/icons_24/icons8-done-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-erase-24.png')
        self.itrash = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')
        self.ix = tk.PhotoImage(file='../icons/icons_24/icons8-close-24.png')

    def __set_tooltip(self):
        ToolTip(self.badd, msg='Adicionar', bg='white')
        ToolTip(self.bdeletar, msg='Apagar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')

    def __set_styles(self):
        self.style = ttk.Style(self)
        self.style.configure('Veiculo.TButton', background='#EC4343')

    def exit(self):
        self.objectt.badd_veiculo.state(['!disabled'])
        self.objectt.notebook.hide('current')

    def add_veiculo(self):
        if all(self.base.get_values()):
            self.veiculo = TypeVeiculo(
                self.base.emodelo.get(), self.base.etipo.get(), self.base.ecor.get(), self.base.eplaca.get()
            )
            resposta = askokcancel('Aviso', 'Deseja adicionar o veiculo:\n{}, placa: {}'.format(
                self.veiculo.modelo, self.veiculo.placa
            ), parent=self)
            if self.veiculo in self.list_veiculos:
                showerror('Erro', 'Veiculos com placas\nidenticas', parent=self)
            else:
                self.base.tree.insert(
                    '', tk.END, values=(
                        self.veiculo.modelo, self.veiculo.tipo, self.veiculo.cor, self.veiculo.placa
                    )
                )
                self.list_veiculos.append(self.veiculo)
                self.controller.save(self.veiculo.modelo, self.veiculo.tipo, self.veiculo.cor, self.veiculo.placa,
                                     self.objectt.uuid_id)

    def delete(self):
        if self.veiculo is not None:
            resposta = askokcancel('Aviso', 'Deseja apagar o veiculo:\n{}, placa: {}'.format(
                self.veiculo.modelo, self.veiculo.placa
            ), parent=self)
            if resposta:
                self.remove_tree()
                self.remove_list_veiculos()
                self.controller.delete(self.veiculo.placa)
                self.veiculo = None

    def clear_entrys(self):
        self.base.clear_entrys()

    def remove_tree(self):
        self.base.tree.delete(self.base.tree.selection()[0])
        self.clear_entrys()

    def remove_list_veiculos(self):
        for i in self.list_veiculos:
            if i == self.veiculo:
                self.list_veiculos.remove(i)

    def item_select(self, event):
        if self.base.tree.selection():
            modelo, tipo, cor, placa = self.base.tree.item(self.base.tree.selection()[0], 'values')
            self.veiculo = TypeVeiculo(modelo, tipo, cor, placa)

    def insert_infos(self, uuid_id):
        self.controller.search(uuid_id)

    def set_controller(self, controller):
        self.controller = controller


# Classes Genericas
class TreView(ttk.Treeview):
    def __init__(self, parent, columns, display, show):
        super().__init__(parent, columns=columns, displaycolumns=display, show=show)
        self.parent = parent
        self.columns = display

    def set_tree_views(self, params, stretch):
        for i, j in zip(self.columns, params):
            self.heading(i, text=i.title())
            self.column(i, width=j, stretch=stretch)


class TypeVeiculo:
    def __init__(self, modelo, tipo, cor, placa):
        self.modelo = modelo
        self.tipo = tipo
        self.cor = cor
        self.placa = placa

    def __eq__(self, other):
        if isinstance(other, TypeVeiculo):
            return self.placa == other.placa


class TypeDoorman:
    def __init__(self, uuid_id=None, nome=None, cpf=None, telefone=None, sexo=None, email=None,
                 adicionar=None, editar=None, apagar=None, adm=None):
        self.uuid_id = uuid_id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.sexo = sexo
        self.email = email
        self.adicionar = adicionar
        self.editar = editar
        self.apagar = apagar
        self.adm = adm

    def __repr__(self):
        return "uuid: {} nome: {} cpf: {} telefone: {} sexo: {} adm: {}".format(
            self.uuid_id, self.nome, self.cpf, self.telefone, self.sexo, self.adm
        )


class TypeVisitor:
    def __init__(self, uuid_id=None, nome=None, cpf=None, telefone=None, sexo=None, fveiculo=None, fempresa=None):
        self.uuid_id = uuid_id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.sexo = sexo
        self.fveiculo = fveiculo
        self.fempresa = fempresa

    def __repr__(self):
        return "uuid: {} nome: {} fveiculo: {} fempresa: {}".format(
            self.uuid_id, self.nome, self.fveiculo, self.fempresa
        )


class TypeHabitante:
    def __init__(self, uuid_id=None, nome=None, cpf=None, telefone=None, residencia=None, fveiculo=None):
        self.uuid_id = uuid_id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.residencia = residencia
        self.fveiculo = fveiculo

    def __repr__(self):
        return "uuid: {} nome: {} cpf: {} telefone: {} residencia: {}".format(
            self.uuid_id, self.nome, self.cpf, self.telefone, self.residencia
        )


class TypeEnterprise:
    def __init__(self, uuid_id=None, nome=None, cnpj=None, telefone=None, fveiculo=None, rua=None, numero=None,
                 bairro=None, cidade=None, cep=None):
        self.uuid_id = uuid_id
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.fveiculo = fveiculo
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    def __repr__(self):
        return "{} {} {}".format(self.uuid_id, self.nome, self.cnpj)


class ViewWindowInfos(tk.Toplevel):
    def __init__(self, parent, nome, uuid_id):
        super().__init__(parent)
        self.__set_window(parent, nome, uuid_id)
        self.__create_notebook()

    def __set_window(self, parent, nome, uuid_id):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (500 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (200 / 2))
        self.geometry(f'700x200+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title(f'Veiculos e Empresa {nome}')
        self.uuid_id = uuid_id

    def __create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)
        self.__create_frames()
        self.notebook.add(self.frame1, text='Veiculo')
        self.notebook.add(self.frame2, text='Empresa')

    def __create_frames(self):
        self.__frame_veiculo()
        self.__frame_enterprise()

    def __frame_veiculo(self):
        self.frame1 = FrameVeiculo(self.notebook, width=700, height=180)
        self.controller = ct.ControllerVisitor(self.frame1)
        self.frame1.pack(fill='both', expand=True)
        self.controller.search_veiculo(self.uuid_id)

    def __frame_enterprise(self):
        self.frame2 = FrameEnterprise(self.notebook, width=700, height=180)
        self.controller = ct.ControllerVisitor(self.frame2)
        self.frame1.pack(fill='both', expand=True)
        self.controller.search_enterprise(self.uuid_id)


class FrameVeiculo(ttk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height)
        self.__set_tree_view()

    def __set_tree_view(self):
        columns = ('modelo', 'tipo', 'cor', 'placa')
        params = (150, 100, 100, 100)
        self.tree = TreView(self, columns, columns, 'headings')
        self.tree.set_tree_views(params, True)
        self.tree.place(relx=0, rely=0, relwidth=0.97, relheight=1)
        self.__set_scrollbar()

    def __set_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)


class FrameEnterprise(ttk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height)
        self.__set_tree_view()

    def __set_tree_view(self):
        columns = ('nome', 'cnpj', 'telefone', 'rua', 'numero', 'bairro', 'cidade')
        params = (200, 150, 130, 250, 80, 150, 150)
        self.tree = TreView(self, columns, columns, 'headings')
        self.tree.set_tree_views(params, False)
        self.tree.place(relx=0, rely=0, relwidth=0.98, relheight=0.92)
        self.__init_scrollbar()

    def __init_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.92, relwidth=0.98, relheight=0.08)


# Views Genericas
class ViewWindowVeiculo(tk.Toplevel):
    def __init__(self, parent, nome):
        super().__init__(parent)
        self.__set_window(parent, nome)
        self.__set_tree_view()

    def __set_window(self, parent, nome):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (500 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (200 / 2))
        self.geometry(f'500x200+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title(f'Veiculos {nome}')

    def __set_tree_view(self):
        columns = ('modelo', 'tipo', 'cor', 'placa')
        params = (150, 100, 100, 100)
        self.tree = TreView(self, columns, columns, 'headings')
        self.tree.set_tree_views(params, True)
        self.tree.place(relx=0, rely=0, relwidth=0.96, relheight=1)
        self.__init_scrollbar()

    def __init_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.96, rely=0, relwidth=0.04, relheight=1)


class ViewWindowEnterprise(tk.Toplevel):
    def __init__(self, parent, nome):
        super().__init__(parent)
        self.__set_window(parent, nome)
        self.__set_tree_view()

    def __set_window(self, parent, nome):
        center_x = int((parent.winfo_x() + (parent.winfo_width() / 2)) - (500 / 2))
        center_y = int((parent.winfo_y() + (parent.winfo_height() / 2)) - (200 / 2))
        self.geometry(f'800x200+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title(f'Empresa {nome}')

    def __set_tree_view(self):
        columns = ('nome', 'cnpj', 'telefone', 'rua', 'numero', 'bairro', 'cidade')
        params = (200, 150, 130, 250, 80, 150, 150)
        self.tree = TreView(self, columns, columns, 'headings')
        self.tree.set_tree_views(params, False)
        self.tree.place(relx=0, rely=0, relwidth=0.98, relheight=0.92)
        self.__init_scrollbar()

    def __init_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.92, relwidth=0.98, relheight=0.08)


class ViewFrameVeiculo(ttk.Frame):
    def __init__(self, container, width, height, objectt):
        super().__init__(container, width=width, height=height)
        self.objectt = objectt
        self.__init()

    def __init(self):
        self.base = ViewVeiculoBase(self)
        self.__set_icons()
        self.__set_buttons()
        self.__tooltip()
        self.__set_styles()
        self.list_veiculos = []

    def __set_buttons(self):
        self.badd = ttk.Button(self, image=self.iadd, command=self.add_veiculo)
        self.badd.place(relx=0.78, rely=0.02)
        self.bdeletar = ttk.Button(self, image=self.itrash, command=self.clear_tree)
        self.bdeletar.place(relx=0.88, rely=0.02)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_entrys)
        self.blimpar.place(relx=0.83, rely=0.02)
        self.bx = ttk.Button(self, text='X', command=self.__exit, style='Veiculo.TButton')
        self.bx.place(relx=0.97, rely=0.05, width=25, height=25, anchor=tk.CENTER)

    def __set_icons(self):
        self.iadd = tk.PhotoImage(file='../icons/icons_24/icons8-done-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-erase-24.png')
        self.itrash = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')
        self.ix = tk.PhotoImage(file='../icons/icons_24/icons8-close-24.png')

    def __tooltip(self):
        ToolTip(self.badd, msg='Adicionar', bg='white')
        ToolTip(self.bdeletar, msg='Apagar', bg='white')
        ToolTip(self.blimpar, msg='Limpar', bg='white')

    def __set_styles(self):
        self.style = ttk.Style(self)
        self.style.configure('Veiculo.TButton', background='#EC4343')

    def __exit(self):
        self.objectt.badd_veiculo.state(['!disabled'])
        self.objectt.veiculo_flag = False
        self.objectt.notebook.hide('current')

    def add_veiculo(self):
        if all(self.base.get_values()):
            veiculo = TypeVeiculo(
                self.base.emodelo.get_value(), self.base.etipo.get_value(), self.base.ecor.get_value(),
                self.base.eplaca.get_value()
            )
            if veiculo in self.list_veiculos:
                showerror('Erro', 'Veiculos com placas\nidenticas', parent=self)
            else:
                self.base.tree.insert(
                    '', tk.END, values=(
                        veiculo.modelo, veiculo.tipo, veiculo.cor, veiculo.placa
                    )
                )
                self.list_veiculos.append(veiculo)

    def clear_tree(self):
        self.base.clear_tree()
        self.list_veiculos.clear()

    def clear_entrys(self):
        self.base.clear_entrys()


class ViewFrameEnterprise(ttk.Frame):
    def __init__(self, container, width, height, objectt):
        super().__init__(container, width=width, height=height)
        self.__init(objectt)

    def __init(self, objectt):
        self.__set_entrys()
        self.__init_tree_views()
        self.__init_scrollbar()
        self.__set_icons()
        self.__set_buttons()
        self.__tooltip()
        self.__set_styles()
        self.controller = None
        self.values = None
        self.objectt = objectt

    def __set_entrys(self):
        self.enome = PlaceHolderEntry(self, "Nome")
        self.enome.place(relx=0.01, rely=0.06, relwidth=0.5)

    def __set_buttons(self):
        self.bpesquisar = ttk.Button(self, image=self.isearch, command=lambda: self.pesquisar(None))
        self.bpesquisar.place(relx=0.55, rely=0.04)
        self.blimpar = ttk.Button(self, image=self.ierase, command=self.clear_tree)
        self.blimpar.place(relx=0.63, rely=0.04)
        self.bexit = ttk.Button(self, text='X', style='Veiculo.TButton', command=self.__exit)
        self.bexit.place(relx=0.98, rely=0.05, width=25, height=25, anchor=tk.CENTER)

    def __set_icons(self):
        self.isearch = tk.PhotoImage(file='../icons/icons_24/icons8-search-24.png')
        self.ierase = tk.PhotoImage(file='../icons/icons_24/icons8-trash-24.png')

    def __tooltip(self):
        ToolTip(self.bpesquisar, msg='Procurar', bg='white')
        ToolTip(self.blimpar, msg='Limpar Lista', bg='white')

    def __init_tree_views(self):
        columns = ('uuid', 'nome', 'cnpj', 'telefone', 'veiculo', 'rua', 'numero', 'bairro', 'cidade', 'cep')
        display = ('nome', 'cnpj', 'telefone', 'rua', 'numero', 'bairro', 'cidade')
        params = (200, 150, 130, 250, 80, 150, 150)
        self.tree = TreView(self, columns, display, 'headings')
        self.tree.set_tree_views(params, False)
        self.tree.bind('<Double-1>', self.item_select)
        self.tree.place(relx=0, rely=0.2, relwidth=0.98, relheight=0.73)

    def __init_scrollbar(self):
        self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.place(relx=0.98, rely=0.2, relwidth=0.02, relheight=0.78)
        self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.place(relx=0, rely=0.93, relwidth=0.98, relheight=0.06)

    def __exit(self):
        self.objectt.bsearch.state(['!disabled'])
        self.objectt.notebook.hide('current')

    def __set_styles(self):
        self.style = ttk.Style(self)
        self.style.configure('Veiculo.TButton', background='#EC4343')

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def pesquisar(self, event):
        self.clear_tree()
        if self.enome.get_value():
            self.controller.search(self.enome.get_value())
        else:
            showerror('Erro', 'Digite um nome', parent=self)

    def item_select(self, event):
        uuid_id, nome, _, _, _, _, _, _, _, _ = self.tree.item(self.tree.selection()[0], 'values')
        self.objectt.base.eempresa.delete(0, tk.END)
        self.objectt.base.eempresa['state'] = 'normal'
        self.objectt.base.eempresa.insert('end', nome)
        self.objectt.base.uuid_empresa = uuid_id
        self.objectt.bsearch.state(['!disabled'])
        self.objectt.notebook.hide('current')

    def set_controller(self, controller):
        self.controller = controller


# Classes Bases
class ViewAddress:
    def __init__(self, parent):
        self.parent = parent
        self.__init()

    def __init(self):
        self.__set_vars()
        self.__set_labels()
        self.__set_entrys()

    def __set_labels(self):
        self.lb_rua = ttk.Label(self.parent, text='Rua')
        self.lb_rua.place(relx=0.01, rely=0.4)
        self.lb_cep = ttk.Label(self.parent, text='Cep')
        self.lb_cep.place(relx=0.65, rely=0.4)
        self.lb_bairro = ttk.Label(self.parent, text='Bairro')
        self.lb_bairro.place(relx=0.01, rely=0.6)
        self.lb_numero = ttk.Label(self.parent, text='Número')
        self.lb_numero.place(relx=0.55, rely=0.6)
        self.lb_cidade = ttk.Label(self.parent, text='Cidade')
        self.lb_cidade.place(relx=0.70, rely=0.6)

    def __set_entrys(self):
        self.entry_rua = ttk.Entry(self.parent, textvariable=self.rua)
        self.entry_rua.place(relx=0.01, rely=0.48, relwidth=0.60)
        self.entry_cep = ttk.Entry(self.parent, textvariable=self.cep)
        self.entry_cep.bind('<Return>', self.search_cep)
        self.entry_cep.place(relx=0.65, rely=0.48, relwidth=0.20)
        self.entry_bairro = ttk.Entry(self.parent, textvariable=self.bairro)
        self.entry_bairro.place(relx=0.01, rely=0.68, relwidth=0.50)
        self.entry_numero = ttk.Entry(self.parent, textvariable=self.numero)
        self.entry_numero.place(relx=0.55, rely=0.68, relwidth=0.09)
        self.entry_cidade = ttk.Entry(self.parent, textvariable=self.cidade)
        self.entry_cidade.place(relx=0.70, rely=0.68, relwidth=0.25)

    def __set_vars(self):
        self.rua = tk.StringVar()
        self.cep = tk.StringVar()
        self.bairro = tk.StringVar()
        self.numero = tk.StringVar()
        self.cidade = tk.StringVar()

    def clear_entrys(self, cep=True):
        self.entry_rua.delete(0, tk.END)
        if cep:
            self.entry_cep.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)

    def search_cep(self, event):
        self.clear_entrys(cep=False)
        cep_object = md.Address(cep=self.entry_cep.get())

        try:
            endereco = cep_object.search_cep()
        except Exception as error:
            ct.MessageBox.show_error(error, parent=self.parent)
        else:
            self.entry_bairro.insert('end', endereco['bairro'])
            self.entry_cidade.insert('end', endereco['cidade'])
            self.entry_rua.insert('end', endereco['logradouro'])


class PlaceHolderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder

        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.clear)
        self.bind("<FocusOut>", self.add)

    def clear(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)

    def add(self, e):
        if not self.get():
            self.insert(0, self.placeholder)

    def get_value(self):
        if self.get() == self.placeholder:
            return False
        else:
            return self.get()


class ViewVeiculoBase:
    def __init__(self, parent):
        self.parent = parent
        self.__set()

    def __set(self):
        self.__set_entrys()
        self.__binds()
        self.__set_tree_views()
        self.__set_scrollbar()

    def __set_entrys(self):
        self.emodelo = PlaceHolderEntry(self.parent, "Modelo")
        self.emodelo.place(relx=0.01, rely=0.05, relwidth=0.25)
        self.etipo = PlaceHolderEntry(self.parent, "Tipo")
        self.etipo.place(relx=0.28, rely=0.05, relwidth=0.15)
        self.ecor = PlaceHolderEntry(self.parent, "Cor")
        self.ecor.place(relx=0.45, rely=0.05, relwidth=0.15)
        self.eplaca = PlaceHolderEntry(self.parent, "Placa")
        self.eplaca.place(relx=0.62, rely=0.05, relwidth=0.15)

    def __binds(self):
        self.emodelo.bind("<Delete>", lambda x: self.emodelo.delete(0, tk.END))
        self.etipo.bind("<Delete>", lambda x: self.etipo.delete(0, tk.END))
        self.ecor.bind("<Delete>", lambda x: self.ecor.delete(0, tk.END))
        self.eplaca.bind("<Delete>", lambda x: self.eplaca.delete(0, tk.END))

    def __set_tree_views(self):
        columns = ('modelo', 'tipo', 'cor', 'placa')
        params = (150, 150, 150, 150)
        self.tree = TreView(self.parent, columns, columns, 'headings')
        self.tree.set_tree_views(params, True)
        self.tree.place(relx=0, rely=0.25, relwidth=0.98, relheight=0.75)

    def __set_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0.98, rely=0.25, relwidth=0.02, relheight=0.75)

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear_entrys(self):
        self.emodelo.delete(0, tk.END)
        self.emodelo.add(None)
        self.etipo.delete(0, tk.END)
        self.etipo.add(None)
        self.ecor.delete(0, tk.END)
        self.ecor.add(None)
        self.eplaca.delete(0, tk.END)
        self.eplaca.add(None)

    def get_values(self):
        return [self.emodelo.get_value(), self.etipo.get_value(), self.ecor.get_value(),
                self.eplaca.get_value()]


class ViewDoormanBase:
    def __init__(self, parent):
        self.parent = parent
        self.__set_vars()
        self.__set_labels()
        self.__set_entrys()
        self.__set_combox()
        self.__set_checkbox()
        self.__set_style()
        self.__set_separator()

    def __set_labels(self):
        self.lb_nome = ttk.Label(self.parent, text='Nome')
        self.lb_nome.place(relx=0.01, rely=0.01)
        self.lb_cpf = ttk.Label(self.parent, text='Cpf')
        self.lb_cpf.place(relx=0.6, rely=0.01)
        self.lb_telefone = ttk.Label(self.parent, text='Telefone')
        self.lb_telefone.place(relx=0.01, rely=0.25)
        self.lb_sexo = ttk.Label(self.parent, text='Sexo')
        self.lb_sexo.place(relx=0.25, rely=0.25)
        self.lb_email = ttk.Label(self.parent, text='Email')
        self.lb_email.place(relx=0.45, rely=0.25)
        self.lb_senha = ttk.Label(self.parent, text='Senha')
        self.lb_senha.place(relx=0.01, rely=0.5)
        self.lb_permissao = ttk.Label(self.parent, text='Permissões')
        self.lb_permissao.place(relx=0.46, rely=0.5)
        self.lb_adm = ttk.Label(self.parent, text='Administrador')
        self.lb_adm.place(relx=0.46, rely=0.73)

    def __set_entrys(self):
        self.entry_nome = ttk.Entry(self.parent, textvariable=self.nome)
        self.entry_nome.focus()
        self.entry_nome.place(relx=0.01, rely=0.09, relwidth=0.55)
        self.entry_cpf = ttk.Entry(self.parent, textvariable=self.cpf)
        self.entry_cpf.place(relx=0.6, rely=0.09, relwidth=0.25)
        self.entry_telefone = ttk.Entry(self.parent, textvariable=self.telefone)
        self.entry_telefone.place(relx=0.01, rely=0.34, relwidth=0.20)
        self.entry_email = ttk.Entry(self.parent, textvariable=self.email)
        self.entry_email.place(relx=0.45, rely=0.34, relwidth=0.4)
        self.entry_senha = ttk.Entry(self.parent, textvariable=self.senha)
        self.entry_senha.place(relx=0.01, rely=0.6, relwidth=0.25)

    def __set_combox(self):
        self.combox = ttk.Combobox(self.parent, textvariable=self.sexo)
        self.combox['values'] = ('Masculino', 'Feminino')
        self.combox['state'] = 'readonly'
        self.combox.place(relx=0.25, rely=0.34, relwidth=0.15)

    def __set_checkbox(self):
        self.check_adicionar = ttk.Checkbutton(
            self.parent, text='Adicionar', variable=self.adicionar, onvalue=1,
            offvalue=0, style='Doorman.TCheckbutton'
        )
        self.check_apagar = ttk.Checkbutton(
            self.parent, text='Apagar', variable=self.apagar, onvalue=1,
            offvalue=0, style='Doorman.TCheckbutton'
        )
        self.check_editar = ttk.Checkbutton(
            self.parent, text='Editar', variable=self.editar, onvalue=1,
            offvalue=0, style='Doorman.TCheckbutton'
        )
        self.check_adm = ttk.Checkbutton(
            self.parent, text='Administrador', variable=self.adm, onvalue=1,
            offvalue=0, style='Doorman.TCheckbutton'
        )
        self.check_adicionar.place(relx=0.5, rely=0.6)
        self.check_apagar.place(relx=0.65, rely=0.6)
        self.check_editar.place(relx=0.75, rely=0.6)
        self.check_adm.place(relx=0.5, rely=0.84)

    def __set_separator(self):
        self.sep1 = ttk.Separator(self.parent, orient='horizontal')
        self.sep1.place(relx=0.46, rely=0.58, relwidth=0.45)
        self.sep2 = ttk.Separator(self.parent, orient='horizontal')
        self.sep2.place(relx=0.46, rely=0.7, relwidth=0.45)
        self.sep3 = ttk.Separator(self.parent, orient='vertical')
        self.sep3.place(relx=0.46, rely=0.58, relheight=0.12)
        self.sep4 = ttk.Separator(self.parent, orient='vertical')
        self.sep4.place(relx=0.91, rely=0.58, relheight=0.12)
        self.sep5 = ttk.Separator(self.parent, orient='horizontal')
        self.sep5.place(relx=0.46, rely=0.82, relwidth=0.25)
        self.sep6 = ttk.Separator(self.parent, orient='horizontal')
        self.sep6.place(relx=0.46, rely=0.95, relwidth=0.25)
        self.sep7 = ttk.Separator(self.parent, orient='vertical')
        self.sep7.place(relx=0.46, rely=0.82, relheight=0.13)
        self.sep8 = ttk.Separator(self.parent, orient='vertical')
        self.sep8.place(relx=0.71, rely=0.82, relheight=0.13)

    def __set_vars(self):
        self.nome = tk.StringVar()
        self.cpf = tk.StringVar()
        self.telefone = tk.StringVar()
        self.sexo = tk.StringVar()
        self.email = tk.StringVar()
        self.senha = tk.StringVar()
        self.adicionar = tk.IntVar()
        self.apagar = tk.IntVar()
        self.editar = tk.IntVar()
        self.adm = tk.IntVar()

    def __set_style(self):
        self.style = ttk.Style(self.parent)
        self.style.configure('Doorman.TCheckbutton', background='white', font=('Arial', 12))

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)


class ViewEnterpriseBase:
    def __init__(self, parent):
        self.parent = parent
        self.address = ViewAddress(parent)
        self.__set_vars()
        self.__set_labels()
        self.__set_entrys()

    def __set_labels(self):
        self.lb_nome = ttk.Label(self.parent, text='Nome Fantasia')
        self.lb_nome.place(relx=0.01, rely=0.01)
        self.lb_cnpj = ttk.Label(self.parent, text='Cnpj')
        self.lb_cnpj.place(relx=0.65, rely=0.01)
        self.lb_telefone = ttk.Label(self.parent, text='Telefone')
        self.lb_telefone.place(relx=0.01, rely=0.2)

    def __set_entrys(self):
        self.entry_nome = ttk.Entry(self.parent, textvariable=self.nome)
        self.entry_nome.place(relx=0.01, rely=0.1, relwidth=0.6)
        self.entry_nome.focus()
        self.entry_cnpj = ttk.Entry(self.parent, textvariable=self.cnpj)
        self.entry_cnpj.place(relx=0.65, rely=0.1, relwidth=0.25)
        self.entry_telefone = ttk.Entry(self.parent, textvariable=self.telefone)
        self.entry_telefone.place(relx=0.01, rely=0.28, relwidth=0.25)

    def __set_vars(self):
        self.nome = tk.StringVar()
        self.cnpj = tk.StringVar()
        self.telefone = tk.StringVar()

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cnpj.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.address.clear_entrys()


class ViewHabitantBase:
    def __init__(self, parent):
        self.parent = parent
        self.__set_vars()
        self.__set_labels()
        self.__set_entrys()

    def __set_labels(self):
        self.lb_nome = ttk.Label(self.parent, text='Nome')
        self.lb_nome.place(relx=0.01, rely=0.01)
        self.lb_cpf = ttk.Label(self.parent, text='Cpf')
        self.lb_cpf.place(relx=0.6, rely=0.01)
        self.lb_telefone = ttk.Label(self.parent, text='Telefone')
        self.lb_telefone.place(relx=0.01, rely=0.31)
        self.lb_residencia = ttk.Label(self.parent, text='N° Apt')
        self.lb_residencia.place(relx=0.30, rely=0.31)

    def __set_entrys(self):
        self.entry_nome = ttk.Entry(self.parent, textvariable=self.nome)
        self.entry_nome.focus()
        self.entry_nome.place(relx=0.01, rely=0.09, relwidth=0.55)
        self.entry_cpf = ttk.Entry(self.parent, textvariable=self.cpf)
        self.entry_cpf.place(relx=0.6, rely=0.09, relwidth=0.25)
        self.entry_telefone = ttk.Entry(self.parent, textvariable=self.telefone)
        self.entry_telefone.place(relx=0.01, rely=0.39, relwidth=0.20)
        self.entry_residencia = ttk.Entry(self.parent, textvariable=self.residencia)
        self.entry_residencia.place(relx=0.30, rely=0.39, relwidth=0.1)

    def __set_vars(self):
        self.nome = tk.StringVar()
        self.cpf = tk.StringVar()
        self.telefone = tk.StringVar()
        self.residencia = tk.StringVar()

    def limpar_tela(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_residencia.delete(0, tk.END)


class ViewVisitorBase:
    def __init__(self, parent):
        self.parent = parent
        self.__set_vars()
        self.__set_labels()
        self.__set_entrys()
        self.__set_combox()
        self.uuid_empresa = None

    def __set_labels(self):
        self.lnome = ttk.Label(self.parent, text='Nome')
        self.lnome.place(relx=0, rely=0)
        self.lcpf = ttk.Label(self.parent, text='Cpf')
        self.lcpf.place(relx=0.6, rely=0.01)
        self.lsexo = ttk.Label(self.parent, text='Sexo')
        self.lsexo.place(relx=0.23, rely=0.23)
        self.ltelefone = ttk.Label(self.parent, text='Telefone')
        self.ltelefone.place(relx=0.01, rely=0.23)
        self.lempresa = ttk.Label(self.parent, text='Empresa')
        self.lempresa.place(relx=0.4, rely=0.23)

    def __set_entrys(self):
        self.enome = ttk.Entry(self.parent, textvariable=self.nome)
        self.enome.focus()
        self.enome.place(relx=0.01, rely=0.09, relwidth=0.55)
        self.ecpf = ttk.Entry(self.parent, textvariable=self.cpf)
        self.ecpf.place(relx=0.6, rely=0.09, relwidth=0.25)
        self.etelefone = ttk.Entry(self.parent, textvariable=self.telefone)
        self.etelefone.place(relx=0.01, rely=0.33, relwidth=0.20)
        self.eempresa = ttk.Entry(self.parent, textvariable=self.empresa)
        self.eempresa['state'] = 'disabled'
        self.eempresa.place(relx=0.4, rely=0.33, relwidth=0.4)

    def __set_combox(self):
        self.combox = ttk.Combobox(self.parent, textvariable=self.sexo)
        self.combox['values'] = ('Masculino', 'Feminino')
        self.combox['state'] = 'readonly'
        self.combox.place(relx=0.23, rely=0.33, relwidth=0.15)

    def __set_vars(self):
        self.nome = tk.StringVar()
        self.cpf = tk.StringVar()
        self.telefone = tk.StringVar()
        self.sexo = tk.StringVar()
        self.empresa = tk.StringVar()
        self.empresa.trace('w', self.bind_entry_empresa)

    def limpar_tela(self):
        self.enome.delete(0, tk.END)
        self.ecpf.delete(0, tk.END)
        self.etelefone.delete(0, tk.END)
        self.eempresa.delete(0, tk.END)

    def bind_entry_empresa(self, *args):
        if len(self.empresa.get()) == 0:
            self.eempresa['state'] = 'disabled'
            self.uuid_empresa = None
