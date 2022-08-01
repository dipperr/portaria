import sqlite3
import hashlib
import logging
from pycep_correios import get_address_from_cep
from pycep_correios import WebService
from pycep_correios import exceptions
import uuid

from dtbase.dtbase import DataBase
from query import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Crud:
    def __init__(self):
        logging.info('instanciou crud')
        self.database = DataBase()

    def save(self, query, valores):
        self.database.execute(query, valores)
        self.database.close_bd()

    def search(self, query):
        self.database.execute(query)
        consulta = self.database.cursor.fetchall()
        self.database.close_bd()
        return consulta

    def delete(self, query, valor):
        self.database.execute(query, valor)
        self.database.close_bd()

    def update(self, query, valores):
        self.database.execute(query, valores)
        self.database.close_bd()


class Address:
    def __init__(self, rua=None, numero=None, bairro=None, cidade=None, cep=None):
        self.__rua = rua
        self.__numero = numero
        self.__bairro = bairro
        self.__cidade = cidade
        self.__cep = cep
        self.crud = Crud()

    @property
    def rua(self):
        return self.__rua.lower().strip()

    @property
    def numero(self):
        return self.__numero

    @property
    def bairro(self):
        return self.__bairro.lower().strip()

    @property
    def cidade(self):
        return self.__cidade.lower().strip()

    @property
    def cep(self):
        return self.__cep.replace('-', '').replace('.', '').replace(' ', '')

    def search_cep(self):
        """o formato de resposta é um objeto dict com as seguintes chaves:
           bairro, cep, cidade, logradouro, uf, complemento"""
        try:
            endereco = get_address_from_cep(self.cep, webservice=WebService.APICEP)
        except exceptions.InvalidCEP:
            raise Exception('Cep inválido')
        except exceptions.CEPNotFound:
            raise Exception('Cep não encontrado')
        except exceptions.ConnectionError:
            raise Exception('Sem conexão com a internet')
        else:
            return endereco

    def save(self, query, uuid_empresa):
        if self.non_null_validation():
            self.crud.save(query, (self.rua, self.numero, self.bairro, self.cidade, self.cep, uuid_empresa))
        else:
            raise ValueError('Valores Ausentes')

    def update(self, query, uuid_empresa):
        logging.info('executando o update da classe carro')
        if self.non_null_validation():
            self.crud.update(query, (self.rua, self.numero, self.bairro, self.cidade, self.cep, uuid_empresa))
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.rua, self.numero, self.bairro, self.cidade, self.cep])


class Veiculo:
    logging.info('instanciou veiculo')

    def __init__(self, modelo=None, tipo=None, cor=None, placa=None, uuid_id=None):
        self.__cor = cor
        self.__modelo = modelo
        self.__tipo = tipo
        self.__placa = placa
        self.uuid_id = uuid_id
        self.crud = Crud()

    @property
    def cor(self):
        return self.__cor.lower().strip()

    @property
    def modelo(self):
        return self.__modelo.lower().strip()

    @property
    def tipo(self):
        return self.__tipo.lower().strip()

    @property
    def placa(self):
        return self.__placa.lower().strip()

    def save(self, query):
        self.crud.save(query, (self.modelo, self.tipo, self.cor, self.placa, self.uuid_id))

    def search_placa(self, query):
        return self.crud.search(query.format(self.placa))

    def search_uuid(self, query):
        return self.crud.search(query.format(self.uuid_id))

    def search_all(self, query):
        return self.crud.search(query)

    def delete_placa(self, query):
        self.crud.delete(query, (self.placa,))

    def non_null_validation(self):
        return all([self.cor, self.modelo, self.tipo, self.placa])


