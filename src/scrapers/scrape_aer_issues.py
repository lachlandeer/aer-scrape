"""
scrape_issues.py

contributor: @ lachlandeer

This script scrapes all the issue links from the AER main website,
saving them as a csv file

Inputs:
    web_url: the current AER website

Outputs:
    aer_issues.pickle : a csv file with a list of links to AER issues linked
                    from the AER homepage

Depends on:
    NULL
"""
# Import libraries
import os
import sys
import re
import pickle
import argparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# ---  Define command line options --- #
# this also generates --help and error handling
CLI = argparse.ArgumentParser()
CLI.add_argument(
  "--website",  # name on the CLI - drop the `--` for positional/required parameters
  nargs   = "*",  # 0 or more values expected => creates a list
  type    = str,
  default = "google.com"
)
CLI.add_argument(
  "--outData",
  nargs   = "*",
  type    = str,  # any type/callable can be used here
  default = "out/",
)

# --- Parse CLI --- #
args          = CLI.parse_args()
candidate_url = args.website[0]
out_data      = args.outData[0]

print("Scraping:      ", candidate_url)
print("Data saved to: ", out_data)

# Configure selenium scraper
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)

# --- Run Scraper --- #
# Go to URL & get weblinks (stored in hrefs)
driver.get(candidate_url)
print('Connected to website...')
payload  = driver.find_element_by_class_name('journal-preview-group')
elements = payload.find_elements_by_xpath("//a[@href]")

# push all hrefs into list
links  = [iElem.get_attribute("href") for iElem in elements]

# close webdriver
driver.quit()

# filter out the links to issues
regex       = re.compile(r'issues/[0-9]{2,3}$')
issue_links = list(filter(regex.search, links))

with open(out_data, 'wb') as fp:
    pickle.dump(issue_links, fp)
