import math
import shutil
from pydub import AudioSegment
from constant_info import SESSION_PATH , RAW_PATH ,DATA_PATH
import os


class MyDataMaker:
    def __init__(self):
        self.split_input = 3

    def get_duration(self, audio):
        return audio.duration_seconds
    def get_audio(self, path):
        return AudioSegment.from_wav(path)    

    def single_split_seconds(self,path, audio, from_sec, to_sec, split_filename):
        t1 = from_sec * 1000
        t2 = to_sec * 1000
        split_audio = audio[t1:t2]
        split_audio.export(path + split_filename, format="wav")

    def multiple_split_Seconds(self, audiofile, file_name,path=''):
        counter = 0
        total_seconds = math.ceil(self.get_duration(audiofile))
        print(total_seconds)
        for i in range(0, total_seconds, self.split_input):
            split_fn = str(counter) + '-' + file_name
            self.single_split_seconds(path,audiofile, i, i + self.split_input, split_fn)
            # print(str(i) + ' Done')
            counter = counter + 1
            if i == total_seconds - self.split_input:
                print('All splited successfully')

    def process_data(self,session_id=0 , filename =''):
        try:
            print("processing raw data ...")
            raw_path=SESSION_PATH+"session_"+str(session_id)+"/"+RAW_PATH
            data_path=SESSION_PATH+"session_"+str(session_id)+"/"+DATA_PATH
            raw_files = os.listdir(raw_path)
            files =[]
            for i in raw_files:
                if  filename in i:
                    files.append(i)
            if len(files) == 0:
                 return str('no raw data found :(...')
            for i in files:
                if self.get_duration(self.get_audio(raw_path+i)) < self.split_input:
                    print('input is lower than 3 seconds ...')
                else:
                    self.multiple_split_Seconds(self.get_audio(raw_path+i), i,path=data_path)

            data_files=os.listdir(data_path)
            print('removing data')

            for i in data_files :
                if self.get_duration(self.get_audio(data_path+i)) <  self.split_input :
                    os.remove(data_path+i)  

    
            return str("processing raw data done !")

        except:
            return str('problem processing data ...')
