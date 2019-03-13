__author__: 'Marcelo dos Santos'

import sqlite3
import datetime
import logging

class BD:
    '''Class model for management in the local database 
    '''
    def __init__(self):
        '''Create database if not exists
        ''' 
        logging.basicConfig(filename='teste.log', level=logging.INFO)
        self.create()

    def __str__(self):
        return '__author__: Marcelo dos Santos'

    @classmethod
    def conectar(self):
        return sqlite3.connect('teste.bd')
    
    def select(self, column='*', id=None):
        conn_select =  self.conectar()
        cursor = conn_select.cursor()
        cmd = 'SELECT {} FROM USER'
        dados = None
        if id:
            cmd +=  ' WHERE ID={};'
            try:
                cursor.execute(cmd.format(column, id))
                dados = cursor.fetchall()
                logging.info('Data selected-->In: {}'.format(self.hour_now()[0]))
            except:
                logging.error('Erro to run select command by id-->In: {}'.format(self.hour_now()[0]))
        else:
            try:
                cmd += ';'
                cursor.execute(cmd.format(column))
                dados = cursor.fetchall()
                logging.info('Data selected-->In: {}'.format(self.hour_now()[0]))
            except:
                logging.error('Error to run select command by column-->In: {}'.format(self.hour_now()[0]))
        conn_select.close()
        return dados

    def insert(self, VALUES):
        conn_insert = self.conectar()
        cursor = conn_insert.cursor()
        VALUES.extend(self.hour_now())
        controll = False
        #IMPLEMENTAR COLUNA BLOB E TENTAR INSERIR UMA IMAGEM
        try:
            cursor.execute('INSERT INTO USER (NAME, AGE, CREATED_IN, HOUR) VALUES (?,?,?,?);', VALUES)
            conn_insert.commit()
            logging.info('Data inserted-->In: {}'.format(self.hour_now()[0]))
            controll = True
        except:
            logging.error('Error to insert-->In: {}'.format(self.hour_now()[0]))
        finally:        
            conn_insert.close()
            return controll

    @classmethod
    def create(self):
        conn_create = self.conectar()
        cursor = conn_create.cursor()
        controll = False
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS USER ( \
                            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                            NAME VARCHAR(30) NOT NULL, \
                            AGE INTEGER NOT NULL,\
                            CREATED_IN DATE, \
                            HOUR CHAR(8));")
            conn_create.commit()
            logging.info('Table USER created-->In: {}'.format(self.hour_now()[0]))
            controll = True
        except:
            logging.error('Error to create table USER-->In: {}'.format(self.hour_now()[0]))
        finally:
            conn_create.close()
            return controll

    def atualiza(self, VALUES):
        conn_create = self.conectar()
        cursor = conn_create.cursor()
        controll = False
        try:
            cursor.execute("UPDATE USER \
                            SET NAME = ?, AGE = ? \
                            WHERE ID = ?;", VALUES)
            conn_create.commit()
            logging.info('Data updated with sucess-->In: {}'.format(self.hour_now()[0]))
            controll = True
        except:
            logging.error('Error to update database-->In: {}'.format(self.hour_now()[0]))
        finally:
            conn_create.close()
            return controll

    def delete(self, id):
        conn_create = self.conectar()
        cursor = conn_create.cursor()
        controll = False
        try:
            cursor.execute("DELETE FROM USER WHERE ID = {};".format(id))
            conn_create.commit()
            logging.info('Data deleted with sucess-->In: {}'.format(self.hour_now()[0]))
            controll = True
        except:
            logging.error('Error to delete from database-->In: {}'.format(self.hour_now()[0]))
        finally:
            conn_create.close()
            return controll

    @classmethod
    def hour_now(self):
        d_h = datetime.datetime.now()
        hora = d_h.strftime('%H:%M:%S')
        data = d_h.strftime('%d/%m/%y')
        return [data, hora]

if __name__ == '__main__':
    
    a = BD()
    a.insert(['Bruna oliveria', 25])
    a.insert(['Bia ferreia', 21])
    a.insert(['Regis santo', 23])
    a.insert(['KKKKKK', 99])
    print(a.select())

