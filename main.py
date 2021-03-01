#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import argparse
import click
import time
import os

def login(driver, username, password, target_url):
	driver.get(target_url)
	driver.find_element_by_id("default_login").click()
	driver.find_element_by_id("username").send_keys(username)
	driver.find_element_by_id("password").send_keys(password)
	driver.find_element_by_class_name("form-button").click()

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
	i = 0
	for page in pages:
		driver.get(page)
		for link in driver.find_elements_by_css_selector('a[href^="/download"]'):
			link.click()
			driver.find_element_by_css_selector('a[aria-label="Download"]').click()
			driver.find_element_by_css_selector('button[aria-label="Close"]').click()
			i += 1

			if i > cutoff:
				print("\nCutoff point reached, aborting programm")
				return i

	return i

def wait_for_downloads(driver, dir, num_downloads, num_existing_files):
	while True:
		files = os.listdir(dir)
		d = [file for file in files if file.endswith(".crdownload")]
		l = len(files)
		#print(d, l)
		if d or l != num_existing_files + num_downloads:
			driver.implicitly_wait(1)
		else:
			break

def main(username, password, url, download_dir=os.getcwd()+"/downloads"):
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

if __name__ == "__main__":
	main("mjeltsch", "***REMOVED***", "https://workgroups.helsinki.fi/display/IP/Workshop+4", 
		 download_dir="/home/tobias/Desktop/test_downloads")