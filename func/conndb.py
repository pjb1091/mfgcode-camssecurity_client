import json
from psycopg2 import connect as pg_connect

class dbcams:
    """
    The class is the base for connection with the postgres database
    for client camssecurity.

    :parameter: option <integer>
    :return: conn <psycopg2.connect>
    """
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
                    # Choice de DB or Template connection / default DB Name
                    if option == 0:
                        dbname = line["dbname"]
                    elif option == 1:
                        dbname = line["template"]
                    else:
                        dbname = line["dbname"]
                    # Try connection method by psycopg2
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
                        # Run principal function son node
                        x = func(*args, {'conn': self.conn, 'cursor': self.cursor, 'data': data})
                        # Close connection and cursor
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

    def __error(self, response=True, display='', e=Exception, data=None):
        msj = '{} - {}'.format(display, e)
        return {'error': response, 'msj': msj, 'data': data}