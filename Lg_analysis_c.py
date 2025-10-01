from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait         
from selenium.webdriver.support import expected_conditions as EC   
from bs4 import BeautifulSoup, Comment
import pandas as pd
import logging

#Remember to use logging and error handling 
def find_data():
    
    driver = None

    try:
        #Using selenium to open up fbref 
        print("Opening chrome browser... no logging whatsoever")
        driver = webdriver.Chrome()
        driver.get("https://fbref.com/en/comps/8/2024-2025/2024-2025-Champions-League-Stats")

        #wait until the elements have loaded 
        print("Waiting for webpage to load... weeee are here")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "table_container")))

        #Find the webelements
        league_phase_table = driver.find_element(By.ID, "all_results2024-202582")
    
        #get inner html content    
        league_phase_html = league_phase_table.get_attribute("innerHTML")

        return  league_phase_html 
    finally:
        driver.quit()


def soup_conversion(league_phase_html):
    #convert raw html to beautiful soup objects
    print("Converting raw HTML to beautifulsoup...")
    league_phase_soup = BeautifulSoup(league_phase_html, "html.parser")

    table_league_phase = league_phase_soup.find('table', id = 'results2024-202582_overall') 

    #Checks
    if table_league_phase is None:
        print("No table")
    else:
        print("table exists.")

    return league_phase_soup, table_league_phase

league_phase_html = find_data()
league_phase_soup, table_league_phase = soup_conversion(league_phase_html)

def Pandas_data():

    table = league_phase_soup.find_all('table')
    pandas_table = pd.read_html(str(table))[0]
    print(pandas_table)

    # Sort teams by expected goal difference per 90
    #pd.DataFrame.sort_values("xGD/90", ascending=False).head(10)

# Get only teams that reached the Round of 16
    #pd[["Notes"].str.contains("Round of 16", na=False)]

# Correlation between points and xGD
    #pd[["Pts", "xGD"]].corr()

Pandas_data()




