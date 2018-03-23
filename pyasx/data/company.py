"""
Functions to pull company information off the ASX.com.au site
"""


import csv
import requests
import tempfile
import pyasx.config


def get_listed_companies():
    """
    Pulls a list of all companies listed on the ASX.  This will not include
    anything other than companies, e.i. no EFT/ETPs, options, warrants etc.
    """

    all_listed_companies = []

    # get CSV file of ASX codes, as a stream
    response = requests.get(pyasx.config.get('asx_index_csv'), stream=True)
    response.raise_for_status()  # throw exception for bad status codes

    # parse the CSV result, piping it to a temp file to make the process more memory efficient
    with tempfile.NamedTemporaryFile("w+") as temp_stream:

        # pipe the CSV data to a temp file
        for block in response.iter_content(1024, True):
            temp_stream.write(block)

        # rewind the temp stream and convert it to an iterator for csv.reader below
        temp_stream.seek(0)
        temp_iter = iter(temp_stream.readline, '');

        # skip the first 3 rows of the CSV as they are header rows
        for i in range(0, 3):
            next(temp_iter)

        # read the stream back in & parse out the company details from each row
        for row in csv.reader(temp_iter):

            name, ticker, gics = row

            all_listed_companies.append({
                'name': name,
                'ticker': ticker,
                'gics': gics
            })

    return all_listed_companies


#def get_company_info()
