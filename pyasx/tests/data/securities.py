

import unittest
import unittest.mock
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


    def setUp(self):

        self.setUpGetListedSecurities()


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
        Unit test for pyasx.data.company.get_listed_securities()
        Simple check of pulling live data
        """

        securities = pyasx.data.companies.get_listed_securities()
        self.assertTrue(len(securities) > 1000) # there are at least a few thousand listed securities
