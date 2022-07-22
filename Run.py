from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from paramiko import *
import pandas as pd
import time

import myconstants

URL = "https://nzfma.org/data/search.aspx"
host = myconstants.REMOTESERVER


def launch_website():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(URL)
    return driver


def click_calendar_button(driver):
    driver.find_element(By.ID, 'ctl00_cphBody_rdpDate_popupButton').click()


def select_date(driver):
    driver.find_element(By.CSS_SELECTOR, f"[title^='{DATE}']").click()


def click_search_button(driver):
    driver.find_element(By.ID, 'cphBody_btnSearch').click()


def get_data_array(driver):
    print("Scraping has successfully begun: ")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print("")

    table = soup.find('table', border="1")
    array = []
    values = table.find_all('td')
    for value in values:
        date_val = (datetime.now() - timedelta(1)).strftime("%d-%b-%y")

        # create subarrays to append to array
        subarray = [date_val, value.text]
        array.append(subarray)

    # data points required
    fra_data = [array[9], array[14], array[19], array[24], array[29], array[34]]
    print("Data successfully gathered: ")
    print(fra_data)

    # create dictionary
    dataframe_collection = {}

    # create dataframe for each of the 6 data points and add to dictionary
    for i in range(0, 6):
        df_data = [fra_data[i]]
        data_frame = pd.DataFrame(df_data, columns=['Date', 'rate'])
        data_frame['rate'] = data_frame['rate'].astype(float) + 0.00001  # make sure rounding is correct
        data_frame['rate'] = data_frame['rate'].round(decimals=2)
        dataframe_collection[f'df{i + 1}'] = data_frame

    # print key and value to make sure the data is correct
    print("\nGenerating DataFrames")
    for key in dataframe_collection.keys():
        print("=" * 20)
        print(key)
        print("-" * 20)
        print(dataframe_collection[key])
    print("")

    return dataframe_collection


def write_to_csv(dataframe_collection):
    # append each of the 6 dataframes to each of the csv files
    for i in range(0, 6):
        path = f'\\\\SERVER\\jdjl\\interest-nz\\interest.co.nz\\chart_data\\interestrates\\bkbm-{i + 1}mth.csv'
        dataframe_collection[f'df{i + 1}'].to_csv(path, mode='a', index=False, header=False)

    print("All files successfully updated")


def ftp_files():
    # connect to the SFTP host server
    print(f"Connecting to {host}...")
    transport = Transport(host)
    transport.connect(None, myconstants.USERNAME, myconstants.PASSWORD)
    sftp = SFTPClient.from_transport(transport)
    print(f"Connection to {host} server successful")

    # upload the local file to replace/update the remote file
    for i in range(0, 6):
        localfile = f"K:\\interest-nz\\interest.co.nz\\chart_data\\interestrates\\bkbm-{i + 1}mth.csv"
        remotefile = f"/var/www/drupal8.interest.co.nz/web/sites/default/files/charts-csv/chart_data/interestrates/bkbm-{i + 1}mth.csv"
        sftp.put(localfile, remotefile)
        print(f"Successfully uploaded: bkbm-{i + 1}mth to host server")
    print("")
    print("All files uploaded")


if __name__ == '__main__':
    if datetime.now().strftime("%A") == "Monday" or datetime.now().strftime("%A") == "Sunday":
        exit()
    else:
        DATE = (datetime.now() - timedelta(1)).strftime("%A, %B %d, %Y")
        driver = launch_website()  # launch bkbm website
        click_calendar_button(driver)  # select calendar
        select_date(driver)  # choose date
        click_search_button(driver)  # click search button
        time.sleep(1)
        dataframe_collection = get_data_array(driver)  # create the array of data
        time.sleep(1)
        write_to_csv(dataframe_collection)  # update csv files
        driver.quit()
        ftp_files()
