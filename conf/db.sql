
CREATE TABLE  cams.public.devices (
	id serial4 NOT NULL,
	host varchar NOT NULL,
	password varchar NOT NULL,
	"user" varchar NOT NULL,
	name varchar NOT NULL,
	dns varchar NOT NULL constraint pk_dns_unique unique,
	devicename varchar  NULL,
	deviceid varchar  NULL,
	model varchar  NULL,
	serialnumber varchar  NULL,
	macaddress varchar  NULL,
	firmwareversion varchar  NULL,
	devicetype varchar  NULL,
	hardwareversion varchar  NULL,
	marca varchar NOT NULL,
	path_dns varchar NULL,
	path_dns_init varchar NULL,
	path_dns_cams varchar NULL,
	path_dns_stream varchar NULL,
	path_dns_config varchar NULL,
	write_date timestamp NULL,
	create_date timestamp NULL,
	create_uid int4 NULL,
	write_uid int4 NULL,
	CONSTRAINT devices_pk PRIMARY KEY (id)
);
 alter table cams.public.devices
   add constraint pk_dns_unique
   unique (dns);

CREATE TABLE  cams.public.channels (
	id serial4 NOT NULL,
    cam_id int8 NULL,
    input_port int8 NULL,
    video_input_enabled boolean NULL,
    name varchar NULL,
    video_format varchar NULL,
    state_info varchar NULL,
    state_cams varchar default 'NOT_CONFIRMED',
    channel int8 NULL,
    device_id INT REFERENCES devices(id),
    dns varchar NULL,
    write_date timestamp NULL,
	create_date timestamp NULL,
	create_uid int4 NULL,
	write_uid int4 NULL,
    CONSTRAINT channels_pk PRIMARY KEY (id)
);

CREATE TABLE  cams.public.channels_weight_info (
	id serial4 NOT NULL,
    weight int8 NULL,
	video_input_enabled boolean NULL,
	state_info varchar NULL,
	state_procces_pil boolean NULL,
	dns varchar NOT NULL,
    channel_id INT REFERENCES channels(id),
    device_id INT REFERENCES devices(id),
    write_date timestamp NULL,
	create_date timestamp NULL,
	create_uid int4 NULL,
	write_uid int4 NULL,
    CONSTRAINT pk_channels_weight_info PRIMARY KEY (id)
);

CREATE TABLE  cams.public.channel_exception(
	id serial4 NOT NULL,
    report_id INT REFERENCES report(id),
    channel_id INT REFERENCES channels(id),
    device_id INT REFERENCES devices(id),
    state varchar NULL,
    dns varchar NULL,
    type varchar NULL,
    write_date timestamp NULL,
	create_date timestamp NULL,
	create_uid int4 NULL,
	write_uid int4 NULL,
    CONSTRAINT pk_channel_exception PRIMARY KEY (id)
);

CREATE TABLE  cams.public.channel_alert(
	id serial4 NOT NULL,
    channel_id INT REFERENCES channels(id),
    device_id INT REFERENCES devices(id),
    state varchar NULL,
    dns varchar NULL,
    type varchar NULL,
    write_date timestamp NULL,
	create_date timestamp NULL,
	create_uid int4 NULL,
	write_uid int4 NULL,
    CONSTRAINT pk_channel_alert PRIMARY KEY (id)
);

CREATE TABLE  cams.public.report(
	id serial4 NOT NULL,
    CONSTRAINT pk_report PRIMARY KEY (id)
);

