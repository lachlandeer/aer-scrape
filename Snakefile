# Main Workflow - aer-scrape
# Contributors: @lachlandeer

import glob, os

# --- Importing Configuration Files --- #

configfile: "config.yaml"

# --- User defined Variables --- #

AER_WEB = "https://www.aeaweb.org/journals/aer/issues"

# --- Build Rules --- #

rule aer_issues:
    input:
        script = config["src_scraper"] + "scrape_aer_issues.py"
    params:
        link = AER_WEB
    output:
        issue_links = config["out_links"] + "aer_issues.pickle"
    log:
        config["log"] + "aer_issues.txt"
    shell:
        "python {input.script} \
            --website {params.link} \
            --outData {output.issue_links} \
            > {log}"