class Doorman:
    def __init__(
            self, cpf=None, nome=None, telefone=None, sexo=None, email=None, senha=None, adicionar=None, apagar=None,
            editar=None, adm=None, uuid_id=None):
        self.__cpf = cpf
        self.__nome = nome
        self.__telefone = telefone
        self.__email = email
        self.senha = senha
        self.sexo = sexo
        self.adicionar = adicionar
        self.apagar = apagar
        self.editar = editar
        self.adm = adm
        self.uuid_id = uuid_id
        self.crud = Crud()

    @property
    def cpf(self):
        return self.__cpf.replace('.', '').replace('/', '').replace('-', '').replace(' ', '')

    @property
    def nome(self):
        return self.__nome.lower().strip()

    @property
    def telefone(self):
        return self.__telefone.strip()

    @property
    def email(self):
        return self.__email.strip()

    def save(self):
        if self.non_null_validation():
            self.__gen_uuid()
            self.__gen_hash()
            self.crud.save(save_doorman, (self.uuid_id, self.cpf, self.nome, self.telefone, self.sexo, self.email,
                                          self.senha, self.adicionar, self.apagar, self.editar, self.adm))
        else:
            raise ValueError('Valores Ausentes')

    def search_nome(self):
        return self.crud.search(search_doorman_nome.format(self.nome))

    def search_uuid(self):
        return self.crud.search(search_doorman_uuid.format(self.uuid_id))

    def search_all(self):
        return self.crud.search(search_doorman_all)

    def delete(self):
        self.crud.delete(delete_doorman, (self.uuid_id,))

    def update(self):
        logging.info('executando o update da classe porteiro')
        if all([self.cpf, self.nome, self.telefone, self.sexo, self.email]):
            if self.senha is None:
                self.crud.update(update_doorman, (self.cpf, self.nome, self.telefone, self.sexo, self.email,
                                                  self.adicionar, self.editar, self.apagar, self.adm, self.uuid_id))
            else:
                self.__gen_hash()
                self.crud.update(update_doorman_key, (self.cpf, self.nome, self.telefone, self.sexo, self.email,
                                                      self.senha, self.adicionar, self.editar, self.apagar, self.adm,
                                                      self.uuid_id))
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cpf, self.nome, self.telefone, self.sexo, self.email, self.senha])

    def __gen_uuid(self):
        self.uuid_id = str(uuid.uuid4())

    def __gen_hash(self):
        self.senha = hashlib.md5(self.senha.strip().encode()).hexdigest()


class Enterprise:
    def __init__(
            self, cnpj=None, nome=None, telefone=None, rua=None, numero=None, bairro=None, cidade=None, cep=None,
            list_veiculos=None, uuid_id=None):
        self.__cnpj = cnpj
        self.__nome = nome
        self.__telefone = telefone
        self.list_veiculos = list_veiculos
        self.uuid_id = uuid_id
        self.fveiculo = 0
        self.endereco = Address(rua, numero, bairro, cidade, cep)
        self.crud = Crud()

    @property
    def cnpj(self):
        return self.__cnpj.replace('.', '').replace('/', '').replace('-', '').replace(' ', '')

    @property
    def nome(self):
        return self.__nome.lower().strip()

    @property
    def telefone(self):
        return self.__telefone.strip()

    def save(self):
        if self.non_null_validation() and self.endereco.non_null_validation():
            self.__gen_uuid()
            self.__values_flags_save()
            try:
                self.crud.save(save_enterprise, (self.uuid_id, self.cnpj, self.nome, self.telefone, self.fveiculo))
            except sqlite3.IntegrityError:
                raise ValueError('Erro de integridade\n Tente novamente')
            else:
                self.endereco.save(save_endereco_enterprise, self.uuid_id)
                if self.list_veiculos:
                    try:
                        for veic in self.list_veiculos:
                            veiculo = Veiculo(veic.modelo, veic.tipo, veic.cor, veic.placa, self.uuid_id)
                            veiculo.save(save_veiculo_enterprise)
                    except sqlite3.IntegrityError:
                        raise ValueError('Erro de integridade\nVeiculos com placas iguais')
        else:
            raise ValueError('Valores Ausentes')

    def search_nome(self):
        return self.crud.search(search_enterprise_nome.format(self.nome))

    def search_uuid(self):
        return self.crud.search(search_enterprise_uuid.format(self.uuid_id))

    def search_enterprise_veiculo(self):
        return self.crud.search(search_enterprise_with_veiculo)

    def search_veiculo(self):
        return self.crud.search(search_enterprise_veiculo_uuid.format(self.uuid_id))

    def search_all(self):
        return self.crud.search(search_enterprise_all)

    def delete(self):
        self.crud.delete(delete_enterprise, (self.uuid_id,))

    def update(self):
        logging.info('executando o update da classe empresa')
        if self.non_null_validation() and self.endereco.non_null_validation():
            self.__values_flags_update()
            self.crud.update(update_enterprise, (self.cnpj, self.nome, self.telefone, self.fveiculo, self.uuid_id))
            self.endereco.update(update_endereco_enterprise, self.uuid_id)
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cnpj, self.nome, self.telefone])

    def __gen_uuid(self):
        self.uuid_id = str(uuid.uuid4())

    def __values_flags_save(self):
        if self.list_veiculos:
            self.fveiculo = 1

    def __values_flags_update(self):
        if self.crud.search(search_enterprise_veiculo_uuid.format(self.uuid_id)):
            self.fveiculo = 1


