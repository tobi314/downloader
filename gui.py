#!/usr/bin/python3
# -*- coding: utf-8 -*-

import eel

#@eel.expose
#def button_click():
#	eel.start("loading.html")
#	eel.sleep(5)
#	eel.start("end.html")

eel.init("")
eel.start("web/start.html", block=False, port=8000)