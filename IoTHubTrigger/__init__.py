import json
import os
import logging

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from IoTHubTrigger.GardenData import GardenInsert, LogSiramInsert
import time
import requests
import pyodbc

def main(event: func.EventHubEvent):
    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')
    
    # idTime = time.time_ns()
    totalKelembaban = body["Total Kelembapan"]
    adcTotal = body["ADC Total"]
    kelembaban1 = body["Nilai Kelembapan 1"]
    adcKelembaban1 = body["ADC Kelembapan 1"]
    kelembaban2 = body["Nilai Kelembapan 2"]
    adcKelembaban2 = body["ADC Kelembapan 2"]
    status_keterangan = body["Status Keterangan"]
    status_relay = body["Status Relay"]
    nilai_cahaya = body["Nilai Cahaya"]
    datetime = body["DateTime"]
    
    try:
        conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:smart-watering-server.database.windows.net,1433;Database=mySWGDatabase;Uid=SmartWateringGarden;Pwd={Raspberrypi4};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
        cursor = conn.cursor()

        insertData = "INSERT INTO dbo.tdata (TotalValue, AdcTotal, ValueKelembapan1, AdcKelembapan1, ValueKelembapan2, AdcKelembapan2, StatusKeterangan, StatusRelay, ValueCahaya, Waktu, id_Device) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(insertData, (totalKelembaban, adcTotal, kelembaban1, adcKelembaban1, kelembaban2, adcKelembaban2, status_keterangan, status_relay, nilai_cahaya, datetime, device_id))
        cursor.commit()
        # agar cursor masih terbuka untuk query selanjutnya
        cursor = conn.cursor() 


        logging.info('Data on tdata is saved')

        if status_relay == "ON":
            direct_method = CloudToDeviceMethod(method_name='actuator_on', payload='{}')
            logging.info('Insert Data Actuator')
            
            findIdData = "select TOP (1) [id_Data] from dbo.tdata ORDER BY [id_Data] DESC"
            cursor.execute(findIdData)
            
            vId_Data = cursor.fetchval()
            print (vId_Data)

            insertLogData = "INSERT INTO dbo.tlog_Siram (Waktu, id_Data) VALUES (?,?)"
            cursor.execute(insertLogData, (datetime, vId_Data))
            cursor.commit()

            logging.info('Data is saved')
            linkURL = 'https://api.telegram.org/bot6318000053:AAHq9JdNN2s190po_6zHPuveM87K23ZIzkI/sendMessage?'
            data = {
                "chat_id" : '1350618150',
                "text" : 'Aktuator {sr} \nTotal Kelembapan : {tk}%({at}), \nStatus Ketarangan : {sk}, \nSensor 1 : {k1}%({ak1}), \nSensor 2 : {k2}%({ak2}), \nIntensitas Cahaya : {nc}lx, \nTanggal dan Waktu : {dt}'.format(
                    sr = status_relay, tk = totalKelembaban, at = adcTotal, sk = status_keterangan, k1 = kelembaban1, ak1 = adcKelembaban1, k2 = kelembaban2, ak2 = adcKelembaban2, nc = nilai_cahaya, dt = datetime)
            }
            tele = requests.get(linkURL, params=data)
            logging.info(f'Sending message via Telegram for device {device_id}')
            logging.info(f'{data}')

        elif status_relay == "OFF":
            direct_method = CloudToDeviceMethod(method_name='actuator_off', payload='{}')
        
        logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

        registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
        registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
        registry_manager.invoke_device_method(device_id, direct_method)

        logging.info('Direct method request sent!')

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f'Error inserting data into the database: {str(e)}')


    