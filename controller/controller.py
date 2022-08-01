import tkinter as tk
import sqlite3
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

import models.models as md
import views.views as vw
from query import *


class MessageBox:
    @staticmethod
    def show_info(parent, message='Dados adicionados!!'):
        showinfo('Informação', message, parent=parent)

    @staticmethod
    def show_error(message, parent):
        showerror('Erro!', message, parent=parent)


class ControllerDoorman:
    def __init__(self, view):
        self.view = view

    def save(self, cpf, nome, telefone, sexo, email, senha, adicionar, apagar, editar, adm):
        try:
            self.model = md.Doorman(cpf, nome, telefone, sexo, email, senha, adicionar, apagar, editar, adm)
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        try:
            self.model = md.Doorman(nome=nome)
            consulta = self.model.search_nome()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            self.model = md.Doorman()
            consulta = self.model.search_all()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, uuid_id):
        try:
            self.model = md.Doorman(uuid_id=uuid_id)
            self.model.delete()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cpf, nome, telefone, sexo, email, uuid_id):
        try:
            self.model = md.Doorman(cpf, nome, telefone, sexo, email, uuid_id)
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)


class ControllerUpdDoorman:
    def __init__(self, view):
        self.view = view

    def insert_infos(self, uuid_id):
        self.model = md.Doorman(uuid_id=uuid_id)
        uuid, nome, cpf, telefone, sexo, email, adicionar, editar, apagar, adm = self.model.search_uuid()[0]
        self.doorman = vw.TypeDoorman(uuid, nome, cpf, telefone, sexo, email, adicionar, editar, apagar, adm)
        self.view.base.entry_nome.insert('end', self.doorman.nome)
        self.view.base.entry_cpf.insert('end', self.doorman.cpf)
        self.view.base.entry_telefone.insert('end', self.doorman.telefone)
        self.view.base.entry_email.insert('end', self.doorman.email)
        self.view.base.combox.set(self.doorman.sexo)
        if self.doorman.adicionar == 'sim':
            self.view.base.check_adicionar.invoke()
        if self.doorman.editar == 'sim':
            self.view.base.check_editar.invoke()
        if self.doorman.apagar == 'sim':
            self.view.base.check_apagar.invoke()
            if self.doorman.adm == 'sim':
                self.view.base.check_adm.invoke()

    def update(self, cpf, nome, telefone, sexo, email, senha, adicionar, apagar, editar, adm, uuid_id):
        try:
            self.model = md.Doorman(cpf, nome, telefone, sexo, email, senha, adicionar, apagar, editar, adm, uuid_id)
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view, message='Dados Atualizados!!')


class ControllerEnterprise:
    def __init__(self, view):
        self.view = view

    def save(self, cnpj, nome, telefone, rua, numero, bairro, cidade, cep, list_veiculos=None):
        try:
            self.model = md.Enterprise(cnpj, nome, telefone, rua, numero, bairro, cidade, cep, list_veiculos)
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        try:
            self.model = md.Enterprise(nome=nome)
            consulta = self.model.search_nome()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_enterprise_veiculo(self):
        try:
            self.model = md.Enterprise()
            consulta = self.model.search_enterprise_veiculo()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            self.model = md.Enterprise()
            consulta = self.model.search_all()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_veiculo(self, uuid_id):
        try:
            self.model = md.Enterprise(uuid_id=uuid_id)
            consulta = self.model.search_veiculo()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, uuid_id):
        try:
            self.model = md.Enterprise(uuid_id=uuid_id)
            self.model.delete()
        except ConnectionError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cnpj, nome, telefone, rua, numero, bairro, cidade, cep, uuid_id):
        try:
            self.model = md.Enterprise(cnpj, nome, telefone, rua, numero, bairro, cidade, cep, uuid_id=uuid_id)
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view, message='Dados Atualizados!!')


class ControllerVeiculoEnterprise:
    def __init__(self, view):
        self.view = view

    def save(self, modelo, tipo, cor, placa, uuid_id):
        self.model = md.Veiculo(modelo, tipo, cor, placa, uuid_id)
        self.model.save(save_veiculo_enterprise)

    def search(self, uuid_id):
        self.model = md.Veiculo(uuid_id=uuid_id)
        consulta = self.model.search_uuid(search_enterprise_veiculo_uuid)
        for c in consulta:
            veiculo = vw.TypeVeiculo(c[0], c[1], c[2], c[3])
            self.view.list_veiculos.append(veiculo)
            self.view.base.tree.insert('', 0, values=c)

    def delete(self, placa):
        self.model = md.Veiculo(placa=placa)
        self.model.delete_placa(delete_veiculo_enterprise)


