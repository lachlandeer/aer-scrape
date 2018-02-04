# Scraping the American Economic Review

This repository scrapes 'meta' information about journal articles published in
the AER from 1999 to present.

We use `python` and `selenium` to control a headless instance of Google chrome

To run the code:
1. install chromedriver following the receipe [here](https://pp4rs.github.io/installation-guide/webscraping_drivers/)
2. Install Snakemake from command line: `pip install snakemake`
3. Ensure all python packages are installed from command line:  `pip install -r requirements.txt`
4. Run `snakemake` from the command line
    * Sometimes one or more of the aer issues won't run through completely, a workaround curently used is `snakemake --keep-going` to continue running through all jobs. Then re-run `snakemake --keep-going` until all targets are constructed

Tested on: Ubuntu: 16.04
Last Run: Feb 2, 2018

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />
