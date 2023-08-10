import json
import os
import logging

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from IoTHubTrigger.GardenData import GardenInsert, LogSiramInsert
import time
import requests


def main(event: func.EventHubEvent, insert: func.Out[func.SqlRow], insertLogSiram: func.Out[func.SqlRow], SelectIdData: func.SqlRowList):
    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')
    
    # idTime = time.time_ns()
    totalKelembaban = body["Total Kelembapan"]
    kelembaban1 = body["Nilai Kelembapan 1"]
    kelembaban2 = body["Nilai Kelembapan 2"]
    status_relay = body["Status Relay"]
    nilai_cahaya = body["Nilai Cahaya"]
    datetime = body["DateTime"]
    
    rowdata = func.SqlRow(GardenInsert(totalKelembaban, kelembaban1, kelembaban2,status_relay,nilai_cahaya, datetime, device_id))
    insert.set(rowdata)
    logging.info('Data is saved')


    if totalKelembaban >= 0 and totalKelembaban < 300:
        direct_method = CloudToDeviceMethod(method_name='actuator_on', payload='{}')
        logging.info('Insert Data Actuator')
        rowdata = list(map(lambda r: json.loads(r.to_json()), SelectIdData))
        print (rowdata[0]['id_Data'])
        rowdata = func.SqlRow(LogSiramInsert(datetime, rowdata[0]['id_Data']))
        insertLogSiram.set(rowdata)
        logging.info('Data is saved')
        linkURL = 'https://api.telegram.org/bot6318000053:AAHq9JdNN2s190po_6zHPuveM87K23ZIzkI/sendMessage?'
        data = {
            "chat_id" : '1350618150',
            "text" : 'Aktuator {sr}, Total Kelembapan : {tk}, Sensor 1 : {k1}, Sensor 2 : {k2}, Intensitas Cahaya : {nc}, Tanggal dan Waktu : {dt}'.format(sr = status_relay, tk = totalKelembaban, k1 = kelembaban1, k2 = kelembaban2, nc = nilai_cahaya, dt = datetime)
        }
        tele = requests.get(linkURL, params=data)

    
    elif totalKelembaban >= 300 and totalKelembaban < 700:
        direct_method = CloudToDeviceMethod(method_name='actuator_off', payload='{}')
    elif totalKelembaban > 700:
        direct_method = CloudToDeviceMethod(method_name='actuator_off', payload='{}')
    
    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Direct method request sent!')
