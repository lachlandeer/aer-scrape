# Scraping the American Economic Review

This repository scrapes 'meta' information about journal articles published in
the AER from 1999 to present.

We use `python` and `selenium` to control a headless instance of Google chrome

To run the code:
1. install chromedriver following the receipe [here](https://pp4rs.github.io/installation-guide/webscraping_drivers/)
2. Install Snakemake from commnad line: `pip install snakemake`
3. Ensure all python packages are installed from command line:  `pip -r requirements.txt`
4. Run `snakemake` from the commad line

Tested on: Ubuntu: 16.04

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />
