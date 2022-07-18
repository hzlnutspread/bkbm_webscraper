# bkbm_webscraper

This was a small task I was given responsibility over.

It involves going to the NZFMA website and collecting the previous day's BKBM interest rates. There are 6 rates (1-6
months) and 6 csv files that need to be updated.

The webscraper goes to the NZFMA website, and depending on what day it currently is, will find the most recent values
and update the existing csv files on the company server. It will then FTP the files over to the production server where
it can be viewed on the website.

Another step towards automating my job.