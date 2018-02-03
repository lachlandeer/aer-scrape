"""
process_aea_issue.py

contributors: @lachlandeer

"""
import sys
import re
import pickle
import argparse
import time
import pandas as pd
from retry import retry
from timeout_decorator import timeout, TimeoutError
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# --- Functions --- #
@retry(TimeoutError, tries = 5)
@timeout(10)

def get_with_retry(driver, url):
    print("Going to link : ", url)
    driver.get(url)

def get_title(payload):
    title = payload.find_element_by_css_selector('h1.title').text.lower()
    return title

def get_authors(payload):
    authors_web = payload.find_elements_by_css_selector('li.author')
    authors =   [iElem.text for iElem in authors_web]
    author_string = ', '.join(authors).lower()
    return author_string

def get_journal_info(payload):
    journal_web = payload.find_elements_by_css_selector('li.journal')
    journal =   [iElem.text for iElem in journal_web]
    journal_string = ', '.join(journal).lower()
    return journal_string

def get_pages(payload):
    pages = payload.find_element_by_css_selector('li.pages').text
    pages = pages.replace('(pp. ', '').replace(')', '')
    return(pages)

def get_abstract(payload):
    abstract = payload.find_element_by_xpath('//*[@id="article-information"]/section[1]')
    abstract_string = abstract.text.replace('Abstract', '').strip('\n').lower()
    return(abstract_string)

def get_doi(payload):
    doi = payload.find_element_by_css_selector('span.doi').text
    doi = doi.replace('DOI: ', '')
    return doi

def get_jel_codes(payload):
    jel_web = payload.find_elements_by_css_selector('strong.code')
    jel_codes =   [iElem.text for iElem in jel_web]
    jel_string = ', '.join(jel_codes)
    return jel_string

def process_article(candidate_url, headless = True):
    options = webdriver.ChromeOptions()

    if headless == True:
        options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=options)

    try:
        # Load page and get all links
        get_with_retry(driver, candidate_url)

        title     = get_title(driver)
        authors   = get_authors(driver)
        journal   = get_journal_info(driver)
        pages     = get_pages(driver)
        jel_codes = get_jel_codes(driver)
        doi       = get_doi(driver)
        abstract  = get_abstract(driver)

        driver.quit()
        # pack up information
        headers = ['title','authors', 'journal', 'pages',
                    'jel_codes', 'doi', 'abstract']
        article_data = pd.DataFrame([[title, authors, journal, pages,
                                        jel_codes, doi, abstract
                                      ]],
                                    columns=headers)
        return article_data
    except:
        driver.quit()
    finally:
        driver.quit()

def process_journal_issue(in_path):
    # import links to articles of an issue
    with open (in_path, 'rb') as fp:
        article_list = pickle.load(fp)

    issue_data = pd.DataFrame()

    for iLink in article_list:
        article_data = process_article(iLink, headless = True)
        issue_data   = issue_data.append(article_data, ignore_index=True)

    return issue_data

# Main execution
if __name__ == "__main__":
    # CLI parser
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
      "--indata",  # name on the CLI - drop the `--` for positional/required parameters
      nargs   = "*",  # 0 or more values expected => creates a list
      type    = str,
      default = "None"
    )
    CLI.add_argument(
      "--outdata",
      nargs   = "*",
      type    = str,  # any type/callable can be used here
      default = "out/",
    )

    args          = CLI.parse_args()
    issue_links   = args.indata[0]
    out_data      = args.outdata[0]

    print("Issue links stored in:  ", issue_links)
    print("Article links saved to: ", out_data)

    issue_data = process_journal_issue(issue_links)
    issue_data.to_csv(out_data, index = False)
