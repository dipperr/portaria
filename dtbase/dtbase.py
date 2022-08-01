import sqlite3
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DataBase:

    def __init_bd(self):
        logging.info('conectando a base de dados')
        self.conexao = sqlite3.connect(
            '/home/luiz/Documentos/database/bancodados2'
        )
        self.cursor = self.conexao.cursor()
        self.cursor.execute("""PRAGMA foreign_keys = ON""")

    def execute(self, query, valores=None):
        self.__init_bd()
        if valores is not None:
            self.cursor.execute(query, valores)
            self.conexao.commit()
        else:
            self.cursor.execute(query)
            self.conexao.commit()

    def close_bd(self):
        logging.info('fechando a conexão')
        self.cursor.close()
        self.conexao.close()
