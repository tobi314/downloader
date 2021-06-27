#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import traceback
import eel
import time
import os
import sys
import pathlib

def handle_exception(e): #displays errorscreen, optionally saves screenshot of webdriver
	tb1 = traceback.TracebackException.from_exception(e)
	t = "".join(tb1.format())
	eel.showErrorScreen(t)
	if screenshot_on_error:
		driver.save_screenshot("error.png")


def login(username, password): #logs in into page
	driver.find_element_by_id("default_login").click()
	driver.find_element_by_id("username").send_keys(username)
	driver.find_element_by_id("password").send_keys(password)
	driver.find_element_by_class_name("form-button").click()

	if driver.find_elements_by_css_selector("p.form-error"): #checks whether login failed
		return False
	else:
		return True

def get_pages(): #scans through all subpages of current page and returns their urls
	driver.implicitly_wait(2)

	lists = driver.find_elements_by_css_selector("ul.rw_pagetree_list") #gets all pagetrees
	for _list in lists: #looks through pagetrees to find current page
		if driver.find_element_by_class_name("rw_current_page_item"):
			link_container = _list

	elements = link_container.find_elements_by_css_selector("ul.rw_pagetree_list a") #gets all page links

	links = []
	for element in elements: #gets thier urls
		links.append(element.get_attribute("href")) 

	return links


def download_files(pages, cutoff): #downloads files
	items = 0
	for page in pages: #loops through pages to get number of files
		driver.get(page)
		for link in driver.find_elements_by_css_selector('a[href^="/download"]'):
			ext = os.path.splitext(link.get_attribute("data-linked-resource-default-alias"))[1]
			if (ext in file_extensions[0]) or ("" in file_extensions[0] and ext not in file_extensions[1]):
				items += 1

	i = 1
	for page in pages: #loops through pages
		driver.get(page)
		for link in driver.find_elements_by_css_selector('a[href^="/download"]'): #loops through all downloadable links in page
			ext = os.path.splitext(link.get_attribute("data-linked-resource-default-alias"))[1] #gets extension of file
			if (ext in file_extensions[0]) or ("" in file_extensions[0] and ext not in file_extensions[1]): #check whether extension is allowed
				link.click()
				driver.find_element_by_css_selector('a[aria-label="Download"]').click() #downloads file
				driver.find_element_by_css_selector('button[aria-label="Close"]').click() #closes file

				#updates progressbar
				eel.updateProgressbar((i/items)*100,'downloading "'+link.get_attribute("data-linked-resource-default-alias")+'"...')

				i += 1
				if i > cutoff: #in case of there beeing too many files, aborts download
					print("\nCutoff point reached, aborting programm")
					return i-1

	return i-1

def wait_for_downloads(): #waits for downloads to finish
	driver.implicitly_wait(2)

	while True: #loops through download dictionary until there are no unfinished downloads anymore
		files = os.listdir(download_dir)
		d = [file for file in files if file.endswith(".crdownload")] #lists all unfinished downloads
		if d: #waits if any are in list
			driver.implicitly_wait(1)
		else:
			break

def get_download_dir(): #returns system download-directory
	return os.path.join(os.path.expanduser("~"), "Downloads")

def generate_filepath_html(path): #dynamically generates html to display download path
	html = '<ol class="breadcrumb" id="filepath">' #starts html <ol>
	folders = []
	while 1: #splits filepath into pieces
	    path, folder = os.path.split(path)

	    if folder != "":
	        folders.append(folder)
	    elif path != "":
	        folders.append(path)
	        break
	folders.reverse()
	del folders[0]

	for folder in folders: #adds <li> to html for each filepath-piece
		html += '<li class="breadcrumb-item">'+folder+'</li>'

	html += "</ol>" #ends html <ol>

	return html

@eel.expose #exposes function, so that it can be called from main.js
def nextButtonClick(url, allowed_file_extensions, advanced_options): #executed whith "Next"-Button click, starts webdriver
	try:
		#print(url, allowed_file_extensions, advanced_options)
		options = webdriver.ChromeOptions()

		global download_dir #ensures that all parts of the programm can access download_dir
		if advanced_options["download_dir"]: #checks whether user specified download_dir
			download_dir = advanced_options["download_dir"]
		else:
			download_dir = get_download_dir() #else gets standart download_dir

		if advanced_options["headless"]:
			options.add_argument('--headless')

		#stets up webdriver to be able to automatically download files on click, without asking user confirmation
		options.add_experimental_option("prefs", {"download.default_directory": download_dir,
												  "download.prompt_for_download": False,
			 									  "download.directory_upgrade": True,
			  									  "safebrowsing.enabled": True})

		global file_extensions #ensures that all parts of the programm can access allowed_extensions
		file_extensions = [[],[]]
		for i in range(len(allowed_file_extensions)): #splits file_extensions into allowed and disallowed
			if allowed_file_extensions[i]:
				file_extensions[0].append([".pdf", ".xls", ".pptx", ".docx", ".txt", ""][i])
			else:
				file_extensions[1].append([".pdf", ".xls", ".pptx", ".docx", ".txt", ""][i])
		if "" in file_extensions[1]:
			del file_extensions[1][file_extensions[1].index("")]
		#print(file_extensions)

		global screenshot_on_error #ensures that all parts of the programm can access screenshot_on_error
		screenshot_on_error = advanced_options["screenshot"]

		global driver #ensures that all parts of the programm can access the webdriver

		## use if os is windows and chromedriver is in /lib 
		driver_location = pathlib.Path(getattr(sys, "._MEIPASS", os.getcwd()))/"lib"/"chromedriver.exe"
		driver = webdriver.Chrome(driver_location, options=options)

		## use if chromedriver is in PATH
		#driver = webdriver.Chrome(options=options)

		driver.get(url)

	except Exception as e:
		handle_exception(e)

@eel.expose #exposes function, so that it can be called from main.js
def startButtonClick(username, password):
	try:
		#print(username, password)
		#raise ValueError
		if login(username, password): #logs in
			m = len(os.listdir(download_dir))
			pages = get_pages() #gets pages
			n = download_files(pages, 5000) #downloads files, cuts programm of after 5000
			wait_for_downloads() #waits for downloads to finish
			eel.showEndScreen(n, generate_filepath_html(download_dir)) #shows endscreen

		else: #if login failed, displays error
			eel.wrongLogin()

	except Exception as e:
		handle_exception(e)

if __name__ == '__main__':
	eel.init("web")
	eel.start("index.html", size=(600,460))