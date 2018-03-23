

import unittest
import unittest.mock
import pyasx.data.company


class CompanyTest(unittest.TestCase):


    def test_all_listed(self):

        # self.assertEqual(3, 4)
        # TODO mock requests.get()

        # print(pyasx.data.company.all_listed())

        with unittest.mock.patch('requests.get') as mock:

            # TODO reusable mock object to mock a iter_content() call
            # instance = mock.return_value
            # instance.method.return_value = \
            # '"MOQ LIMITED","MOQ","Software & Services"'
            # '"1-PAGE LIMITED","1PG","Software & Services"'
            # '"1300 SMILES LIMITED","ONT","Health Care Equipment & Services"'
            # '"1ST GROUP LIMITED","1ST","Health Care Equipment & Services"'

            # print(pyasx.data.company.all_listed())
            pyasx.data.company.get_listed_companies()