class Habitant:
    def __init__(self, cpf=None, nome=None, telefone=None, residencia=None, list_veiculos=None, uuid_id=None):
        self.__cpf = cpf
        self.__nome = nome
        self.__telefone = telefone
        self.__residencia = residencia
        self.list_veiculos = list_veiculos
        self.uuid_id = uuid_id
        self.fveiculo = 0
        self.crud = Crud()

    @property
    def cpf(self):
        return self.__cpf.replace('.', '').replace('-', '').replace(' ', '')

    @property
    def nome(self):
        return self.__nome.lower().strip()

    @property
    def telefone(self):
        return self.__telefone.strip()

    @property
    def residencia(self):
        return self.__residencia

    def save(self):
        if self.non_null_validation():
            self.__gen_uuid()
            self.__values_flags_save()
            try:
                self.crud.save(save_habitant, (self.uuid_id, self.cpf, self.nome, self.telefone, self.residencia,
                                               self.fveiculo))
            except sqlite3.IntegrityError:
                raise ValueError('Erro de integridade\n Tente novamente')
            else:
                if self.list_veiculos:
                    try:
                        for veic in self.list_veiculos:
                            veiculo = Veiculo(veic.modelo, veic.tipo, veic.cor, veic.placa, self.uuid_id)
                            veiculo.save(save_veiculo_habitant)
                    except sqlite3.IntegrityError:
                        raise ValueError('Erro de integridade\nVeiculos com placas iguais')
        else:
            raise ValueError('Valores Ausentes')

    def search_nome(self):
        return self.crud.search(search_habitant_nome.format(self.nome))

    def search_uuid(self):
        return self.crud.search(search_habitant_uuid.format(self.uuid_id))

    def search_all(self):
        return self.crud.search(search_habitant_all)

    def search_pessoa_veiculo(self):
        return self.crud.search(search_habitant_with_veiculo)

    def search_veiculo(self):
        return self.crud.search(search_habitant_veiculo_uuid.format(self.uuid_id))

    def delete(self):
        self.crud.delete(delete_habitant, (self.uuid_id,))

    def update(self):
        logging.info('executando o update da classe habitant')
        if self.non_null_validation():
            self.__values_flags_update()
            self.crud.update(update_habitant, (self.cpf, self.nome, self.telefone, self.residencia, self.fveiculo,
                                               self.uuid_id))
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cpf, self.nome, self.telefone, self.residencia])

    def __gen_uuid(self):
        self.uuid_id = str(uuid.uuid4())

    def __values_flags_save(self):
        if self.list_veiculos:
            self.fveiculo = 1

    def __values_flags_update(self):
        if self.crud.search(search_habitant_veiculo_uuid.format(self.uuid_id)):
            self.fveiculo = 1


