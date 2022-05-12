from pathlib import Path
import requests
import csv
import re

from urls import url_prefix, url_body, url_suffix

# Variables
channel_list=str(Path.home()) + '/Desktop/channel_list.csv'
playlist_string="m3u8"
visual_string="VisualImpaired"
subtitle_string="Subtitles"
audio_string="eng"


def create_channel_list ():
	try:
		with open (channel_list) as channels:
			full_channel_list = channels.read().splitlines()
			return full_channel_list
	except Exception as e:
		raise e
	
def get_channel_information (full_channel_list):
	channel_split = full_channel_list.split(",")
	channel_name = channel_split[0]
	channel_id = channel_split[1]
	return channel_name, channel_id

def get_channel_status_code (channel_id):
	for obc_index in range(1, 8):
		r = requests.get(url_prefix + str(obc_index) + url_body + channel_id + url_suffix)
		if r.status_code == 200:
			return obc_index

def get_channel_definition (channel_id, obc_index):
	r = requests.get(url_prefix + str(obc_index) + url_body + channel_id + url_suffix)
	return r.text

def find_matching_line (line, match_string):
	if re.search(match_string, line):
		return line

def get_stream_definition (obc_index, channel_id, stream_id):
	r = requests.get(url_prefix + str(obc_index) + url_body + channel_id + "/" + stream_id)
	return r.text

def count_streams (obc_index, channel_id, stream_id):
	streams_array = []
#	print(obc_index, channel_id, stream_id)
	stream_text = get_stream_definition(obc_index, channel_id, stream_id)
	for line in stream_text.splitlines():
		if not re.search("#EXT", line):
			streams_array.append(line)
	return (len(streams_array))

def get_playlists (channel_text, channel_id, obc_index):
	playlist_array = []
	for line in channel_text.splitlines():
		playlist = find_matching_line(line, playlist_string)
		if playlist != None:
			if re.search(visual_string, playlist):
				stream_count = count_streams(obc_index, channel_id, playlist.split("URI=")[1].split('"')[1])
				playlist_array.append(playlist.split("URI=")[1].split('"')[1] + " - Visually Impared Track" + "  - " + str(stream_count) + " elements")
			elif re.search(subtitle_string, line):
				stream_count = count_streams(obc_index, channel_id, playlist.split("URI=")[1].split('"')[1])
				playlist_array.append(playlist.split("URI=")[1].split('"')[1] + " - Subtitle Track" + "  - " + str(stream_count) + " elements")
			elif re.search(audio_string, line):
				stream_count = count_streams(obc_index, channel_id, playlist.split("URI=")[1].split('"')[1])
				playlist_array.append(playlist.split("URI=")[1].split('"')[1] + " - Default Audio Track" + "  - " + str(stream_count) + " elements")
			else:
				stream_count = count_streams(obc_index, channel_id, playlist)
				playlist_array.append(playlist + " - Video Track" + " - Default Audio Track" + "  - " + str(stream_count) + " elements")
	playlist_array.sort()
	return playlist_array

full_channel_list = create_channel_list()

for channel in full_channel_list:
	channel_name, channel_id = get_channel_information(channel)
	obc_index = get_channel_status_code(channel_id)

	if obc_index != None:
		channel_text = get_channel_definition(channel_id, obc_index)
		print(channel_name + ", " + channel_id)
		playlists = get_playlists(channel_text, channel_id, obc_index)
		for track in playlists:
			print(track)
		print("")
	else:
		print(channel_name + ", " + channel_id + " - MISSING!")