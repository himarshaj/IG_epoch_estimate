#!/usr/bin/env python3

import os
import json
from datetime import date
from datetime import datetime, timedelta
import io
import csv
import re
import requests
from bs4 import BeautifulSoup
from csv import writer
from csv import reader
from selenium import webdriver
import selenium as se
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time



def get_shortcodes():
	shortcode_list = []
	with open("shortcode.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")
		for i in reader:
			#print(i[0])
			shortcode = i[0]
			shortcode_list.append(shortcode)
	return shortcode_list

def IG_epoch(milsec,ts):
	time_s = milsec/1000 #TIme from shortcode in seconds wrt to IG_epoch
	time_p = ts #Time from HTML in seconds wrt to unix_epoch
	#IG_epoch = unix_epoch + time_p - time_s
	x = time_p - time_s #IG_epoch wrt to unix_epoch
	IG_epoch = datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
	return IG_epoch


if __name__ == "__main__":
	shortcode_list = get_shortcodes()
	#shortcode_list = ["CHTqeWXhwFv", "CHTqeWXhwFv"]
	with open("Shortcode_epoch_estimate.csv", "w") as f:
		sn = 0
		counter = 0
		for shortcode in shortcode_list:
			sn = sn + 1
			counter = counter +1
			print(sn, shortcode)
			try:
				url =  "https://www.instagram.com/p/%s/" % shortcode
				options = Options()
				driver = webdriver.Chrome(options=options)
				response = driver.get(url)
				html = driver.page_source		
				soup = BeautifulSoup(html, "lxml")
				script_tag = soup.find_all('script') 
				list = []
				for tag in script_tag:
					text = tag.contents
					list.append(text)
				for each in list:
					text = "None"
					try:
						text= each[0]
					except Exception as e:
						pass
					if text.startswith("window._sharedData"):
						a = text.split(' = ', 1)[1]
						a = a.strip(";")
						json_data = json.loads(a)
						shortcode = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['shortcode']
						media_id = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['id']
						created_at_unix = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['taken_at_timestamp']
						is_video = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['is_video']
						vid_duration = None
						count = None
						if is_video == True:
							vid_duration = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_duration']
						is_multiple = False
						try:
							children = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']
							is_multiple = True
						except:
							pass
						if is_multiple == True:
							is_multiple_pics = False
							is_multiple_vids = False
							items = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
							count = len(items)
							vid = "'is_video': True"
							if vid in str(items):
								is_video = "Contains at least one video"
							else:
								is_video = False
						ts = int(created_at_unix)
						created_at_utc = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						media_id_binary = f"{int(media_id):b}"
						media_id_binary = int(media_id_binary, 2)
						media_id_binary_pad_64 = format(media_id_binary, '064b')
						media_id_binary_first_41 = media_id_binary_pad_64[0:41]
						milsec = int(media_id_binary_first_41, 2)
						x = IG_epoch(milsec,ts)
						f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (shortcode, media_id, milsec/1000, created_at_unix, created_at_utc, x, is_multiple, count, is_video, vid_duration))
				time.sleep(10)
				mod = counter%50
				if mod == 0:
					print("Long sleep started..")
					time.sleep(900)
					print("Long sleep finished..")
				driver.quit()
			except Exception as e:
				print(e)
				print(shortcode)