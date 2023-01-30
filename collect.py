import os
import pandas as pd


############################################################################
##  Get folder separator sign
############################################################################
def get_folder_separator():

    if 'ix' in os.name:
        sep = '/'  ## -- path separator for LINIX
    else:
        sep = '\\' ## -- path separator for Windows
    return sep
	
	
############################################################################
dirname = "data"
sep = get_folder_separator()

if not dirname.endswith(sep):
    dirname = dirname + sep
dirname = '.' + sep + dirname

first = True
for filename in os.listdir(dirname):
    file = dirname + filename
    date = filename.split('_')[1]
    date = '.'.join([date[-2:], date[4:6], date[:4]])
    
    ##  read datafile
    df = pd.read_csv(file)
    print(date, file, os.path.getmtime(file), df.shape) ## время доступа к файла
    if df.shape[0] == 0:
        continue
        
    ##  add  data and timestamp
    params = ["timestamp", "datetime", "Date"] + list(df.columns.values)
    df['Date'] = date
    df['datetime'] = df.apply(lambda row: row.Date + ' ' + row.Time, axis=1)
    #df['datetime'] = pd.to_datetime(df.datetime)
    df['timestamp'] = df.apply(lambda row: int(pd.to_datetime(row['datetime'], format = '%d.%m.%Y %H:%M:%S').timestamp()), axis=1) #pd.to_datetime(df.Timestamp)
    
    ##  add file data to data frame
    df = df[params]
    if first:
        data = df
        first = False
    else:
        data = pd.concat([data, df], ignore_index=True)
    print('data: ', data.shape)

    
##  отсортировать по времени timestamp
data.sort_values(by=['timestamp']).drop_duplicates(subset=['timestamp']).set_index('timestamp').to_csv("DAS_collected.csv")

