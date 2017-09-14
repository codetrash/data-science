import urllib.request as urlreq
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    #direct json
    #url = 'http://data.go.id/api/action/datastore_search?resource_id=8b678581-ccc7-4656-b779-85f89bb9aa1d'

    #by Query
    #Note: it turns out that data.go.id uses postgre
    sql = 'SELECT SUM(jumlah_guru) AS jumlah_guru, kode_provinsi, nama_provinsi from "8b678581-ccc7-4656-b779-85f89bb9aa1d" GROUP BY kode_provinsi, nama_provinsi ORDER BY jumlah_guru ASC'
    url = 'http://data.go.id/api/action/datastore_search_sql?sql=' + sql

    geturl = urlreq.urlopen(url)
    data = geturl.read() #in fact its read as json bytes instead of json

    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON


    data = data.decode('utf8').replace("'", '"')
    data_json = json.loads(data)

    records = data_json['result']['records']

    data_frame = pd.DataFrame(records, columns=['jumlah_guru','nama_provinsi'])
     #check datatype
    print(data_frame.jumlah_guru.dtype)
    print(data_frame.nama_provinsi.dtype)
    #convert to float
    data_frame.jumlah_guru = data_frame.jumlah_guru.astype(float)
    #data_frame.kode_provinsi = data_frame.kode_provinsi.astype(float)
    data_frame.plot(x = 'nama_provinsi', y = 'jumlah_guru', kind = 'barh', color= 'orange')

    print(data_frame)
    plt.xlabel("Jumlah Guru")
    plt.ylabel("Provinsi")

    xmin = min(data_frame.jumlah_guru)
    xmax = max(data_frame.jumlah_guru)
    print("Min X:", xmin, " Max X:", xmax)

    plt.suptitle('Data Guru thn 2012. source: data.go.id', fontsize=14, fontweight='bold', color='purple')

    plt.axis([xmin, xmax, None, None])
    plt.show()
