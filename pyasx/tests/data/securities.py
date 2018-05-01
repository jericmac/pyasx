

import unittest
import unittest.mock
import pyasx.data
import pyasx.data.securities
import json


class SecuritiesTest(unittest.TestCase):
    """
    Unit tests for pyasx.data.securities module
    """


    def __init__(self, *args, **kwargs):
        super(SecuritiesTest, self).__init__(*args, **kwargs)

        self.get_listed_securities_data = []
        self.get_listed_securities_mock = ""
        self.get_security_info_mock = []


    def setUp(self):

        self.setUpGetListedSecurities()
        self.setUpGetSecurityInfo()


    def setUpGetListedSecurities(self):  # TODO

        self.get_listed_securities_data = [
            # just the first ones from the file to test with
            [ "IJH", "ISHARES MID-CAP ETF", "CHESS DEPOSITARY INTERESTS 1:1 ISHS&P400", "AU000000IJH2" ],
            [ "MOQ", "MOQ LIMITED", "ORDINARY FULLY PAID", "AU000000MOQ5" ],
            [ "MOQAI", "MOQ LIMITED", "OPTION EXPIRING VARIOUS DATES EX VARIOUS PRICES", "AU0000MOQAI6" ],
        ]

        # build the mock CSV data based on self.get_listed_companies_data

        for i in range(0, 5):  # header
            self.get_listed_securities_mock += "HEADER\tROW\n"

        for row in self.get_listed_securities_data:

            csv_row = "\t".join(row)
            csv_row += "\n"

            self.get_listed_securities_mock += csv_row


    def setUpGetSecurityInfo(self):

        # mock data in structure returned by the ASX API
        self.get_security_info_mock = {
            "code": "TICKER",
            "isin_code": "AU000ABC123",
            "desc_full": "DESC FULL",
            "last_price": 1,
            "open_price": 2,
            "day_high_price": 3,
            "day_low_price": 4,
            "change_price": 5,
            "change_in_percent": "7%",
            "volume": 8,
            "bid_price": 9,
            "offer_price": 10,
            "previous_close_price": 11,
            "previous_day_percentage_change": "-12%",
            "year_high_price": 13,
            "last_trade_date": "2018-03-23T00:00:00+1100",
            "year_high_date": "2018-03-23T00:00:00+1100",
            "year_low_price": 14,
            "year_low_date": "2018-03-22T00:00:00+1100",
            "year_open_price": 15,
            "year_open_date": "2014-02-25T11:00:00+1100",
            "year_change_price": -16,
            "year_change_in_percentage": "-17%",
            "pe": 18,
            "eps": 19,
            "average_daily_volume": 20,
            "annual_dividend_yield": 21,
            "market_cap": 22,
            "number_of_shares": 23,
            "deprecated_market_cap": 24,
            "deprecated_number_of_shares": 25,
            "suspended": False,
            "status": [
              "CD"
            ],
            "indices": [
                {
                  "index_code": "XJO",
                  "name_full": "S&P/ASX 200",
                  "name_short": "S&P/ASX200",
                  "name_abrev": "S&P/ASX 200"
                }
            ]
        }


    def testGetListedSecuritiesMocked(self):
        """
        Unit test for pyasx.data.securities.get_listed_securities()
        Test pulling mock data + verify
        """

        with unittest.mock.patch("requests.get") as mock:

            # set up mock iterator for response.iter_content()

            bytes_mock = bytes(self.get_listed_securities_mock, "utf-8")

            instance = mock.return_value
            instance.iter_content.return_value = iter([bytes_mock])

            # this is the test
            securities = pyasx.data.securities.get_listed_securities()

            # verify data is all correct
            i = 0;
            for security in securities:
                security_data = self.get_listed_securities_data[i]

                self.assertEqual(security["ticker"], security_data[0])
                self.assertEqual(security["name"], security_data[1])
                self.assertEqual(security["type"], security_data[2])
                self.assertEqual(security["isin"], security_data[3])

                i += 1


    def testGetListedSecuritiesLive(self):
        """
        Unit test for pyasx.data.securities.get_listed_securities()
        Simple check of pulling live data
        """

        securities = pyasx.data.securities.get_listed_securities()
        self.assertTrue(len(securities) > 1000) # there are at least a few thousand listed securities


    def testGetSecurityInfoMocked(self):
        """
        Unit test for pyasx.data.securities.get_security_info()
        Test pulling mock data + verify
        """

        with unittest.mock.patch("requests.get") as mock:

            # set up mock iterator for response.json()
            instance = mock.return_value
            instance.json.return_value = self.get_security_info_mock

            security = pyasx.data.securities.get_security_info('CBAPC')

            self.assertTrue("ticker"                  in security and security["ticker"] == "TICKER")
            self.assertTrue("isin"                    in security and security["isin"] == "AU000ABC123")
            self.assertTrue("type"                    in security and security["type"] == "DESC FULL")
            self.assertTrue("open_price"              in security and security["open_price"] == 2)
            self.assertTrue("last_price"              in security and security["last_price"] == 1)
            self.assertTrue("bid_price"               in security and security["bid_price"] == 9)
            self.assertTrue("offer_price"             in security and security["offer_price"] == 10)
            self.assertTrue("last_trade_date"         in security and security["last_trade_date"] == "2018-03-23T00:00:00+1100")
            self.assertTrue("day_high_price"          in security and security["day_high_price"] == 3)
            self.assertTrue("day_low_price"           in security and security["day_low_price"] == 4)
            self.assertTrue("day_change_price"        in security and security["day_change_price"] == 5)
            self.assertTrue("day_change_percent"      in security and security["day_change_percent"] == "7%")
            self.assertTrue("day_volume"              in security and security["day_volume"] == 8)
            self.assertTrue("prev_day_close_price"    in security and security["prev_day_close_price"] == 11)
            self.assertTrue("prev_day_change_percent" in security and security["prev_day_change_percent"] == "-12%")
            self.assertTrue("year_high_price"         in security and security["year_high_price"] == 13)
            self.assertTrue("year_high_date"          in security and security["year_high_date"] == "2018-03-23T00:00:00+1100")
            self.assertTrue("year_low_price"          in security and security["year_low_price"] == 14)
            self.assertTrue("year_low_date"           in security and security["year_low_date"] == "2018-03-22T00:00:00+1100")
            self.assertTrue("year_open_price"         in security and security["year_open_price"] == 15)
            self.assertTrue("year_change_price"       in security and security["year_change_price"] == -16)
            self.assertTrue("year_change_percent"     in security and security["year_change_percent"] == "-17%")
            self.assertTrue("average_daily_volume"    in security and security["average_daily_volume"] == 20)
            self.assertTrue("pe"                      in security and security["pe"] == 18)
            self.assertTrue("eps"                     in security and security["eps"] == 19)
            self.assertTrue("annual_dividend_yield"   in security and security["annual_dividend_yield"] == 21)
            self.assertTrue("securities_outstanding"  in security and security["securities_outstanding"] == 23)
            self.assertTrue("market_cap"              in security and security["market_cap"] == 22)
            self.assertTrue("is_suspended"            in security and security["is_suspended"] == False)
            self.assertTrue("indices"                 in security and len(security["indices"]))


    def testGetSecurityInfoLive(self):
        """
        Unit test for pyasx.data.securities.get_security_info()
        Simple check of pulling live data
        """

        security = pyasx.data.securities.get_security_info('CBAPC')
        self.assertTrue("ticker" in security)
        self.assertTrue(len(security))
