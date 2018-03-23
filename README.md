
# PyASX

Python library to pull ASX stock information via the undocumented API used on
[www.ASX.com.au](https://www.asx.com.au).

_NOTE: This library uses a bunch of undocumented APIs from the ASX.com.au
website and thus could break silently :/_

## Example

TODO

## API

### `pyasx.data.companies.get_listed_companies()`

Pull full list of ASX listed companies

### `pyasx.data.companies.get_company_info(ticker)`

Pull detailed info for the given company.

**Example**

    >>> import pyasx.data.companies
    >>> pyasx.data.companies.get_company_info('CBA')
    TODO simplified data pls

### `pyasx.data.companies.get_company_annoucements(ticker)`

Pull the latest annoucements for the given company.

### `pyasx.data.securities.get_listed_securities()`

Pull full list of ASX listed securities.

### `pyasx.data.securities.get_security_info()`

Pull pricing data for the given listed security.

### `pyasx.data.historical.get_security_historical(ticker)`

Pull historical daily OHLC data for specific ASX listed securities.

_NOTE: historical data is pulled from (Float.com.au)[http://float.com.au/]._

## Disclaimer

TODO
