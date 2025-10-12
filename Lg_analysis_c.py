from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait         
from selenium.webdriver.support import expected_conditions as EC   
from bs4 import BeautifulSoup
import pandas as pd
import logging
import matplotlib.pyplot as plt

def get_data():
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
                
                #convert raw html to beautiful soup objects
                print("Converting raw HTML to beautifulsoup...")
                league_phase_soup = BeautifulSoup(league_phase_html, "html.parser")
                table = league_phase_soup.find_all('table')
                pandas_table = pd.read_html(str(table))[0]
                pandas_table.drop("Notes", axis=1, inplace=True)
                print(pandas_table)
                return pandas_table
                
        finally:
                
                driver.quit()



def data_visuals(pandas_table):
       
        #possession vs points   
        plt.scatter(pandas_table['Squad'],pandas_table['GF'], label = 'Goals for')
        plt.scatter(pandas_table['Squad'],pandas_table['xG'], label = 'Expected goals')
        plt.xticks(rotation = 45, ha='right')
        plt.title("Goals compared to Expected Goals")
        plt.xlabel('Team')
        plt.ylabel('Goals')
        plt.legend()
        plt.show()


pandas_table = get_data()
data_visuals(pandas_table)


