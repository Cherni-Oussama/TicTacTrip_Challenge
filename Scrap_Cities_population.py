import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from parsel import Selector

import io
import csv
import pandas as pd
import time 
import re


old_cities_csv = pd.read_csv('./data/cities.csv')
new_cities_csv = old_cities_csv.iloc[:]

nan_value = 0


def convert(lis):
	if lis[1].isdigit() == True :
		population = float(lis[0])*1000 + float(lis[1])
	elif ((lis[1] == 'millions') or (lis[1] == 'million')):
		x = float(lis[0].replace(',','.'))
		population = x *1000000
	else:
		population = lis[0]
	return(population)


lien = "https://www.google.com/search?q=population"

print("\n start scraping...")
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('log-level=3')		
driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options ,service_log_path='NUL' )
driver.get(lien)

for idx , row in new_cities_csv.iterrows():
	try:
		time.sleep(2)


		lien = "https://www.google.com/search?q="+ row['local_name'] + " population"
		driver.get(lien)

		

		try:
			element = driver.find_element_by_css_selector("body.srp.tbo.vasq:nth-child(2) div.mw:nth-child(12) div.col:nth-child(2) div.med:nth-child(3) div.g.mnr-c.g-blk:nth-child(1) div.kp-blk.EyBRub.fm06If.Wnoohf.OJXvsb div.xpdopen:nth-child(1) div.ifM9O:nth-child(1) div.EfDVh.mod div:nth-child(1) div.c4bQHf:nth-child(3) div:nth-child(1) > div.ayqGOc.kno-fb-ctx.KBXm4e")
			population = element.text
		except : 
			element = driver.find_element_by_class_name('Z0LcW')
			population = element.text

		row['population']=convert(population.split())
		new_cities_csv.at[new_cities_csv['id'] == row['id'] , 'population'] = convert(population.split())
		print('nb rech == ' , row)

	except : 
		print('We cant')

driver.close()

new_cities_csv.to_csv (r'./new_cities_csv.csv', index = False, header=True)
