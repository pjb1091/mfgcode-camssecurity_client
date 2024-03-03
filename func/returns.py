class returns:
    """
    The class is help to return correct code http request

    :return: this return + request code
    """

    def __call__(self, func):
        def wraps(*args, **kwargs):
            try:
                x = func(*args, **kwargs)
                if x["error"]:
                    return (x, 500)
                else:
                    return (x, 200)
            except Exception as e:
                return self.__error(display='Fatal error for return request', e=e)
        return wraps

    def __error(self, response=True, display='', e=Exception, data=None):
        msj = '{} - {}'.format(display, e)
        return {'error': response, 'msj': msj, 'data': data}