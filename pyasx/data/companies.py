"""
Functions to pull information on ASX listed companies via the ASX.com.au API.
"""


import csv
import requests
import tempfile
import pyasx.config
import pyasx.data
import pyasx.data.securities


def get_listed_companies():
    """
    Pulls a list of all companies listed on the ASX.  This will not include
    anything other than companies, i.e. no EFT/ETPs, options, warrants etc.

    This returns an array in the following format;
    [
        {
            'ticker': 'CBA',
            'name': 'COMMONWEALTH BANK OF AUSTRALIA.',
            'gics_industry': 'Banks'
        }
    ]
    :raises pyasx.data.LookupError:
    """

    all_listed_companies = []

    # GET CSV file of ASX codes, as a stream
    try:

        response = requests.get(pyasx.config.get('asx_companies_csv'), stream=True)
        response.raise_for_status()  # throw exception for bad status codes

    except requests.exceptions.HTTPError as ex:

        raise pyasx.data.LookupError("Failed to lookup listed companies; %s" % str(ex))

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
                'gics_industry': gics
            })

    return all_listed_companies


# normalise dividend info as part of get_company_info()
def _normalise_share_dividend_info(raw):

    last_dividend = {  # defaults
        'type': '',
        'created_date': '',
        'ex_date': '',
        'payable_date': '',
        'record_date': '',
        'books_close_date': '',
        'amount_aud': '',
        'franked_percent': '',
        'comments': ''
    }

    if 'last_dividend' in raw:
        raw_dividend = raw['last_dividend']

        last_dividend['type'] = raw_dividend['type'] if 'type' in raw else ''
        last_dividend['created_date'] = raw_dividend['created_date'] if 'created_date' in raw else ''
        last_dividend['ex_date'] = raw_dividend['ex_date'] if 'ex_date' in raw else ''
        last_dividend['payable_date'] = raw_dividend['payable_date'] if 'payable_date' in raw else ''
        last_dividend['record_date'] = raw_dividend['record_date'] if 'record_date' in raw else ''
        last_dividend['books_close_date'] = raw_dividend['books_close_date'] if 'books_close_date' in raw else ''
        last_dividend['amount_aud'] = raw_dividend['amount'] if 'amount' in raw else ''
        last_dividend['franked_percent'] = raw_dividend['raw_franked_percentage'] if 'raw_franked_percentage' in raw else ''
        last_dividend['comments'] = raw_dividend['comments'] if 'comments' in raw else ''

        # parse dates to datetime objects
        last_dividend['created_date'] = pyasx.data._parse_datetime(last_dividend['created_date'])
        last_dividend['ex_date'] = pyasx.data._parse_datetime(last_dividend['ex_date'])
        last_dividend['payable_date'] = pyasx.data._parse_datetime(last_dividend['payable_date'])
        last_dividend['books_close_date'] = pyasx.data._parse_datetime(last_dividend['books_close_date'])

    return last_dividend


# normalise the basic company info as part of get_company_info()
def _normalise_company_info(raw):

    company_info = {}

    company_info['ticker'] = raw['code'] if 'code' in raw else ''
    company_info['name'] = raw['name_full'] if 'name_full' in raw else ''
    company_info['name_short'] = raw['name_abbrev'] if 'name_abbrev' in raw else ''
    company_info['principal_activities'] = raw['principal_activities'] if 'principal_activities' in raw else ''
    company_info['gics_industry'] = raw['industry_group_name'] if 'industry_group_name' in raw else ''
    company_info['gics_sector'] = raw['sector_name'] if 'sector_name' in raw else ''
    company_info['listing_date'] = raw['listing_date'] if 'listing_date' in raw else ''
    company_info['delisting_date'] = raw['delisting_date'] if 'delisting_date' in raw else ''
    company_info['website'] = raw['web_address'] if 'web_address' in raw else ''
    company_info['mailing_address'] = raw['mailing_address'] if 'mailing_address' in raw else ''
    company_info['phone_number'] = raw['phone_number'] if 'phone_number' in raw else ''
    company_info['fax_number'] = raw['fax_number'] if 'fax_number' in raw else ''
    company_info['registry_name'] = raw['registry_name'] if 'registry_name' in raw else ''
    company_info['registry_name'] = raw['registry_name'] if 'registry_name' in raw else ''
    company_info['registry_phone_number'] = raw['registry_phone_number'] if 'registry_phone_number' in raw else ''
    company_info['foreign_exempt'] = raw['foreign_exempt'] if 'foreign_exempt' in raw else False
    company_info['products'] = raw['products'] if 'products' in raw else []

    company_info['last_dividend'] = _normalise_share_dividend_info(raw)

    # parse dates to datetime objects
    company_info['listing_date'] = pyasx.data._parse_datetime(company_info['listing_date'])
    company_info['delisting_date'] = pyasx.data._parse_datetime(company_info['delisting_date'])

    return company_info


