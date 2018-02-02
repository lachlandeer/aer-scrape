"""
get_article_links.py

contributor: @ lachlandeer

This script scrapes all the article links from the AER main website,
saving them as pickle files, one per issue

Inputs:
    issues: a pickle file of AER issue links

Outputs:
    {issue_id}.pickle : a pickle file with a list of links to articles from
                        each issue of the aer

Depends on:
    NULL
"""
# Import libraries
import os
import sys
import re
import pickle
import argparse
import time
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# ---  Define command line options --- #
# this also generates --help and error handling
CLI = argparse.ArgumentParser()
CLI.add_argument(
  "--issues",  # name on the CLI - drop the `--` for positional/required parameters
  nargs   = "*",  # 0 or more values expected => creates a list
  type    = str,
  default = "None"
)
CLI.add_argument(
  "--outpath",
  nargs   = "*",
  type    = str,  # any type/callable can be used here
  default = "out/",
)

# --- Parse CLI --- #
args          = CLI.parse_args()
issue_links   = args.issues[0]
out_path      = args.outpath[0]

print("Issue links stored in:  ", issue_links)
print("Article links saved to: ", out_path)

# Configure selenium scraper
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options = options)

# --- Read in article links --- #
with open (issue_links, 'rb') as fp:
    issue_list = pickle.load(fp)

for idx, iLink in enumerate(issue_list):
    print("Going to link ", idx, ": ", iLink)

    # Load page and get all links
    driver.get(issue_list[idx])
    payload  = driver.find_element_by_class_name('journal-article-group')
    elements = payload.find_elements_by_xpath("//a[@href]")
    links    = [iElem.get_attribute("href") for iElem in elements]
    # filter out the links that are articles
    regex         = re.compile(r'articles\?id\=')
    article_links = list(filter(regex.search, links))
    # save to disk
    with open(out_path + str(idx) + ".pickle", 'wb') as fp:
        pickle.dump(article_links, fp)

    time.sleep(randint(5, 10))
