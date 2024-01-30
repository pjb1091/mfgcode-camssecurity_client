import logging
class logger():

    def __int__(self):
        logging.basicConfig(
            d = {'clientip':'10.150.4.192'}
            format='[%(levelname)s] %(process)d_%(processName)s %(asctime)s %(filename)s %(funcName)s %(module)s %(clientip)-15s %(user)-8s %(message)s %(msecs)d %(created)f',
            datefmt='%m/%d/%Y_%I:%M:%S_%p', level=logging.DEBUG, extra=d)

    def __call__(self, func):
        def wraps(*args, **kwargs):
            try:
                print("print log")
                x = func(*args, **kwargs)
                return  x
            except Exception as e:
                return self.__error(display='Dont open file', e=e)
        return wraps

    def __error(self,response=True, display='', e=Exception, data=None):
        msj = '{} - {}'.format(display,e)
        return {'error': response, 'msj': msj, 'data': data}



