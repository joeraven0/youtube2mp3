print('Script: youtube2mp3_12.py')
print('Description: Downloads all songs in playlist as sound file webm and converts to mp3.')
print('Howto: By use of readfile.txt, just add playlist href to a line in textfile. Press enter between each playlist')
print('Version: 0.1.2')
print('Change log:')
print('			1. Added ability to use readfile.txt')
print('To be fixed: ')
print('			1. Download segment is slow since the mmpeg need to start and stop during conversion. This was faster in first beta since all files were handled at the same time.\n\n')
import pytube
import os
import re
from pydub import AudioSegment
from pytube import Channel
from pytube import Playlist
from pytube import YouTube
downloadFolder = os.path.expanduser("~")+'/mnt/srv-nas/music/A-Downloaded_mix/'						#Windows example savepath = r'c:\\files\\blabla\\'
artist = ''
album = ''
def enterPlaylists():																				#Insert all playlists to download. Builds the playlist list and then calls for getPlaylist(playlist_url) for each element string in list
	run = 1																							#this resets to 0 when last playlist is inserted
	list_of_playlists=[]
	inputmethod = 0
	a = '0'
	while (inputmethod!='1') and (inputmethod!='2'):												#Select how to input playlist string, manual with terminal or by reading links from textfile
		print("1. Read from terminal")
		print("2. Read from file")
		inputmethod = input("Read method: ")
	counter = 0																						#for iterating through lines in file
	while run == 1:
		if inputmethod=='1':																		#read from terminal input
			a = input("Add playlist - (o)k: ")
		if inputmethod=='2':																		#read from file
			linkfile = open('linkfile.txt')
			filecontent = linkfile.read()
			filecontent = ''.join((filecontent,'\n'))												#add \n to end of file to make sure split works
			links = filecontent.split('\n')															#split playlist links to multiple arrays
			linkfile.close()
			a = links[counter]																		#a is the variables that currently shall download
		if (a!='o') and (len(a)>10):
			try:				
				artist = YouTube(a).author
				album = Playlist(a).title
				list_of_playlists.append(a)
				print('Added artist: '+artist + ' - '+album)
			except:
				print('Except: Really a playlist link?')
		if counter>=len(links)-1:a='o'																#Manual input confirms with letter o, automated file search does it here
		if a == 'o':
																									#print(list_of_playlists)
			run=0
		counter = counter + 1
	print('\n')
	for playlist_url in list_of_playlists:															#send each singe playlist link to getPlaylist()
		getPlaylist(playlist_url)

def getPlaylist(playlist_url):																		#Gets artist, album, song number & url and sends variables to the download() that downloads the files
	artist = YouTube(playlist_url).author															#Get playlist creator, which is the name of the channel, typically the artist channel itself
	p = Playlist(playlist_url)																		#Creates object with all metadata
	album = p.title
	songs = p.videos
	print('\nBegins download of artist & album')
	print('Artist: '+artist)
	print('Album: '+album)
																									#print(p)
	songnumber = 1
	for url in p:																					#p itself is a list of all urls to each song (video) in the playlist
		download(artist,album,url,songnumber)														#Go download it
		songnumber = songnumber + 1																	#Increased to print song number in filename since youtube doesn't have any clue about song numbers more than the song order in



def download(artist,album,url,songnumber):															#magic happens, download the song
	YOUTUBE_STREAM_AUDIO = '140'																	#modify the value to download a different stream. This might not be used? Try to remove later
	if len(artist)>0:																				#create subfolder if artist name exists, if not, then just put in the download folder. Used for single downloaded songs without playlist. Not tried yet in Beta1.2
		artist = artist + '/'
	DOWNLOAD_DIR = downloadFolder+artist+album														#The download dir. Change this to fint operating system paths.

																									#physically downloading the audio track

	string_filepath_files=[]

																									#for video in playlist.videos:
	try:
		audioStream = YouTube(url).streams.last()
		string_filepath = audioStream.download(output_path=DOWNLOAD_DIR)
		string_bitrate = audioStream.abr.replace('bps','')
		song = AudioSegment.from_file(string_filepath,'webm')
		filenamearray=string_filepath.split('/')
		filename = filenamearray[-1].split('.')
		filename[-1] = '.mp3'
		filename[0] = str(songnumber).zfill(2) + " - " + filename[0]
		filenamearray[-1] = ''.join(filename)
		string_filepath_mp3 = '/'.join(filenamearray)
		string_filepath_files.append(string_filepath)
																									#string_filepath_mp3 = string_filepath.replace('.webm','.mp3')
																									#Export mp3 to path
		song.export(string_filepath_mp3, format="mp3", bitrate=string_bitrate)
		print(string_filepath_mp3)
	except:
		print("Video age restrictions")																#Exception thrown if age restriction is set to song, since this script didnt login and confirm its age ;)

	for fileremove in string_filepath_files:														#Remove the downloaded webm file since we converted it to mp3 above
		try:
			os.remove(fileremove)
		except:
			pass		


enterPlaylists()																					#Begins here. Program flow---> enterPlaylists()->getPlaylist(playlist_url)->download(artist,album,url,songnumber)
