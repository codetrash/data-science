import urllib.request as urlreq
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':

    ''' Dataset '''
    #http://data.go.id/dataset/jumlah-wisatawan-asing
    #by direct json
    #url = 'http://data.go.id/api/action/datastore_search?resource_id=78faf937-6c7e-40c4-9c74-463c67d47a30'

    #By SQL
    sql = 'SELECT * FROM "78faf937-6c7e-40c4-9c74-463c67d47a30" '

    url = 'http://data.go.id/api/action/datastore_search_sql?sql=' + sql
    geturl = urlreq.urlopen(url)
    data = geturl.read()

    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    data = data.decode('utf8')
    data_json = json.loads(data)

    records = data_json['result']['records']

    data_frame1 = pd.DataFrame(records, columns = ['Jumlah Wisman', 'Devisa Wisman (Juta US$)', 'Tahun'])

    #convert Data Type
    data_frame1 = data_frame1.convert_objects( convert_numeric=True)

    #Conver NaN to a number 0
    data_frame1['Jumlah Wisman'] = data_frame1['Jumlah Wisman'].fillna(0)
    data_frame1['Tahun'] = data_frame1['Tahun'].fillna(0)

    data_frame1['Jumlah Wisman'] = data_frame1['Jumlah Wisman'].astype(float)
    data_frame1['Jumlah Wisman'] = data_frame1['Jumlah Wisman'] / 1000
    data_frame1['Tahun'] = data_frame1['Tahun'].astype(float)

    data_frame1['Devisa Wisman (Juta US$)'] = data_frame1['Devisa Wisman (Juta US$)'].astype(float)


    #remove 0 value from table
    data_frame1 = data_frame1[data_frame1['Tahun'] != 0]
    data_frame1 = data_frame1.fillna(0)


    print(data_frame1)


    #create plot from dataFrame

    #data_frame2.plot(x = 'Tahun', y = 'Devisa Wisman (Juta US$)')

    #data_frame1.plot(x = 'Tahun', y = 'Jumlah Wisman')

    fig, (ax1, ax2) = plt.subplots(2)

    dataX = data_frame1['Tahun']
    dataY1 = data_frame1['Jumlah Wisman']
    dataY2 = data_frame1['Devisa Wisman (Juta US$)']


    ax1.plot(dataX, dataY1, 'g-')
    ax2.plot(dataX, dataY2, 'b-')

    ax1.set_ylabel('Jumlah Wisman(K)')
    ax2.set_ylabel('Devisa Wisman (Juta US$)')

    ax1.set_xlabel('Tahun')
    ax2.set_xlabel('Tahun')

    #xLabel range
    xmin = min(data_frame1['Tahun'])
    xmax = max(data_frame1['Tahun']) + 1  #+ 1 year

    #ylabel range
    ax1_ymin = min(data_frame1['Jumlah Wisman'])
    ax1_ymax = max(data_frame1['Jumlah Wisman'])

    ax2_ymin = min(data_frame1['Devisa Wisman (Juta US$)'])
    ax2_ymax = max(data_frame1['Devisa Wisman (Juta US$)'])

    ax1.set_xlim([xmin, xmax])
    ax1.set_ylim([ax1_ymin, ax1_ymax])

    ax2.set_xlim([xmin, xmax])
    ax2.set_ylim([ax2_ymin, ax2_ymax])

    plt.ticklabel_format(useOffset=False, style='plain')

    plt.show()