class Visitor:
    def __init__(
            self, cpf=None, nome=None, telefone=None, sexo=None, uuid_empresa=None, path=None, list_veiculos=None,
            uuid_id=None):
        self.__cpf = cpf
        self.__nome = nome
        self.__telefone = telefone
        self.__sexo = sexo
        self.path = path
        self.uuid_empresa = uuid_empresa
        self.list_veiculos = list_veiculos
        self.uuid_id = uuid_id
        self.fveiculo = 0
        self.fempresa = 0
        self.crud = Crud()

    @property
    def cpf(self):
        return self.__cpf.replace('.', '').replace('-', '').replace(' ', '')

    @property
    def nome(self):
        return self.__nome.lower().strip()

    @property
    def telefone(self):
        return self.__telefone.strip()

    @property
    def sexo(self):
        return self.__sexo.lower().strip()

    def save(self):
        if self.non_null_validation():
            self.__gen_uuid()
            self.__values_flags_save()
            try:
                self.crud.save(save_visitor, (self.uuid_id, self.cpf, self.nome, self.telefone, self.sexo,
                                              self.fveiculo, self.fempresa))
            except sqlite3.IntegrityError:
                raise ValueError('Erro de integridade\n Tente novamente')
            else:
                if self.uuid_empresa is not None:
                    self.crud.save(save_visitor_enterprise, (self.uuid_id, self.uuid_empresa))
                if self.list_veiculos:
                    try:
                        for veic in self.list_veiculos:
                            veiculo = Veiculo(veic.modelo, veic.tipo, veic.cor, veic.placa, self.uuid_id)
                            veiculo.save(save_veiculo_visitor)
                    except sqlite3.IntegrityError:
                        raise ValueError('Erro de integridade\nVeiculos com placas iguais')
        else:
            raise ValueError('Valores Ausentes')

    def search_uuid(self):
        return self.crud.search(search_visitor_uuid.format(self.uuid_id))

    def search_nome(self):
        return self.crud.search(search_visitor_nome.format(self.nome))

    def search_all(self):
        return self.crud.search(search_visitor_all)

    def search_pessoa_work(self):
        return self.crud.search(search_visitor_with_work)

    def search_pessoa_veiculo(self):
        return self.crud.search(search_visitor_with_veiculo)

    def search_veiculo(self):
        return self.crud.search(search_visitor_veiculo.format(self.uuid_id))

    def search_enterprise(self):
        return self.crud.search(search_visitor_enterprise.format(self.uuid_id))

    def search_with_ent_veic(self):
        return self.crud.search(search_visitor_with_ent_veic)

    def delete(self):
        self.crud.delete(delete_visitor, (self.uuid_id,))

    def update(self):
        logging.info('executando o update da classe visitante')
        if self.non_null_validation():
            self.__values_flags_update()
            self.crud.update(update_visitor, (self.cpf, self.nome, self.telefone, self.sexo, self.fveiculo,
                                              self.fempresa, self.uuid_id))
            if self.uuid_empresa is not None:
                self.crud.update(update_visitor_enterprise, (self.uuid_empresa, self.uuid_id))
        else:
            raise ValueError('Valores Ausentes')

    def non_null_validation(self):
        return all([self.cpf, self.nome, self.telefone, self.sexo])

    def __gen_uuid(self):
        self.uuid_id = str(uuid.uuid4())

    def __values_flags_save(self):
        if self.uuid_empresa is not None:
            self.fempresa = 1
        if self.list_veiculos:
            self.fveiculo = 1

    def __values_flags_update(self):
        if self.uuid_empresa is not None:
            self.fempresa = 1
        else:
            self.crud.delete(delete_funcionario, (self.uuid_id,))
        if self.crud.search(search_visitor_veiculo.format(self.uuid_id)):
            self.fveiculo = 1
