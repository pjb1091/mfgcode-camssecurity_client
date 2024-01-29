from flask import Flask
from func.hikvision import Hickvision
import json

app = Flask(__name__)

@app.route('/nvr/database/create')
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
