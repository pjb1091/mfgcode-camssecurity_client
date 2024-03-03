import os

from flask import Flask, redirect, url_for, request
from func.hikvision import Hickvision
from func.licence import Licence
import json

app = Flask(__name__)

#####################################################  [ CHECK ]
@app.route('/apiv.1/check', methods=["POST","GET"])
def check():
    return (""""
        ================================================================================ 
         
        🅰🅶🅴🅽🆃-🅲🅰🅼
        
        ================================================================================ 

        Menu for check:
        
        1.- ping : Review start app
                security: NO
                endpoint: /apiv.1/check/ping
                
        2.- files : Review important files
                security: NO
                endpoint: /apiv.1/check/files
    """)
@app.route('/apiv.1/check/ping', methods=["POST","GET"])
def ping():
    """
    Check function from response client
    :return: {}
    """
    if request.method == 'POST':
        return {'error':False, "msj": "Test request app - Agent [METHOD:POST] - OK!!"}
    elif request.method == 'GET':
        return {'error': False, "msj": "Test request app - Agent [METHOD:GET] - OK!!"}

@app.route('/apiv.1/check/files', methods=["POST","GET"])
def files_check():
    """
    Check inportant files for opertion
    :return: {}
    """
    if os.path.isfile('conf/database.json') and os.path.isfile('conf/access.json'):
        return {'error': False, "msj": "Test request app - Agent [METHOD:GET] - OK!!"}
    else:
        return ({'error': True, "msj": "FAIL open impotant files"}, 500)


#####################################################  [ NVR ]

@app.route('/apiv.1/nvr', methods=["POST", "GET"])
def nvr():
    return (""""
        ================================================================================ 

        🅰🅶🅴🅽🆃-🅲🅰🅼

        ================================================================================ 

        Menu for nvr:

        1.- accessdb : Check database connection from json params
                security: NO
                endpoint: /apiv.1/nvr/accessdb

        2.- accessplataform : Check licence and status record company from main sysmtem Cam-Security
                security: NO
                endpoint: /apiv.1/nvr/accessplataform
        
        3.- hikvision: Api conection HikVision (Integrated)
                security: SI
                endpoint: /apiv.1/nvr/hikvision
    """)

@app.route('/apiv.1/nvr/accessdb', methods=["POST", "GET"])
def accesdb():
    nvr = Hickvision()
    response = nvr.init_check_database()
    return response


@app.route('/apiv.1/nvr/accessplataform', methods=["POST", "GET"])
def accessplataform():
    licence = Licence()
    response = licence.init_check_licence()
    return response


@app.route('/api/nvr/database/create')
def create_nvr():
    nvr = Hickvision()
    response = nvr.init_enviroment()
    if response is None:
        response = nvr.init_enviroment()
    return response

@app.route('/nvr/append')
def append_nvr():
    nvr = Hickvision()
    response = nvr.new_device('hikvision', 'http://10.150.24.106/', 'admin', 'admin2017', 'Thermofluidos', 'THRMO24',
                              'normal', 1)
    if not response['error']:
        print(response["data"])
        print("Adding Path ...")
        dns = nvr.clean_str(response["data"]["dns"])
        marca = nvr.clean_str(response["data"]["marca"])
        path_dns = nvr.clean_str(response["data"]["path_dns"])
        path_dns_init = nvr.clean_str(response["data"]["path_dns_init"])
        path_dns_cams = nvr.clean_str(response["data"]["path_dns_cams"])
        path_dns_stream = nvr.clean_str(response["data"]["path_dns_stream"])
        path_dns_config = nvr.clean_str(response["data"]["path_dns_config"])
        print(dns)
        print(marca)
        print(path_dns)
        print(path_dns_init)
        print(path_dns_cams)
        print(path_dns_stream)
        print(path_dns_config)
        nvr.create_path()
        channel = nvr.get_channels_conf(path_dns_init, marca, dns)
        if not channel['error']:
            data = channel['data']
            print(data)
            print("Create dir channels")
            nvr.create_paths_channels(data['channels'], path_dns_cams, marca, data['id_device'])
            nvr.create_paths_channels(data['channels'], path_dns_config, marca, data['id_device'])
            print("Checking Channels ...")
            check_channel = nvr.check_channel(data['dns'], data['id_device'], data['ids_channels'], path_dns_config,
                                              marca, path_dns_cams)
            if check_channel:
                print("Device add complete ...")
                print("Finish ...")
            else:
                print("There are some problems ...")
        else:
            print(channel)
    else:
        print(response)




if __name__ == '__main__':
    app.run()
