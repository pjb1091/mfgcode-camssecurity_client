from hikvisionapi import Client, AsyncClient
import pytesseract
from PIL import Image, ImageEnhance,ImageOps
from func.returns import returns
import func.dbactions as db
import time
import os
import datetime
import glob
import json
import xmltodict


class Hickvision:

    device = None
    device_info = {}
    type = None
    marca = None
    host = None
    user = None
    password = None
    name = None
    user_write = None
    dns = None
    path_dns = ""
    path_dns_init = ""
    path_dns_cams = ""
    path_dns_stream = ""
    path_dns_config = ""
    type = 'normal'
    passkey = "0xi@23"

    def __init__(self):
        self.parent_dir = '{}/static/'.format(os.getcwd())


    @returns()
    def init_check_database(self):
        response = db.rev_conn_template(data={}, option=1)
        return response

    def init_enviroment(self):
        func = db.rev_conn_template(data={}, option=1)
        if not func['error']:
            print("Adding device ...")
            func2 = db.rev_conn_cams(data={}, option=0)
            if not func2['error']:
                print("Continue adding...")
                func4 = db.rev_tables_cam_schema(data={}, option=0)
                if not func4['error']:
                    return func4
                else:
                    print("Adding schemas..")
                    func5 = db.create_schemas_cams(data={}, option=0)
                    time.sleep(10)
                    if not func5['error']:
                        self.init_enviroment()
                    else:
                        return func5
            else:
                print("Creatting database..")
                if 'database "cams" does not exist' in func2['msj']:
                    func3 = db.create_db_cams(data={}, option=1)
                    time.sleep(5)
                    if not func3['error']:
                        self.init_enviroment()
                    else:
                        return func3
                else:
                    return func2
        else:
            return func

    def new_device(self, marca, host, user, password, name, dns, type='normal',user_w=1):
        self.type = type
        self.marca = marca
        self.host = host
        self.user = user
        self.password = password
        self.name = name
        self.dns = dns
        self.user_write = user_w
        path_init = "INIT"
        path_cameras = "CAMS"
        path_stream = "STREAMING"
        path_config = "CONF"
        principal_directory = self.dns
        if marca == 'hikvision':
            try:
                self.device = Client(self.host, self.user, self.password)
                self.device_info = self.device.System.deviceInfo(method='get')
                if (self.device._check_session):
                    for x in self.device_info['DeviceInfo']:
                        if x == 'deviceName':
                            devicename = self.device_info['DeviceInfo'][x]
                        elif x == 'deviceID':
                            deviceid = self.device_info['DeviceInfo'][x]
                        elif x == 'model':
                            model = self.device_info['DeviceInfo'][x]
                        elif x == 'serialNumber':
                            serialnumber = self.device_info['DeviceInfo'][x]
                        elif x == 'macAddress':
                            macaddress = self.device_info['DeviceInfo'][x]
                        elif x == 'firmwareVersion':
                            firmwareversion = self.device_info['DeviceInfo'][x]
                        elif x == 'deviceType':
                            devicetype = self.device_info['DeviceInfo'][x]
                        elif x == 'hardwareVersion':
                            hardwareversion = self.device_info['DeviceInfo'][x]
                    self.path_dns = "{}{}".format(self.parent_dir, principal_directory)
                    self.path_dns_init = "{}/{}".format(self.path_dns, path_init)
                    self.path_dns_cams = "{}/{}".format(self.path_dns, path_cameras)
                    self.path_dns_stream = "{}/{}".format(self.path_dns, path_stream)
                    self.path_dns_config = "{}/{}".format(self.path_dns, path_config)
                    data = {
                        'host': "'{}'".format(self.host),
                        'password': "'{}'".format(self.password),
                        '"user"': "'{}'".format(self.user),
                        'name': "'{}'".format(self.name),
                        'dns': "'{}'".format(self.dns),
                        'devicename': "'{}'".format(devicename),
                        'deviceid': "'{}'".format(deviceid),
                        'model': "'{}'".format(model),
                        'serialnumber': "'{}'".format(serialnumber),
                        'macaddress': "'{}'".format(macaddress),
                        'firmwareversion': "'{}'".format(firmwareversion),
                        'devicetype': "'{}'".format(devicetype),
                        'hardwareversion': "'{}'".format(hardwareversion),
                        'marca': "'{}'".format(self.marca),
                        'path_dns': "'{}'".format(self.path_dns),
                        'path_dns_init': "'{}'".format(self.path_dns_init),
                        'path_dns_cams': "'{}'".format(self.path_dns_cams),
                        'path_dns_stream': "'{}'".format(self.path_dns_stream),
                        'path_dns_config': "'{}'".format(self.path_dns_config),
                        'write_date': "'{}'".format(self.today()),
                        'create_date': "'{}'".format(self.today()),
                        'create_uid': 1,
                        'write_uid': 1,
                    }
                    return db.insert_device(data=data, option=0)
                else:
                    return False
            except Exception as e:
                return {'error': True, 'msj': 'Not conection host - {}'.format(e), 'data': {}}
        else:
            return False

    def create_path(self):
        os.mkdir(self.path_dns)
        os.mkdir(self.path_dns_init)
        os.mkdir(self.path_dns_cams)
        os.mkdir(self.path_dns_stream)
        os.mkdir(self.path_dns_config)
        return True

    def today(self):
        return datetime.datetime.now()
    def create_paths_channels(self,channels, path, marca, device_id):
        for i in channels:
            complete_path = '{}/{}_{}_{}'.format(path,marca,device_id,i)
            os.mkdir(complete_path)
        return True

    def get_device(self):
        return self.device

    def set_device(self,device):
        self.device = device

    def get_deviceinfo(self):
        return self.device_info

    def get_channels_conf(self, path, marca, dns):
        if marca == 'hikvision':
            info_cams = self.device.System.Video.inputs.channels(method='get', type='opaque_data')
            dict = self.get(info_cams)
            cams = []
            start = 0
            for i in glob.glob('{}/*'.format(path)):
                os.unlink(i)
            for cam in dict['VideoInputChannelList']['VideoInputChannel']:
                channel = 0
                for i in range(start, ((int(cam['inputPort'])*100) + 10), 100):
                    deletex = False
                    channel_cam = self.device.Streaming.channels[i].picture(method='get', type='opaque_data')
                    with open('{}/{}_picture_{}.jpg'.format(path, dns, i), 'wb') as f:
                        for chunk in channel_cam.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                if 'Device Busy' in str(chunk) or 'Invalid XML Content' in str(chunk):
                                    deletex = True
                    time.sleep(1)
                    if deletex:
                        deletex = False
                        os.unlink('{}/{}_picture_{}.jpg'.format(path, dns, i))
                    else:
                        channel = i
                cams.append(
                    {
                        'cam_id': cam['id'],
                        'input_port': cam['inputPort'],
                        'video_input_enabled': cam['videoInputEnabled'],
                        'name': cam['name'],
                        'video_format': cam['videoFormat'],
                        'state_info': cam['resDesc'],
                        'channel': channel,
                        'write_uid': self.user_write,
                        'create_uid': self.user_write,
                        'write_date': self.today(),
                        'create_date': self.today()
                    }
                )
                start = start + 100
            data = {
                'dns': dns,
                'node': cams
            }
            response = db.save_channels(data=data, option=0)
            return response
        else:
            return False

    def check_channel(self, dns, id_device, channels, path, marca, path_cams):
        if marca == 'hikvision':
            for l in channels:
                response = self.device.System.Video.inputs.channels[l](method='get', type='opaque_data')
                response = self.get(response)['VideoInputChannel']
                data = {
                    'cam_id': l,
                    'device_id': id_device
                }
                channel = db.get_channel_from_deviceid_id(data=data, option=0)
                if not channel['error']:
                    channel = channel['data']['channel']
                    dir_current = '{}_{}_{}'.format(marca,id_device,channel)
                    path_pick_1 = '{}/{}/check_picture_A_{}.jpg'.format(path,dir_current, l)
                    path_pick_pil_1 = '{}/{}/check_process_picture_B_{}.jpg'.format(path, dir_current, l)
                    cam_info = self.device.Streaming.channels[channel].picture(method='get', type='opaque_data')
                    with open(path_pick_1, 'wb') as f:
                        for chunk in cam_info.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                if 'Device Busy' in str(chunk) or 'Invalid XML Content' in str(chunk):
                                    print("Warning")
                    time.sleep(1)
                    image = Image.open(path_pick_1).convert("L")
                    contrast = ImageEnhance.Contrast(image)
                    image = contrast.enhance(2)
                    image = image.convert("RGB")
                    bits = image.getdata()
                    new_image = []
                    for item in bits:
                        if item[0] in range(0, 201):
                            new_image.append((0, 0, 0))
                        else:
                            new_image.append(item)
                    image.putdata(new_image)
                    image = ImageOps.invert(image)
                    nxd = 0
                    for i in range(1, image.size[0]):
                        for j in range(1, image.size[1]):
                            pix = image.getpixel((i,j))
                            sum = pix[0] + pix[1] + pix[2]
                        nxd = nxd + sum
                    image.save(path_pick_pil_1, quality=95)
                    text = pytesseract.image_to_string(image, lang='eng')
                    if "NO VIDEO" in text:
                        state = False
                    else:
                        state = True
                    data = {
                        'weight': nxd,
                        'video_input_enabled': response['videoInputEnabled'],
                        'state_info': response['resDesc'],
                        'state_procces_pil': state,
                        'dns': dns,
                        'channel_id': l,
                        'device_id': id_device,
                        'create_date': self.today(),
                        'write_date': self.today(),
                        'create_uid': self.user_write,
                        'write_uid': self.user_write,
                    }
                    response = db.insert_channel_weight_info(data=data, option=0)
                    if not response['error']:
                        print("Review info per create alert ...")
                        data = {'id': response['data']['id']}
                        response = db.get_channel_weight_info_from_id(data=data, option=0)
                        data = response['data']
                        cw_weight = data['cw_weight']
                        cw_date = data['cw_date']
                        cw_video_enabled = data['cw_video_enabled']
                        cw_state_info = data['cw_state_info']
                        cw_state_process_pil = data['cw_state_process_pil']
                        c_video_enabled = data['c_video_enabled']
                        c_state_info = data['c_state_info']
                        x_weight = data['x_weight']
                        x_porcent = data['x_porcent']
                        device_id = data['device_id']
                        cam_id = data['cam_id']
                        if c_video_enabled and (c_video_enabled == cw_video_enabled):
                            if c_state_info == "NO VIDEO":
                                response = "ERROR NO VIDEO FROM API"
                            elif c_state_info != "NO VIDEO" and (cw_state_info == c_state_info):
                                if cw_state_process_pil:
                                    procent_real = ((float(x_porcent)/100) * float(x_weight))
                                    limit_super = float(x_weight) + float(procent_real)
                                    limit_minus = float(x_weight) - float(procent_real)
                                    if cw_weight < limit_super and cw_weight > limit_minus:
                                        response = "OK"
                                    else:
                                        response = "POSSIBLE CHANNEL OBSTRUCTION"
                                else:
                                    response = "ERROR NO VIDEO FROM IMAGE REVIEW"
                            elif c_state_info != "NO VIDEO" and (cw_state_info != c_state_info):
                                if cw_state_process_pil:
                                    response = "DETECTED CHANNEL UP"
                                else:
                                    response = "ERROR CHANGE TO NO VIDEO"
                            else:
                                response = "ERROR NOT DOCUMENT"
                        else:
                            response = "ERROR VIDEO CLOSED CHANNEL"
                        if response == "OK":
                            self.get_image_to_channel(20, path_cams, marca, id_device, cam_id)
                        else:
                            data = {
                                'device_id': device_id,
                                'cam_id': cam_id
                            }
                            response1 = db.get_idchannel_from_deviceid_id(data=data,option=0)
                            channel_id = response1['data']['id']
                            data = {
                                'channel_id': channel_id,
                                'device_id': device_id
                            }
                            response2 = db.get_channel_exception_from_ids_channel_device(data=data, option=0)
                            if response2['data']:
                                print("Existe una excepcion abierta...")
                                data = {
                                    'id': {'data': response2['data']['id'], 'type': 'int'},
                                    'write_date': {'data': self.today(), 'type': 'string'},
                                    'write_uid': {'data': self.user_write, 'type': 'int'},
                                }
                                response3 = db.update_fields_exception_from_id(data=data, option=0)
                                if not response3['error']:
                                    if response3['data']:
                                        print(response)
                                        if response2['data']['type'] == "DETECTED CHANNEL UP":
                                            data = {
                                                'channel_id': channel_id,
                                                'device_id': device_id,
                                                'state': 'open',
                                                'dns': dns,
                                                'write_date': self.today(),
                                                'create_date': self.today(),
                                                'create_uid': self.user_write,
                                                'write_uid': self.user_write,
                                                'type': 'ERROR NO DETECTED'
                                            }
                                            if response == "POSSIBLE CHANNEL OBSTRUCTION":
                                                data['type'] = "POSSIBLE CHANNEL OBSTRUCTION"
                                            elif response == "DETECTED CHANNEL UP":
                                                data['type'] = "DETECTED CHANNEL UP"
                                            elif response == "ERROR NO VIDEO FROM API":
                                                data['type'] = "ERROR NO VIDEO FROM API"
                                            elif response == "ERROR NOT DOCUMENT":
                                                data['type'] = "ERROR NOT DOCUMENT"
                                            elif response == "ERROR VIDEO CLOSED CHANNEL":
                                                data['type'] = "ERROR VIDEO CLOSED CHANNEL"
                                            elif response == "ERROR NO VIDEO FROM IMAGE REVIEW":
                                                data['type'] = "ERROR NO VIDEO FROM IMAGE REVIEW"
                                            elif response == "ERROR CHANGE TO NO VIDEO":
                                                data['type'] = "ERROR CHANGE TO NO VIDEO"
                                            print("Se crea alerta [1]...")
                                            response4 = db.insert_channel_alert(data=data, option=0)
                                            if response4['error']:
                                                return False
                                            else:
                                                id = response4['data']['id']
                                                print("Se ha creado alerta {}...".format(id))
                                        else:
                                            print("Re actualizarón fechas de excepción...")
                                            print("Nada mas para hacer...")
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                data = {
                                    'channel_id': channel_id,
                                    'device_id': device_id,
                                    'state': 'open',
                                    'dns': dns,
                                    'write_date': self.today(),
                                    'create_date': self.today(),
                                    'create_uid': self.user_write,
                                    'write_uid': self.user_write,
                                    'type': 'ERROR NO DETECTED'
                                }
                                if response == "POSSIBLE CHANNEL OBSTRUCTION":
                                    data['type'] = "POSSIBLE CHANNEL OBSTRUCTION"
                                elif response == "DETECTED CHANNEL UP":
                                    data['type'] = "DETECTED CHANNEL UP"
                                elif response == "ERROR NO VIDEO FROM API":
                                    data['type'] = "ERROR NO VIDEO FROM API"
                                elif response == "ERROR NOT DOCUMENT":
                                    data['type'] = "ERROR NOT DOCUMENT"
                                elif response == "ERROR VIDEO CLOSED CHANNEL":
                                    data['type'] = "ERROR VIDEO CLOSED CHANNEL"
                                elif response == "ERROR NO VIDEO FROM IMAGE REVIEW":
                                    data['type'] = "ERROR NO VIDEO FROM IMAGE REVIEW"
                                elif response == "ERROR CHANGE TO NO VIDEO":
                                    data['type'] = "ERROR CHANGE TO NO VIDEO"
                                print("Se crea alerta [2]...")
                                response4 = db.insert_channel_alert(data=data, option=0)
                                if response4['error']:
                                    return False
                                else:
                                    id = response4['data']['id']
                                    print("Se ha creado alerta {}...".format(id))
                    else:
                        return False
                else:
                    return False
        else:
            return False
        return True

    def get_image_to_channel(self, qty, path_cams, marca, id_device, cam_id):
        dirx = "{}/{}_{}_{}/".format(path_cams, marca, id_device, (int(cam_id)*100))
        for n in range(1, (qty + 1)):
            img = "{}capture_{}.jpg".format(dirx, n)
            cam_info = self.device.Streaming.channels[(int(cam_id)*100)].picture(method='get', type='opaque_data')
            with open(img, 'wb') as f:
                for chunk in cam_info.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        if 'Device Busy' in str(chunk) or 'Invalid XML Content' in str(chunk):
                            print("Warning")
            time.sleep(1)
        return True

    def get(self,f):
            return json.loads(json.dumps(xmltodict.parse(f.content)))

    def clean_str(self,s):
            return str(s.replace('\'', ''))





