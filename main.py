from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

titles = []
prices = []
stocks = []


n = 0
s = 1
k = 2
j = False

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(r'C:\chromedriver.exe', options = options)
driver.get('https://amazon.es/')

action = ActionChains(driver)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sp-cc-accept"]')))
acpt_cookies = driver.find_element_by_xpath('//*[@id="sp-cc-accept"]').click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
search = driver.find_element_by_id('twotabsearchtextbox').send_keys('Móvil', Keys.RETURN)
while s < 8:
	n = 0
	while n < 65:
		try:
			article = driver.find_element_by_xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[' + str(n) + ']/div/span/div/div/span/a/div/img').click()
			j = True

		except:
			print('')
		finally:
			n += 1

		if j:
			try:

				WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'productTitle')))
				title = driver.find_element_by_id('productTitle')

				WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'priceblock_ourprice')))
				price = driver.find_element_by_id('priceblock_ourprice')

				WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="availability"]/span')))
				in_stock = driver.find_element_by_xpath('//*[@id="availability"]/span')

				titles.append(title.text)
				prices.append(price.text)
				stocks.append(in_stock.text)
				driver.back()
			except:
				driver.back()
			finally:
				j = False


	s += 1
	url = 'https://amazon.es/s?k=Móvil&page={}'.format(str(s))
	driver.get(url)

df = pd.DataFrame({'Article':titles, 'Price':prices, 'Stock':stocks})

print(df)
df.to_excel('Móviles.xlsx', index = False)
