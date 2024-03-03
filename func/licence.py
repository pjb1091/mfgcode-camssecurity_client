from func.returns import returns
import os


class Licence:

    def __init__(self):
        self.parent_dir = '{}/static/'.format(os.getcwd())

    @returns()
    def init_check_licence(self):
        response = {"error": False, "msj": "No yet to do", "data": None}
        return response



