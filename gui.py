#!/usr/bin/python3
# -*- coding: utf-8 -*-

import eel
import main

@eel.expose
def quitButton_click():
	print("quit Button was clicked")

@eel.expose
def submitButton_click(username, password, url):#, download_dir):
	print("submit Button was clicked")
	print(username, password, url)
	main.main(username, password, url)

@eel.expose
def backButton_click():
	print("back Button was clicked")

eel.init("web")
eel.start("index.html", size=(600,400), block=True)
