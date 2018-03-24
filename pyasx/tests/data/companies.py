"""
Unit tests for the pyasx.data.companies module
"""


import unittest
import unittest.mock
import pyasx.data.companies
import json


class CompaniesTest(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(CompaniesTest, self).__init__(*args, **kwargs)

        self.get_listed_companies_data = []
        self.get_listed_companies_mock = []


    def setUp(self):

        self.setUpGetListedCompanies()
        self.setUpGetCompanyInfo()


    def setUpGetListedCompanies(self):

        self.get_listed_companies_data = [
            # just the first ones from the file to test with
            [ "MOQ LIMITED", "MOQ", "Software & Services" ],
            [ "1-PAGE LIMITED", "1PG", "Software & Services" ],
            [ "1300 SMILES LIMITED", "ONT", "Health Care Equipment & Services" ],
            [ "1ST GROUP LIMITED", "1ST", "Health Care Equipment & Services" ],
        ]

        # build the mock CSV data based on self.get_listed_companies_data

        for i in range(0, 3):  # header
            self.get_listed_companies_mock.append("\n")

        for row in self.get_listed_companies_data:

            csv_row = ",".join(row)
            csv_row += "\n"

            self.get_listed_companies_mock.append(csv_row)


    def setUpGetCompanyInfo(self):

        self.get_company_info_mock = {
            "code":                  "GEN",
            "name_full":             "GENERIC INCORPORATED",
            "name_short":            "GEN INC",
            "name_abbrev":           "GENERIC INC",
            "principal_activities":  "ACTIVITIES",
            "industry_group_name":   "Banks",
            "sector_name":           "Financials",
            "listing_date":          "2000-01-01T00:00:00+1000",
            "delisting_date":        None,
            "web_address":           "WEBSITE",
            "mailing_address":       "ADDRESS",
            "phone_number":          "4321 4321",
            "fax_number":            "1234 1234",
            "registry_name":         "REG NAME",
            "registry_address":      "REG ADDRESS",
            "registry_phone_number": "1800 123 456",
            "foreign_exempt":        False,
            "primary_share_code":    "GEN",  # so it pulls valid pricing info
            "recent_announcement":   False,
            "products":[
                "shares",
                "hybrid-securities",
                "options",
                "warrants"
            ]
        }


    def testGetListedCompaniesMocked(self):
        """
        Unit test for pyasx.data.company.get_listed_companies()
        Test pulling mock data + verify
        """

        with unittest.mock.patch("requests.get") as mock:

            # set up mock iterator for response.iter_content()
            instance = mock.return_value
            instance.iter_content.return_value = iter(self.get_listed_companies_mock)

            # this is the test
            companies = pyasx.data.companies.get_listed_companies()

            # verify data is all correct
            i = 0;
            for company in companies:
                company_data = self.get_listed_companies_data[i]

                self.assertEqual(company["name"], company_data[0])
                self.assertEqual(company["ticker"], company_data[1])
                self.assertEqual(company["gics"], company_data[2])

                i += 1


    def testGetListedCompaniesSimple(self):
        """
        Unit test for pyasx.data.company.get_listed_companies()
        Simple check of pulling live data
        """

        companies = pyasx.data.companies.get_listed_companies()
        self.assertTrue(len(companies) > 1000) # there are atleast a couple thousand listed companies


    def testGetCompanyInfoMocked(self):
        """
        Unit test for pyasx.data.company.get_company_info()
        Test pulling mock data + verify
        """

        with unittest.mock.patch("requests.get") as mock:

            # set up mock iterator for response.json()
            instance = mock.return_value
            instance.json.return_value = self.get_company_info_mock

            company = pyasx.data.companies.get_company_info('CBA')

            self.assertTrue("ticker"                in company and company["ticker"] == "GEN")
            self.assertTrue("name"                  in company and company["name"] == "GENERIC INCORPORATED")
            self.assertTrue("name_short"            in company and company["name_short"] == "GENERIC INC")
            self.assertTrue("principal_activities"  in company and company["principal_activities"] == "ACTIVITIES")
            self.assertTrue("gics"                  in company and company["gics"] == "Banks")
            self.assertTrue("sector"                in company and company["sector"] == "Financials")
            self.assertTrue("listing_date"          in company and company["listing_date"] == "2000-01-01T00:00:00+1000")
            self.assertTrue("delisting_date"        in company and company["delisting_date"] is None)
            self.assertTrue("website"               in company and company["website"] == "WEBSITE")
            self.assertTrue("mailing_address"       in company and company["mailing_address"] == "ADDRESS")
            self.assertTrue("phone_number"          in company and company["phone_number"] == "4321 4321")
            self.assertTrue("fax_number"            in company and company["fax_number"] == "1234 1234")
            self.assertTrue("registry_name"         in company and company["registry_name"] == "REG NAME")
            self.assertTrue("registry_phone_number" in company and company["registry_phone_number"] == "1800 123 456")
            self.assertTrue("foreign_exempt"        in company and company["foreign_exempt"] == False)
            self.assertTrue("products"              in company and len(company["products"]))
            self.assertTrue("last_dividend"         in company and len(company["last_dividend"]))
            self.assertTrue("primary_share"         in company and len(company["primary_share"]))


    def testGetCompanyInfoSimple(self):
        """
        Unit test for pyasx.data.company.get_listed_companies()
        Simple check of pulling live data
        """

        company = pyasx.data.companies.get_company_info('CBA')
        self.assertTrue("ticker" in company)
        self.assertTrue(len(company))
