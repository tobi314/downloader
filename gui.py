#!/usr/bin/python3
# -*- coding: utf-8 -*-

import eel
import main
import os

@eel.expose
def quitButton_click():
	print("quit Button was clicked")

@eel.expose
def submitButton_click(username, password, url):
	print("submit Button was clicked")
	print(username, password, url)
	filepath = os.path.join(os.getcwd(),"downloads")
	n = main.main(username, password, url, filepath)
	print("ready")
	eel.showEndScreen(n, generate_filepath_html(filepath))

@eel.expose
def backButton_click():
	print("back Button was clicked")

def generate_filepath_html(path):
	html = '<ol class="breadcrumb" id="filepath">'

	folders = []
	while 1:
	    path, folder = os.path.split(path)

	    if folder != "":
	        folders.append(folder)
	    elif path != "":
	        folders.append(path)
	        break
	folders.reverse()
	del folders[0]

	for folder in folders:
		html += '<li class="breadcrumb-item"><a href="#">'+folder+'</a></li>'

	html += "</ol>"

	return html

eel.init("web")
eel.start("index.html", size=(600,400), block=True)
