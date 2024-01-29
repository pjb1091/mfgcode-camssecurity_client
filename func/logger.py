import json
from psycopg2 import connect as pg_connect , sql

class logger:

    option = "static/logger.file"

    def __int__(self, file=option):
        self.option = file

    def __call__(self, func):
        def wraps(*args, **kwargs):
            try:
                f = open(self.option, "a")
                x = func(*args, **kwargs)
                return  x
            except Exception as e:
                return self.__error(display='Dont open file', e=e)
        return wraps

    def __error(self,response=True, display='', e=Exception, data=None):
        msj = '{} - {}'.format(display,e)
        return {'error': response, 'msj': msj, 'data': data}



