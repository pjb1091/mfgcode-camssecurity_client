import json
import logging
from psycopg2 import connect as pg_connect , sql

class dbcams:

    option = 0

    def __int__(self, option):
        self.conn = None
        self.cursor = None
        self.option = option

    def __call__(self, func):
        def wraps(*args, **kwargs):
            try:
                data = kwargs['data']
                option = kwargs['option']
                try:
                    f = open("conf/database.json", "r")
                    line = json.loads(f.read())
                    f.close()
                    host = line["host"]
                    port = line["port"]
                    user = line["user"]
                    password = line["password"]
                    if option == 0:
                        dbname = line["dbname"]
                    elif option == 1:
                        dbname = line["template"]
                    else:
                        dbname = line["dbname"]
                    try:
                        self.conn = pg_connect(
                            "dbname='{}'"
                            "user='{}'"
                            "password='{}'"
                            "host='{}'"
                            "port='{}'".format(
                                dbname,
                                user,
                                password,
                                host,
                                port
                            )
                        )
                        self.cursor = self.conn.cursor()
                        x = func(*args, {'conn': self.conn, 'cursor': self.cursor, 'data': data})
                        self.cursor.close()
                        self.conn.close()
                        return x
                    except Exception as e:
                        return self.__error(display='Connect CAMS DB', e=e)
                except Exception as e:
                    return self.__error(display='Read JSON Connect CAMS DB', e=e)
            except Exception as e:
                return self.__error(display='Variable requerid : (data={}, option=0) <= Is most important', e=e)
            print(kwargs)
        return wraps

    def __error(self,response=True, display='', e=Exception, data=None):
        msj = '{} - {}'.format(display,e)
        return {'error': response, 'msj': msj, 'data': data}



