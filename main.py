#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import argparse
import click
import time
import os

USERNAME, PASSWORD = "mjeltsch", "***REMOVED***"

def login(driver):
	driver.get(r"https://workgroups.helsinki.fi/loginout/HYcrowdlogin.php?url=%2Fpages%2Fviewpage.action%3FspaceKey%3DMATRANSMED%26title%3DAPPLICATIONS%2B-%2BHAKEMUKSET")
	driver.find_element_by_id("username").send_keys(USERNAME)
	driver.find_element_by_id("password").send_keys(PASSWORD)
	driver.find_element_by_class_name("form-button").click()

def download_files(driver, cutoff):
	#Find links
	links= []
	elements = driver.find_elements_by_css_selector("#rw_pagetree_item_74300140 .rw_item_content a")
	for element in elements:
		links.append(element.get_attribute("href"))

	#Download files
	i = 0
	with click.progressbar(links, label="Downloading files...") as _links:
		for link in _links:
			driver.get(link)
			for file in driver.find_elements_by_class_name("filename"):
				file.click()
			i += 1
			if i > cutoff:
				print("\nCutoff point reached, aborting programm")
				break

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--version", action="version", version="FILE_DOWNLOADER 1.0")
	parser.add_argument("-d", type=str, default=os.getcwd(), help="specify download directory, default: working directory")
	parser.add_argument("-m", type=int, default=10000, help="specify max amount of files to download")
	parser.add_argument("-l", default=False, action="store_const", const=True, help="make webdriver run headless")
	args = parser.parse_args()

	print("Preparing Download...")
	options = webdriver.ChromeOptions()
	options.add_experimental_option("prefs", {"download.default_directory": args.d,
											  "download.prompt_for_download": False,
  											  "download.directory_upgrade": True,
  											  "safebrowsing.enabled": True})
	if args.l:
		options.add_argument('--headless')

	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(5)

	try:
		login(driver)
		download_files(driver, args.m)
		time.sleep(3)
		driver.quit()

	except Exception as e:
		driver.save_screenshot("error.png")
		driver.quit()
		raise e

if __name__ == "__main__":
	main()