#CREACIÓN DE AMBIENTES
# response = nvr.init_enviroment()
# if response is None:
#     response = nvr.init_enviroment()
# print(response)

#AGREGAR DISPOSITIVO
# response = nvr.new_device('hikvision', 'http://10.150.24.106/', 'admin', 'admin2017', 'Thermofluidos', 'THRMO24', 'normal', 1)
# if not response['error']:
#     print(response["data"])
#     print("Adding Path ...")
#     dns = nvr.clean_str(response["data"]["dns"])
#     marca = nvr.clean_str(response["data"]["marca"])
#     path_dns = nvr.clean_str(response["data"]["path_dns"])
#     path_dns_init = nvr.clean_str(response["data"]["path_dns_init"])
#     path_dns_cams = nvr.clean_str(response["data"]["path_dns_cams"])
#     path_dns_stream = nvr.clean_str(response["data"]["path_dns_stream"])
#     path_dns_config = nvr.clean_str(response["data"]["path_dns_config"])
#     print(dns)
#     print(marca)
#     print(path_dns)
#     print(path_dns_init)
#     print(path_dns_cams)
#     print(path_dns_stream)
#     print(path_dns_config)
#     nvr.create_path()
#     channel = nvr.get_channels_conf(path_dns_init, marca, dns)
#     if not channel['error']:
#         data = channel['data']
#         print(data)
#         print("Create dir channels")
#         nvr.create_paths_channels(data['channels'], path_dns_cams, marca, data['id_device'])
#         nvr.create_paths_channels(data['channels'], path_dns_config, marca, data['id_device'])
#         print("Checking Channels ...")
#         check_channel = nvr.check_channel(data['dns'], data['id_device'], data['ids_channels'], path_dns_config, marca, path_dns_cams)
#         if check_channel:
#             print("Device add complete ...")
#             print("Finish ...")
#         else:
#             print("There are some problems ...")
#     else:
#         print(channel)
# else:
#     print(response)
#     print("Checking Channels ...")
#     data = {'dns': 'THRMO23', 'id_device': 34,
#             'channels': [500],
#              'ids_channels':[5]}
#     path = '/mnt/c/Users/TI12R/Documents/Develop/Otros/hikvision/static/THRMO23/CONF'
#     path_cams = '/mnt/c/Users/TI12R/Documents/Develop/Otros/hikvision/static/THRMO23/CAMS'
#     marca = 'hikvision'
#     check_channel = nvr.check_channel(data['dns'], data['id_device'], data['ids_channels'], path, marca, path_cams)
#     print(check_channel)



