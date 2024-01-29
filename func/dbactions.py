
### --------------------------------------------
### FIRST CONECTION WITH DATABASE
### --------------------------------------------
@dbcams()
def rev_conn_template(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        curs.execute("SELECT now();")
        result = curs.fetchone()
        date = result[0].strftime("%m/%d/%Y, %H:%M:%S")
        return {'error': False, 'msj': 'Great !! Conection to template1 db is OK', 'data': {'date': date}}
    except Exception as e:
        print(e)
        return {'error': True, 'msj': "You can't access for template 1 - ".format(e), 'data': {}}

@dbcams()
def rev_conn_cams(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        curs.execute("SELECT now();")
        result = curs.fetchone()
        date = result[0].strftime("%m/%d/%Y, %H:%M:%S")
        return {'error': False, 'msj': 'Great !! Conection to cams db is OK', 'data': {'date': date}}
    except Exception as e:
        return {'error': True, 'msj': "You can't access for cams db - ".format(e), 'data': {}}

@dbcams()
def create_db_cams(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        conn.autocommit = True
        create_database_cmd = sql.SQL('CREATE DATABASE cams;')
        create_privileges_cmd = sql.SQL('GRANT ALL PRIVILEGES ON DATABASE cams TO cams;')
        curs.execute(create_database_cmd)
        curs.execute(create_privileges_cmd)
        return {'error': False, 'msj': 'Great !! Database es create', 'data': {}}
    except Exception as e:
        print(e)
        return {'error': False, 'msj': 'Dont create database cam - {}'.format(e), 'data': {}}

@dbcams()
def rev_tables_cam_schema(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        curs.execute("SELECT count(id) FROM devices;")
        result = curs.fetchone()[0]
        return {'error': False, 'msj': 'Great !! the enviromet correct', 'data': {'date': result}}
    except Exception as e:
        return {'error': True, 'msj': "Tables schema doesn't exist - ".format(e), 'data': {}}

@dbcams()
def create_schemas_cams(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        conn.autocommit = True
        f = open("conf/db.sql", "r")
        statement = f.read()
        f.close()
        create_tables_cmd = sql.SQL(statement)
        curs.execute(create_tables_cmd)
        return {'error': False, 'msj': 'Great !! Schemas has create for cam', 'data': {}}
    except Exception as e:
        return {'error': False, 'msj': 'Dont create schemas for cam - {}'.format(e), 'data': {}}

### --------------------------------------------
### DB CONEWCTIONS
### --------------------------------------------
@dbcams()
def insert_device(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    fields = ''
    values = ''
    for val in data:
        fields = "{}{}, ".format(fields, val)
        values = "{}{}, ".format(values, data[val])
    fields = fields[0:-2]
    values = values[0:-2]
    try:
        conn.autocommit = True
        query = "INSERT INTO cams.public.devices({}) values({});".format(fields, values)
        curs.execute(query)
        response = {
            'error': False,
            'msj': "Success Insert Device DB",
            'dns': data['dns'],
            'marca': data['marca'],
            'path_dns': data['path_dns'],
            'path_dns_init': data['path_dns_init'],
            'path_dns_cams': data['path_dns_cams'],
            'path_dns_stream': data['path_dns_stream'],
            'path_dns_config': data['path_dns_config']
        }
        return {'error': False, 'msj': 'Great !! your device was added', 'data': response}
    except Exception as e:
        return {'error': True, 'msj': "Insert Device DB - {}".format(e),'data': {}}

@dbcams()
def save_channels(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        conn.autocommit = True
        curs.execute("SELECT id FROM devices WHERE dns = '{}';".format(data['dns']))
        id = curs.fetchone()[0]
        channels = []
        ids_channels = []
        # Insert channels
        for insert in data['node']:
            insert_query = """insert into channels (cam_id, input_port, video_input_enabled, name, video_format, state_info, channel, device_id, dns, create_date, write_date, create_uid, write_uid)
            values ({}, {}, {}, '{}', '{}', '{}', {}, {}, '{}', '{}', '{}',{},{});""".format(
                insert['cam_id'],
                insert['input_port'],
                insert['video_input_enabled'],
                insert['name'],
                insert['video_format'],
                insert['state_info'],
                insert['channel'],
                id,
                data['dns'],
                insert['create_date'],
                insert['write_date'],
                insert['create_uid'],
                insert['write_uid'],
            )
            curs.execute(insert_query)
            channels.append(insert['channel'])
            ids_channels.append(insert['cam_id'])
        datas = {
            'dns': data['dns'],
            'id_device': id,
            'channels': channels,
            'ids_channels': ids_channels
        }
        return {'error': False, 'msj': 'Save channels for "{}"'.format(data["dns"]), 'data': datas}
    except Exception as e:
        return {'error': True, 'msj': "Don't save channels for {} - {}".format(data['dns'], e),'data': {}}

@dbcams()
def get_channel_from_deviceid_id(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        curs.execute("SELECT channel FROM channels WHERE cam_id = {} AND device_id = {};".format(
            data['cam_id'],
            data['device_id']
        ))
        result = curs.fetchaaone()[0]
        return {'error': False, 'msj': 'Great !! consult terminated', 'data': {'channel': result}}
    except Exception as e:
        return {'error': True, 'msj': "We dont get info - ".format(e), 'data': {}}

@dbcams()
def get_idchannel_from_deviceid_id(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        curs.execute("SELECT id FROM channels WHERE cam_id = {} AND device_id = {};".format(
            data['cam_id'],
            data['device_id']
        ))
        result = curs.fetchone()[0]
        return {'error': False, 'msj': 'Great !! consult terminated', 'data': {'id': result}}
    except Exception as e:
        return {'error': True, 'msj': "We dont get info - ".format(e), 'data': {}}

@dbcams()
def get_campath_from_deviceid(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        curs.execute("SELECT path_dns_cams FROM channels WHERE id = {};".format(
            data['device_id']
        ))
        result = curs.fetchone()[0]
        return {'error': False, 'msj': 'Great !! consult terminated', 'data': {'id': result}}
    except Exception as e:
        return {'error': True, 'msj': "We dont get info - ".format(e), 'data': {}}

@dbcams()
def insert_channel_weight_info(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        conn.autocommit = True
        query = """INSERT INTO cams.public.channels_weight_info(weight, video_input_enabled, state_info, state_procces_pil, dns, channel_id, device_id, create_date, write_date, create_uid, write_uid) values({}, {}, '{}', {}, '{}', {}, {}, '{}', '{}', {}, {}) RETURNING id;""".format(
            data['weight'],
            data['video_input_enabled'],
            data['state_info'],
            data['state_procces_pil'],
            data['dns'],
            data['channel_id'],
            data['device_id'],
            data['create_date'],
            data['write_date'],
            data['create_uid'],
            data['write_uid'],
        )
        curs.execute(query)
        res = curs.fetchone()
        last_inserted_id = res[0]
        response = {
            'error': False,
            'msj': "Success Insert Device DB",
            'id': last_inserted_id,
        }
        return {'error': False, 'msj': 'Great !! your device was added', 'data': response}
    except Exception as e:
        return {'error': True, 'msj': "Insert Device DB - {}".format(e),'data': {}}

@dbcams()
def get_channel_weight_info_from_id(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        query = """SELECT 
                        * 
                    FROM channels_weight_info 
                    WHERE 
                        id = {};""".format(data["id"]);
        curs.execute(query)
        response1 = curs.fetchone()
        weight = response1[1]
        date = response1[9]
        video_enabled = response1[2]
        state_info = response1[3]
        state_process_pil = response1[4]
        query = """SELECT 
                        * 
                    FROM channels 
                    WHERE 
                        cam_id = {} 
                        and device_id = {};""".format(response1[6],response1[7])
        curs.execute(query)
        response2 = curs.fetchone()
        video_enabled2 = response2[3]
        state_info2 = response2[6]
        query = """SELECT
                case
                    when weight is null then
                        0
                    else
                        weight
                end weight,
                10.0::float8 porcent,
                write_date
            FROM
                channels_weight_info
            WHERE
                device_id = {}
                and channel_id = {}
                and video_input_enabled
                and state_procces_pil
            order by
                write_date desc
            limit 1;""".format(response1[7], response1[6])
        curs.execute(query)
        response3 = curs.fetchone()
        if response3:
            x_weight = response3[0]
            porcent = response3[1]
        else:
            x_weight = 0
            porcent = 0
        data = {
            'cw_weight': weight,
            'cw_date': date,
            'cw_video_enabled': video_enabled,
            'cw_state_info': state_info,
            'cw_state_process_pil': state_process_pil,
            'c_video_enabled': video_enabled2,
            'c_state_info': state_info2,
            'x_weight': x_weight,
            'x_porcent': porcent,
            'device_id': response1[7],
            'cam_id': response1[6]
        }
        return {'error': False, 'msj': 'Great !! your device was added', 'data': data}
    except Exception as e:
        return {'error': True, 'msj': "Insert Device DB - {}".format(e), 'data': {}}

@dbcams()
def get_channel_exception_from_ids_channel_device(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        query = "SELECT * FROM channel_exception WHERE channel_id = {} AND device_id = {} AND state = 'open';".format(
            data['channel_id'],
            data['device_id']
        )
        curs.execute(query)
        result = curs.fetchone()
        data = {
            'id': result[0],
            'report_id': result[1],
            'channel_id': result[2],
            'device_id': result[3],
            'state': result[4],
            'dns': result[5],
            'type': result[6],
            'create_date': result[7],
            'write_date': result[8],
            'create_uid': result[9],
            'write_uid': result[10],
        }
        return {'error': False, 'msj': 'Great !! consult terminated', 'data': data}
    except Exception as e:
        return {'error': True, 'msj': "We dont get info - ".format(e), 'data': {}}

@dbcams()
def update_fields_exception_from_id(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    fields_val = ''
    id_bool = True
    for val in data:
        if id_bool:
            id_bool = False
        else:
            if data[val]['type'] == 'string':
                fields_val = "{}{} = '{}', ".format(fields_val, val, data[val]['data'])
            elif data[val]['type'] == 'int':
                fields_val = "{}{} = {}, ".format(fields_val, val, data[val]['data'])
    fields_val = fields_val[0:-2]
    try:
        query = "UPDATE channel_exception SET {} WHERE id = {};".format(fields_val, data['id']['data'])
        curs.execute(query)
        conn.commit()
        response = curs.rowcount
        return {'error': False, 'msj': 'Great !! your device was added', 'data': response}
    except Exception as e:
        return {'error': True, 'msj': "Insert Device DB - {}".format(e), 'data': {}}


@dbcams()
def insert_channel_alert(*args):
    # ----- [FIRST ARGUMENTS] ----
    conn = args[0]['conn']
    curs = args[0]['cursor']
    data = args[0]['data']
    # ----- [YOUR CODE]
    try:
        conn.autocommit = True
        query = """insert into channel_alert (channel_id, device_id, state, dns, write_date, create_date, create_uid, write_uid, type) values({}, {}, '{}', '{}', '{}', '{}', {}, {}, '{}') RETURNING id;""".format(
            data['channel_id'],
            data['device_id'],
            data['state'],
            data['dns'],
            data['write_date'],
            data['create_date'],
            data['create_uid'],
            data['write_uid'],
            data['type'],
        )
        curs.execute(query)
        res = curs.fetchone()
        last_inserted_id = res[0]
        response = {
            'error': False,
            'msj': "Success Insert Device DB",
            'id': last_inserted_id,
        }
        return {'error': False, 'msj': 'Great !! your device was added', 'data': response}
    except Exception as e:
        return {'error': True, 'msj': "Insert Device DB - {}".format(e),'data': {}}
