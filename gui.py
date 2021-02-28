#!/usr/bin/python3
# -*- coding: utf-8 -*-

import eel

@eel.expose
def quitButton_click():
	print("quit Button was clicked")

@eel.expose
def submitButton_click():
	print("submit Button was clicked")

@eel.expose
def backButton_click():
	print("back Button was clicked")

eel.init("web")
eel.start("index.html", size=(600,400), block=True)
