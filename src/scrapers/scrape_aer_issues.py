"""
scrape_issues.py

contributor: @ lachlandeer

This script scrapes all the issue links from the AER main website,
saving them as a csv file

Inputs:
    web_url: the current AER website

Outputs:
    aer_isses.csv : a csv file with a list of links to AER issues linked
                    from the AER homepage

Depends on:
    NULL
"""
# Import libraries
import os
import sys
import re
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
