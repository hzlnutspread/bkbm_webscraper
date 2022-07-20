from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import pandas as pd
import time

if datetime.now().strftime("%A") == "Monday":
    DATE = (datetime.now() - timedelta(3)).strftime("%A, %B %d, %Y")
else:
    DATE = (datetime.now() - timedelta(1)).strftime("%A, %B %d, %Y")

URL = "https://nzfma.org/data/search.aspx"


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
    print("\n")

    table = soup.find('table', border="1")
    array = []
    values = table.find_all('td')
    for value in values:
        if datetime.now().strftime("%A") == "Monday":
            # format date for csv export
            date_val = (datetime.now() - timedelta(3)).strftime("%d-%b-%y")
        else:
            date_val = (datetime.now() - timedelta(1)).strftime("%d-%b-%y")

        # create subarrays to append to array
        subarray = [date_val, value.text]
        array.append(subarray)

    # data points required
    fra_data = [array[9], array[14], array[19], array[24], array[29], array[34]]
    print(fra_data)

    # create dictionary
    dataframe_collection = {}

    # create dataframe for each of the 6 data points
    for i in range(0, 6):
        df_data = [fra_data[i]]
        data_frame = pd.DataFrame(df_data, columns=['Date', 'rate'])
        data_frame['rate'] = data_frame['rate'].astype(float) + 0.00001  # make sure rounding is correct
        data_frame['rate'] = data_frame['rate'].round(decimals=2)
        dataframe_collection[f'df{i + 1}'] = data_frame

    return dataframe_collection


def write_to_csv(dataframe_collection):
    # print key and value to make sure the data is correct
    for key in dataframe_collection.keys():
        print("\n" + "=" * 20)
        print(key)
        print("-" * 20)
        print(dataframe_collection[key])

    print("")
    # append each of the 6 dataframes to each of the csv files
    for i in range(0, 6):
        # path = f'\\\\SERVER\\jdjl\\interest-nz\\interest.co.nz\\chart_data\\interestrates\\bkbm-{i + 1}mth.csv'
        path = f"C:\\Users\\ken\\Desktop\\Book{i + 1}.csv"
        dataframe_collection[f'df{i + 1}'].to_csv(path, mode='a', index=False, header=False)
        print(f"Successfully added to: bkbm-{i + 1}")


def ftp_files():
    # transfer updated csv files to website server
    # figure out how to do this
    return


if __name__ == '__main__':
    driver = launch_website()  # launch bkbm website
    click_calendar_button(driver)  # select calendar
    select_date(driver)  # choose date
    click_search_button(driver)  # click search button
    time.sleep(1)
    dataframe_collection = get_data_array(driver)  # create the array of data
    time.sleep(1)
    write_to_csv(dataframe_collection)  # update csv files
    driver.quit()

