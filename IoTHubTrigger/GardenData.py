# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import collections
import time
from datetime import datetime

class GardenInsert(collections.UserDict):
    def __init__(self, Total_Kelembaban, Adc_Total, Nilai_Kelembaban1, Adc_Kelembaban1, Nilai_Kelembaban2, Adc_Kelembaban2, Status_Keterangan, Status_Relay, Nilai_Cahaya, TanggalWaktu, device_id):
        super().__init__()
        # self(isi tabel db)
        self['TotalValue'] = Total_Kelembaban
        self['AdcTotal'] = Adc_Total
        self['ValueKelembapan1'] = Nilai_Kelembaban1
        self['AdcKelembapan1'] = Adc_Kelembaban1
        self['ValueKelembapan2'] = Nilai_Kelembaban2
        self['AdcKelembapan2'] = Adc_Kelembaban2
        self['StatusKeterangan'] = Status_Keterangan
        self['StatusRelay'] = Status_Relay
        self['ValueCahaya'] = Nilai_Cahaya
        self['Waktu'] = TanggalWaktu
        self['id_Device'] = device_id
        

class LogSiramInsert(collections.UserDict):
    def __init__(self, TanggalWaktu, id_Data):
        super().__init__()
        self['Waktu'] = TanggalWaktu
        self['id_Data'] = id_Data
