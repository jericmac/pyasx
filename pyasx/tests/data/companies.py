

import unittest
import unittest.mock
import pyasx.data
import pyasx.data.companies


class CompaniesTest(unittest.TestCase):
    """
    Unit tests for pyasx.data.companies module
    """


    def __init__(self, *args, **kwargs):
        super(CompaniesTest, self).__init__(*args, **kwargs)

        self.get_listed_companies_data = []
        self.get_listed_companies_mock = ""
        self.get_company_info_mock = []
        self.get_company_announcements_mock = []


    def setUp(self):

        self.setUpGetListedCompanies()
        self.setUpGetCompanyInfo()
        self.setUpGetCompanyAnnouncements()


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
            self.get_listed_companies_mock+= "\n"

        for row in self.get_listed_companies_data:

            csv_row = ",".join(row)
            csv_row += "\n"

            self.get_listed_companies_mock += csv_row


    def setUpGetCompanyInfo(self):

        # mock data in structure returned by the ASX API
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


    def setUpGetCompanyAnnouncements(self):

        # mock data in structure returned by the ASX API
        self.get_company_announcements_mock = {
            "data": [
                {
                    "id": "12341234",
                    "document_date": "2018-03-15T00:00:00+1100",
                    "document_release_date": "2018-03-14T00:00:00+1100",
                    "url": "FULL URL",
                    "relative_url": "RELATIVE URL",
                    "header": "TITLE",
                    "market_sensitive": True,
                    "number_of_pages": 101,
                    "size": "200.1MB",
                    "legacy_announcement": False
                },
                {
                    "id": "43214321",
                    "document_date": "2018-03-12T00:00:00+1100",
                    "document_release_date": "2018-03-11T00:00:00+1100",
                    "url": "FULL URL",
                    "relative_url": "RELATIVE URL",
                    "header": "TITLE",
                    "market_sensitive": True,
                    "number_of_pages": 202,
                    "size": "100.2MB",
                    "legacy_announcement": True
                },

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
            instance.iter_content.return_value = iter([self.get_listed_companies_mock])

            # this is the test
            companies = pyasx.data.companies.get_listed_companies()

            # verify data is all correct
            i = 0;
            for company in companies:
                company_data = self.get_listed_companies_data[i]

                self.assertEqual(company["name"], company_data[0])
                self.assertEqual(company["ticker"], company_data[1])
                self.assertEqual(company["gics_industry"], company_data[2])

                i += 1


    def testGetListedCompaniesLive(self):
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

            self.assertEquals(company["ticker"], "GEN")
            self.assertEquals(company["name"], "GENERIC INCORPORATED")
            self.assertEquals(company["name_short"], "GENERIC INC")
            self.assertEquals(company["principal_activities"], "ACTIVITIES")
            self.assertEquals(company["gics_industry"], "Banks")
            self.assertEquals(company["gics_sector"], "Financials")
            self.assertEquals(pyasx.data._format_date(company["listing_date"]), "2000-01-01T00:00:00+1000")
            self.assertTrue(company["delisting_date"] is None)
            self.assertEquals(company["website"], "WEBSITE")
            self.assertEquals(company["mailing_address"], "ADDRESS")
            self.assertEquals(company["phone_number"], "4321 4321")
            self.assertEquals(company["fax_number"], "1234 1234")
            self.assertEquals(company["registry_name"], "REG NAME")
            self.assertEquals(company["registry_phone_number"], "1800 123 456")
            self.assertEquals(company["foreign_exempt"], False)
            self.assertTrue(len(company["products"]))
            self.assertTrue(len(company["last_dividend"]))
            self.assertTrue(len(company["primary_share"]))


    def testGetCompanyInfoLive(self):
        """
        Unit test for pyasx.data.company.get_listed_companies()
        Simple check of pulling live data
        """

        company = pyasx.data.companies.get_company_info('CBA')
        self.assertTrue("ticker" in company)
        self.assertTrue(len(company))


    def testGetCompanyAnnouncementsMocked(self):
        """
        Unit test for pyasx.data.company.get_company_announcements()
        Test pulling mock data + verify
        """

        with unittest.mock.patch("requests.get") as mock:

            # set up mock iterator for response.json()
            instance = mock.return_value
            instance.json.return_value = self.get_company_announcements_mock

            # this is the test
            announcements = pyasx.data.companies.get_company_announcements('CBA')

            # verify data is all correct against the mock data
            i = 0;
            for announcement in announcements:
                announcement_data = self.get_company_announcements_mock['data'][i]

                self.assertEqual(announcement["title"], announcement_data["header"])
                self.assertEqual(announcement["url"], announcement_data["url"])

                self.assertEqual(
                    pyasx.data._format_date(announcement["document_date"]),
                    announcement_data["document_date"]
                )

                self.assertEqual(
                    pyasx.data._format_date(announcement["release_date"]),
                    announcement_data["document_release_date"]
                )

                self.assertEqual(announcement["num_pages"], announcement_data["number_of_pages"])
                self.assertEqual(announcement["size"], announcement_data["size"])

                i += 1


    def testGetCompanyAnnouncementsLive(self):
        """
        Unit test for pyasx.data.company.get_company_annoucements()
        Simple check of pulling live data
        """

        announcements = pyasx.data.companies.get_company_announcements('CBA')
        self.assertTrue(len(announcements))
