import os
import pandas as pd


## =========================================================================
##  Get folder separator sign
## =========================================================================
def get_folder_separator():

    if 'ix' in os.name:
        sep = '/'  ## -- path separator for LINIX
    else:
        sep = '\\' ## -- path separator for Windows
    return sep


############################################################################
## =========================================================================
line = '-' * 75
print(line,"Программа для сбора данных из файлов формата прибора DAC в один файл.", line, sep="\n")

## каталог для входных данных
dirname = "data"
sep = get_folder_separator()

if not dirname.endswith(sep):
    dirname = dirname + sep
dirname = '.' + sep + dirname

if not os.path.isdir(dirname):
    print(f"\n\n Error Alarm!! Папка с данными не обнаружена!")
    print(f"Создайте папку {dirname}, положите туда файлы с данными. После этого снова запустите эту программу.\n")
    ##  wait 
    x = input("\n\nPress ENTER to finish...\n")
    exit()
    

first = True
for filename in os.listdir(dirname):
    ##  полный путь к файлу
    file = dirname + filename
    
    ##  работаем только с файлами
    if not os.path.isfile(file):
        print(f"\n {file} не является файлом.", end='\t')
        continue
    
    try:
        date = filename.split('_')[1]
        date = '.'.join([date[-2:], date[4:6], date[:4]])
    except:
        #print(f"\n {filename} name does not look as a DAC datafilename. Skipped.")
        print(f"\n {filename} не похоже на имя файла с данными DAC. Файл пропущен.", end="\t")
        continue
    
    ##  read datafile
    df = pd.read_csv(file)
    print("\n", date, file, os.path.getmtime(file), '\t', df.shape, end='\t') ## время доступа к файлу
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
    print('data: ', data.shape, end='')

##  sort and save
try:    
    ##  отсортировать по времени timestamp
    data.sort_values(by=['timestamp']).drop_duplicates(subset=['timestamp']).set_index('timestamp').to_csv("DAS_collected.csv")
except:
    print(f"\n\nERROR: Данных не обнаружено. Проверьте папку {dirname}, положите туда файлы с данными. После этого снова запустите эту программу.\n")

##  wait 
x = input("\n\nPress ENTER to finish...\n")
