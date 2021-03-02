#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import traceback
import eel
import os

def login(driver, username, password):
	driver.find_element_by_id("default_login").click()
	driver.find_element_by_id("username").send_keys(username)
	driver.find_element_by_id("password").send_keys(password)
	driver.find_element_by_class_name("form-button").click()
	#driver.implicitly_wait(1)
	if driver.find_elements_by_css_selector("p.form-error"):
		return False
	else:
		return True

def get_pages(driver):
	driver.implicitly_wait(2)
	lists = driver.find_elements_by_css_selector("ul.rw_pagetree_list")
	for _list in lists:
		if driver.find_element_by_class_name("rw_current_page_item"):
			link_container = _list

	elements = link_container.find_elements_by_css_selector("ul.rw_pagetree_list a")

	links = []
	for element in elements:
		links.append(element.get_attribute("href"))

	return links


def download_files(driver, pages, cutoff):
	items = 0
	for page in pages:
		driver.get(page)
		for link in driver.find_elements_by_css_selector('a[href^="/download"]'):
			for extension in allowed_extensions.keys():
				if allowed_extensions[extension] and link.get_attribute("data-linked-resource-default-alias").endswith(extension):
					items += 1

	i = 1
	for page in pages:
		driver.get(page)
		for link in driver.find_elements_by_css_selector('a[href^="/download"]'):
			for extension in allowed_extensions:
				if allowed_extensions[extension] and link.get_attribute("data-linked-resource-default-alias").endswith(extension):
					link.click()
					driver.find_element_by_css_selector('a[aria-label="Download"]').click()
					driver.find_element_by_css_selector('button[aria-label="Close"]').click()
					eel.updateProgressbar((i/items)*100,'downloading "'+link.get_attribute("data-linked-resource-default-alias")+'"...')
					#print(i, items)

					i += 1
					if i > cutoff:
						print("\nCutoff point reached, aborting programm")
						return i-1

	return i-1

def wait_for_downloads(driver, dir, num_downloads, num_existing_files):
	driver.implicitly_wait(2)
	while True:
		files = os.listdir(dir)
		d = [file for file in files if file.endswith(".crdownload")]
		if d:
			driver.implicitly_wait(1)
		else:
			break

def main(username, password, url, download_dir):
	try:
		options = webdriver.ChromeOptions()
		options.add_experimental_option("prefs", {"download.default_directory": download_dir,
												  "download.prompt_for_download": False,
	 											  "download.directory_upgrade": True,
	  											  "safebrowsing.enabled": True})

		if True:
			options.add_argument('--headless')

		m = len(os.listdir(download_dir))
		driver = webdriver.Chrome(options=options)
		login(driver, username, password, url)
		pages = get_pages(driver)
		n = download_files(driver, pages, 5000)
		wait_for_downloads(driver, download_dir, n, m)
		eel.showEndScreen(n, generate_filepath_html(filepath))

	except Exception as e:
		tb1 = traceback.TracebackException.from_exception(e)
		t = "".join(tb1.format())
		print(t)
		eel.showErrorScreen(t)

def get_download_dir():
	#return os.path.join(os.getcwd(), "downloads")
	return os.path.join(os.path.expanduser("~"), "Downloads")

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

@eel.expose
def nextButtonClick(url, allowed_file_extensions, advanced_options): #executed whith "Next"-Button click, starts webdriver
	print("next Button was clicked")
	print(url, allowed_file_extensions, advanced_options)
	options = webdriver.ChromeOptions()

	global download_dir
	if advanced_options["download_dir"]:
		download_dir = advanced_options["download_dir"]
	else:
		download_dir = get_download_dir()

	if advanced_options["headless"]:
		options.add_argument('--headless')

	options.add_experimental_option("prefs", {"download.default_directory": download_dir,
											  "download.prompt_for_download": False,
	 										  "download.directory_upgrade": True,
	  										  "safebrowsing.enabled": True})

	global allowed_extensions
	allowed_extensions = dict(zip([".pdf", ".xls", ".pptx", ".docx", ".txt", ""], allowed_file_extensions))

	global driver
	driver = webdriver.Chrome(options=options)
	driver.get(url)

@eel.expose
def startButtonClick(username, password):
	print("start Button was clicked")
	print(username, password)
	if login(driver, username, password):
		m = len(os.listdir(download_dir))
		pages = get_pages(driver)
		n = download_files(driver, pages, 5000)
		wait_for_downloads(driver, download_dir, n, m)
		eel.showEndScreen(n, generate_filepath_html(download_dir))
	else:
		eel.wrongLogin()

@eel.expose
def quitButtonClick():
	print("quit Button was clicked")


@eel.expose
def backButtonClick():
	print("back Button was clicked")

if __name__ == '__main__':
	eel.init("web")
	eel.start("index.html", size=(600,450), block=True)


#if __name__ == "__main__":
#	main("mjeltsch", "***REMOVED***", "https://workgroups.helsinki.fi/display/IP/Workshop+4", 
#		 download_dir="/home/tobias/Desktop/test_downloads")