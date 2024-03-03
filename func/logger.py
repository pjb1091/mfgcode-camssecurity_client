import logging
import urllib.request
import json

class logger:

    file = None
    named = None

    def __init__(self, file, named=None):
        self.file = file
        self.named = named

    def __call__(self, func):
        def wraps(*args, **kwargs):
            try:
                try:
                    if len(self.file) > 0:
                        log = self.__log(types="info", msj="__CALLBACK")
                        kwargs["log"] = log
                        x = func(*args, **kwargs)
                        try:
                            log = self.__log(msj=x, jsonData=True)
                        except Exception as e:
                            log = self.__log(msj=e, types="exception")
                        return x
                    else:
                        log = self.__log(msj='Need name log', types="critical")
                        return self.__error(display='Need name log')
                except Exception as e:
                    return self.__error(display='Dont open process file', e=e)
            except Exception as e:
                return self.__error(display='Dont open file', e=e)
        return wraps

    def __log(self, file=None, msj=None, types="info", printData=False, jsonData=False):
        if file == None:
            file = 'log/{}.log'.format(self.file)
        log_std_out = logging.FileHandler(filename=file, encoding='utf-8', mode='a')
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(user)-8s  %(clientip)-8s : %(fname)s : %(message)s')
        f = open("conf/access.json", "r")
        line = json.loads(f.read())
        fuser = line["user"]
        f.close()
        d = {'clientip': external_ip, 'user': fuser, 'fname': self.named}
        log_std_out.setFormatter(formatter)
        loggers = logging.getLogger('agent-cams')
        for hdl in loggers.handlers[:]:
            loggers.removeHandler(hdl)
        loggers.addHandler(log_std_out)
        loggers.setLevel(logging.DEBUG)
        if not jsonData:
            if types == "info":
                loggers.info(msg=msj, extra=d)
            elif types == "debug":
                loggers.debug(msj, extra=d)
            elif types == "error":
                loggers.error(msj, extra=d)
            elif types == "warning":
                loggers.warning(msj, extra=d)
            elif types == "critical":
                loggers.critical(msj, extra=d)
            elif types == "exception":
                loggers.exception(msj, extra=d)
        else:
            if not printData:
                msj_out = msj["msj"]
            else:
                msj_out = "'''{}''' // ---> ({})".format(msj["msj"], msj["data"])
            if msj["error"]:
                loggers.error(msj_out, extra=d)
            else:
                loggers.info(msj_out, extra=d)
        return loggers

    def __error(self,response=True, display='', e=Exception, data=None):
        msj = '{} - {}'.format(display,e)
        return {'error': response, 'msj': msj, 'data': data}




