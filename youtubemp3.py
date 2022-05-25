import pytube
import os
from pydub import AudioSegment
#Savepath empty if in same folder as script, otherwise clean win path.
#example savepath = r'c:\files'
savepath = r''
def downloadYT():
    url = input('Enter youtube url:') 
    youtube = pytube.YouTube(url)
    #Select youtube source to download - last() is webm format
    video = youtube.streams.last()
    #Returns where webm file was saved
    string_filepath = video.download(savepath)
    #Get bitrate from original file
    string_bitrate = video.abr.replace('bps','')
    song = AudioSegment.from_file(string_filepath,'webm')
    #Create new mp3 filename (change .webm to .mp3)
    string_filepath_mp3 = string_filepath.replace('.webm','.mp3')
    print("Loaded")
    #Export mp3 to path
    song.export(string_filepath_mp3, format="mp3", bitrate=string_bitrate)
    print("Converted and saved")
    #Remove webm file
    os.remove(string_filepath)
downloadYT()