class ControllerHabitant:
    def __init__(self, view):
        self.view = view

    def save(self, cpf, nome, telefone, residencia, list_veiculos=None):
        try:
            self.model = md.Habitant(cpf, nome, telefone, residencia, list_veiculos)
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        try:
            self.model = md.Habitant(nome=nome)
            consulta = self.model.search_nome()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_pessoa_veiculo(self):
        try:
            self.model = md.Habitant()
            consulta = self.model.search_pessoa_veiculo()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            self.model = md.Habitant()
            consulta = self.model.search_all()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_veiculo(self, uuid_id):
        try:
            self.model = md.Habitant(uuid_id=uuid_id)
            consulta = self.model.search_veiculo()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, uuid_id):
        try:
            self.model = md.Habitant(uuid_id=uuid_id)
            self.model.delete()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cpf, nome, telefone, residencia, uuid_id):
        try:
            self.model = md.Habitant(cpf, nome, telefone, residencia, uuid_id=uuid_id)
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view, message='Dados Atualizados!!')


class ControllerVeiculoHabitant:
    def __init__(self, view):
        self.view = view

    def save(self, modelo, tipo, cor, placa, uuid_id):
        self.model = md.Veiculo(modelo, tipo, cor, placa, uuid_id)
        self.model.save(save_veiculo_habitant)

    def search(self, uuid_id):
        self.model = md.Veiculo(uuid_id=uuid_id)
        consulta = self.model.search_uuid(search_habitant_veiculo_uuid)
        for c in consulta:
            veiculo = vw.TypeVeiculo(c[0], c[1], c[2], c[3])
            self.view.list_veiculos.append(veiculo)
            self.view.base.tree.insert('', 0, values=c)

    def delete(self, placa):
        self.model = md.Veiculo(placa=placa)
        self.model.delete_placa(delete_veiculo_habitant)


class ControllerVisitor:
    def __init__(self, view):
        self.view = view

    def save(self, cpf, nome, telefone, sexo, uuid_empresa, path=None, list_veiculos=None):
        try:
            self.model = md.Visitor(cpf, nome, telefone, sexo, uuid_empresa, path, list_veiculos)
            self.model.save()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            MessageBox.show_info(parent=self.view)

    def search(self, nome):
        try:
            self.model = md.Visitor(nome=nome)
            consulta = self.model.search_nome()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_all(self):
        try:
            self.model = md.Visitor()
            consulta = self.model.search_all()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_pessoa_work(self):
        try:
            self.model = md.Visitor()
            consulta = self.model.search_pessoa_work()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_pessoa_veiculo(self):
        try:
            self.model = md.Visitor()
            consulta = self.model.search_pessoa_veiculo()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_veiculo(self, uuid_id):
        try:
            self.model = md.Visitor(uuid_id=uuid_id)
            consulta = self.model.search_veiculo()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_enterprise(self, uuid_id):
        try:
            self.model = md.Visitor(uuid_id=uuid_id)
            consulta = self.model.search_enterprise()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def search_with_ent_veic(self):
        try:
            self.model = md.Visitor()
            consulta = self.model.search_with_ent_veic()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        else:
            for c in consulta:
                self.view.tree.insert('', 0, values=c)

    def delete(self, uuid_id):
        try:
            self.model = md.Visitor(uuid_id=uuid_id)
            self.model.delete()
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)

    def update(self, cpf, nome, telefone, sexo, uuid_id, uuid_empresa):
        try:
            self.model = md.Visitor(cpf, nome, telefone, sexo, uuid_id=uuid_id, uuid_empresa=uuid_empresa)
            self.model.update()
        except ValueError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.OperationalError as error:
            MessageBox.show_error(error, parent=self.view)
        except sqlite3.IntegrityError:
            MessageBox.show_error('Cpf repetido!!!', parent=self.view)
        else:
            MessageBox.show_info(parent=self.view, message='Dados Atualizados!!')

    def search_enterprise_nome(self, uuid_id):
        self.model = md.Visitor(uuid_id=uuid_id)
        return self.model.search_enterprise()[0]


class ControllerVeiculoVisitante:
    def __init__(self, view):
        self.view = view

    def save(self, modelo, tipo, cor, placa, uuid_id):
        self.model = md.Veiculo(modelo, tipo, cor, placa, uuid_id)
        self.model.save(save_veiculo_visitor)

    def search(self, uuid_id):
        self.model = md.Veiculo(uuid_id=uuid_id)
        consulta = self.model.search_uuid(search_visitor_veiculo)
        for c in consulta:
            veiculo = vw.TypeVeiculo(c[0], c[1], c[2], c[3])
            self.view.list_veiculos.append(veiculo)
            self.view.base.tree.insert('', 0, values=c)

    def delete(self, placa):
        self.model = md.Veiculo(placa=placa)
        self.model.delete_placa(delete_veiculo_visitante)
