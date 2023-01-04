from os import listdir
from os.path import isfile, join
from datetime import date, datetime
import os
import time


#monitor path setup
PATH = '/Users/scott/Library/CloudStorage/OneDrive-Personal/Scott and Coco Pty Ltd/Invoices'

#checking frequency, every 1 seconds
#onedrive needs time to download & upload files, need to wait until the file is renamed.

FREQUENCY = 10
now = datetime.now()

#function to return files in a directory
def fileInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return(onlyfiles)



def listComparison(OriginalList: list, NewList: list):
    differencesList = [x for x in NewList if x not in OriginalList] #Note if files get deleted, this will not highlight them
    return(differencesList)


def rename(filearr):
    for file in filearr:
        test = file.split('.')[0][-1]
        #only rename the file if it doesn't end with number
        try:
            test = int(test)
        except:
            test
        if type(test) != int:
            old_path = f'{PATH}/{file}'
            today = date.today().strftime('%d%m%Y')
            new_file_name = '.'.join([file.split('.')[0] +' '+today, file.split('.')[1]]) #add date to the file, keep the original suffix
            new_path = f'{PATH}/{new_file_name}'
            uniq = 1
            #avoid mulitple same files on the same day
            while os.path.exists(new_path):
                new_file_name = '.'.join([file.split('.')[0] +' '+today+' '+str(uniq), file.split('.')[1]])
                new_path = f'{PATH}/{new_file_name}'
                uniq += 1

            os.rename(old_path, new_path)
            print(f'{file} renamed to {new_file_name} at {now}')



def fileWatcher(my_dir: str, pollTime: int):
    while True:
        if 'watching' not in locals():  # Check if this is the first time the function has run
            previousFileList = fileInDirectory(PATH)
            watching = 1
            print('Initial Folder')
            print(previousFileList)
            print('============')

        time.sleep(pollTime)

        newFileList = fileInDirectory(PATH)

        fileDiff = listComparison(previousFileList, newFileList)

        previousFileList = newFileList
        if len(fileDiff) == 0: continue
        rename(fileDiff)

if __name__ == '__main__':
    fileWatcher(PATH, FREQUENCY)