def get_company_info(ticker):
    """
    Pull information on the company with the given ticker symbol. This also
    includes all of the pricing information returned by
    `pyasx.data.securities.get_security_info()`.

    This will only work for a company, it will not return information on, ETFs,
    warrants, indices etc. For that please use
    `pyasx.data.securities.get_security_info()`

    :param ticker: The ticker symbol of the company to lookup.
    :raises pyasx.data.LookupError:
    """

    assert(len(ticker) >= 3)

    # build the endpoint to pull company info
    endpoint_pattern = pyasx.config.get('asx_company_json')
    endpoint = endpoint_pattern % ticker.upper()

    # GET the company info
    response = requests.get(endpoint)
    if response.status_code != 200:  # 200 OK

        if response.status_code == 404:
            # 404 not found, therefore unknown ticker

            raise pyasx.data.UnknownTickerException(
                "Unknown company ticker %s" % ticker
            )

        else:
            # otherwise its an error, raise as status so we get a decent description
            # to return in the exception

            try:

                response.raise_for_status()

            except HTTPError as ex:

                raise pyasx.data.LookupError(
                    "Failed to lookup company info for %s; HTTP status %s" % (
                        ticker, str(ex)
                    )
                )

    # parse response & normalise

    raw_info = response.json()

    company_info = _normalise_company_info(raw_info)

    # get company share info, sometimes this is included, other times it is not and we have to pull it manually

    if 'primary_share' in raw_info:
        share_info = pyasx.data.securities._normalise_security_info(raw_info['primary_share'])
    else:
        share_info = pyasx.data.securities.get_security_info(ticker)

    company_info['primary_share'] = share_info

    return company_info


# normalise the annoucements data pulled via get_company_annoucements()
def _normalise_annoucements(raw_annoucements):

    annoucements = []

    if 'data' in raw_annoucements:

        for raw_annoucement in raw_annoucements['data']:

            annoucement = {}
            annoucement['url'] = raw_annoucement['url'] if 'url' in raw_annoucement else ''
            annoucement['title'] = raw_annoucement['header'] if 'header' in raw_annoucement else ''
            annoucement['document_date'] = raw_annoucement['document_date'] if 'document_date' in raw_annoucement else ''
            annoucement['release_date'] = raw_annoucement['document_release_date'] if 'document_release_date' in raw_annoucement else ''
            annoucement['num_pages'] = raw_annoucement['number_of_pages'] if 'number_of_pages' in raw_annoucement else ''
            annoucement['size'] = raw_annoucement['size'] if 'size' in raw_annoucement else ''

            # parse dates to datetime objects
            annoucement['document_date'] = pyasx.data._parse_datetime(annoucement['document_date'])
            annoucement['release_date'] = pyasx.data._parse_datetime(annoucement['release_date'])

            annoucements.append(annoucement)

    return annoucements


def get_company_announcements(ticker):
    """
    Pull the latest company announcements for the company with the given ticker
    symbol. This will only work for companies, it won't work for other securities.

    _NOTE_ This currently only pulls the 20 latest _market sensitive_ announcements.
    :param ticker: The ticker symbol of the company to pull annoucements for.
    :raises pyasx.data.LookupError:
    """

    # build the endpoint to pull announcements info
    endpoint_pattern = pyasx.config.get('asx_announcements_json')
    endpoint = endpoint_pattern % ticker.upper()

    # GET the company annoucements
    try:

        response = requests.get(endpoint)
        response.raise_for_status()  # throw exception for bad status codes

    except requests.exceptions.HTTPError as ex:

        raise pyasx.data.LookupError(
            "Failed to lookup announcements for %s; %s" % (
                ticker, str(ex)
            )
        )

    # parse response & normalise

    raw_announcements = response.json()

    announcements = _normalise_annoucements(raw_announcements)

    return announcements
