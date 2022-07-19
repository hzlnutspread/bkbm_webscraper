
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from csv import writer
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
            date_val = (datetime.now() - timedelta(3)).strftime("%d-%b-%y")                 # format date for csv export
        else:
            date_val = (datetime.now() - timedelta(1)).strftime("%d-%b-%y")                 # format date for csv export

        subarray = [date_val, value.text]                                                   # create subarrays to append to array
        array.append(subarray)

    fra_data = [array[9], array[14], array[19], array[24], array[29], array[34]]            # data points required
    print(fra_data)

    dataframe_collection = {}                                                               # create dictionary

    for i in range(0, 6):
        df_data = [fra_data[i]]
        data_frame = pd.DataFrame(df_data, columns=['Date', 'rate'])
        data_frame['rate'] = data_frame['rate'].astype(float).round(decimals=2)
        dataframe_collection[f'df{i + 1}'] = data_frame                                     # loop to create a dataframe for each data point

#-------------------------------------------------------------- # return dataframe_collection here to pass into new method to append csvs. Get rid of write_to_csv method
    for key in dataframe_collection.keys():
        print("\n" + "=" * 20)
        print(key)
        print("-" * 20)
        print(dataframe_collection[key])                                                    # print it out to make sure its working

    for i in range(0, 6):
        path = f"C:\\Users\\User\\Desktop\\Book{i + 1}.csv"
        dataframe_collection[f'df{i + 1}'].to_csv(path, mode='a', index=False, header=False)
        print("Successfully added")                                                         # append each dataframe onto corresponding csv file

    return dataframe_collection                                                             #


def write_to_csv(array):
    print(DATE + ": ")
    print("\n")

    for x in range(1, 7):
        # location = f'\\SERVER\\jdjl\\interest-nz\\interest.co.nz\\chart_data\\interestrates\\bkbm-{x}mth.csv'
        file_location = f'C:\\Users\\User\\Desktop\\Book{x}.csv'
        with open(file_location, 'a', newline='') as target_csv:
            writer_object = writer(target_csv)
            if x == 1:
                print("bkbm-1mth: ")
                print(array[9])
                print("\n")
                writer_object.writerow(array[9])
                target_csv.close()
            elif x == 2:
                print("bkbm-2mth: ")
                print(array[14])
                print("\n")
                writer_object.writerow(array[14])
                target_csv.close()
            elif x == 3:
                print("bkbm-3mth: ")
                print(array[19])
                print("\n")
                writer_object.writerow(array[19])
                target_csv.close()
            elif x == 4:
                print("bkbm-4mth: ")
                print(array[24])
                print("\n")
                writer_object.writerow(array[24])
                target_csv.close()
            elif x == 5:
                print("bkbm-5mth: ")
                print(array[29])
                print("\n")
                writer_object.writerow(array[29])
                target_csv.close()
            else:
                print("bkbm-6mth: ")
                print(array[34])
                writer_object.writerow(array[34])
                target_csv.close()


def ftp_files():
    return


if __name__ == '__main__':

    driver = launch_website()  # launch bkbm website
    click_calendar_button(driver)  # select calendar
    select_date(driver)  # choose date
    click_search_button(driver)  # click search button
    time.sleep(1)
    data_array = get_data_array(driver)  # create the array of data
    time.sleep(1)
    # write_to_csv(data_array)  # update csv files
    driver.quit()