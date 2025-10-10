from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait         
from selenium.webdriver.support import expected_conditions as EC   
from bs4 import BeautifulSoup
import pandas as pd
import logging

try:
        #Using selenium to open up fbref 
        print("Opening chrome browser... no logging whatsoever")
        driver = webdriver.Chrome()
        driver.get("https://fbref.com/en/comps/8/2024-2025/2024-2025-Champions-League-Stats")

        #wait until the elements have loaded 
        print("Waiting for webpage to load... weeee are here")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "table_container")))

        #Find the web elements
        league_phase_table = driver.find_element(By.ID, "all_results2024-202582")
    
        #get inner html content    
        league_phase_html = league_phase_table.get_attribute("innerHTML")

finally:
        driver.quit()

#convert raw html to beautiful soup objects
print("Converting raw HTML to beautifulsoup...")
league_phase_soup = BeautifulSoup(league_phase_html, "html.parser")
table_league_phase = league_phase_soup.find('table', id = 'results2024-202582_overall') 

table = league_phase_soup.find_all('table')
pandas_table = pd.read_html(str(table))[0]
pandas_table.drop("Notes", axis=1, inplace=True)
print(pandas_table)



