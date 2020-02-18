from unittest import TestCase
from iospreadsheetdata import IOSpreadsheetData
from pybrary import Pybrary
import pygsheets
import secretsecret
from pybraryexceptions import NonexistentProperty


class TestPyLibrary(TestCase):
    def create_test_sheet(self, test_col_titles, num_books=10):
        """
        Creates a test sheet
        """
        gc = pygsheets.authorize(service_account_file=secretsecret.authfile())
        num_titles = len(test_col_titles)
        test_books = []
        for idx in range(1, num_books + 1):
            book_info = []
            for val in test_col_titles[:len(test_col_titles) - 1]:
                book_info.append(val + " " + str(idx))
            book_info.append("False")
            test_books.append(book_info)

        gc.sheet.create('testSheet')
        sh = gc.open('testSheet')
        wks = sh.sheet1
        # Writes Column Names
        col_titles = pygsheets.DataRange(start=(1, 1), end=(1, num_titles), worksheet=wks)
        col_titles.update_values([test_col_titles])
        # Writes Book Information
        books = pygsheets.DataRange(start=(2, 1), end=(num_books + 1, num_titles), worksheet=wks)
        books.update_values(test_books)
        # Shares sheet to main google account

    def setUp(self) -> None:
        self.headers = ['Title', 'Author', 'SUID', 'SUNet', 'Cell Phone', 'Address', 'Date Out', 'Date Due', 'Is Checked Out']
        self.permheaders = ['Title', 'Author']
        num_books = 10
        self.io = IOSpreadsheetData(secretsecret.devauthfile())
        self.io.delete_all_files()
        self.create_test_sheet(self.headers, num_books)
        self.pybrary = Pybrary(authfile=secretsecret.devauthfile(),
                                 libraryname='testSheet',
                                 librarypage=0,
                                 permheaders=self.permheaders,
                                 checkoutlimit=2)


class TestLibraryInfoGathering(TestPyLibrary):
    def test_PyLibrary_ExistingProperty_ReturnsPropertyColnum(self):
        existing_property = 'Title'
        expected_col_num = idx + 1 #Columns are 1 indexed
        actual_col_num = self.pybrary.get_property_colnum(existing_property)
        self.assertEqual(expected_col_num, actual_col_num)

    def test_PyLibrary_NonexistentProperty_ExceptionThrown(self):
        nonexistent_property = 'rats'
        self.assertRaises(NonexistentProperty, self.pybrary.get_property_colnum, nonexistent_property)

    def test_get_book_row(self):
        self.fail()

    def test_get_book(self):
        self.fail()

    def test_get_book_property(self):
        self.fail()


class TestCheckIn(TestPyLibrary):
    def test_check_in_book(self):
        self.fail()

    def test_get_check_in_info(self):
        self.fail()


class TestCheckOut(TestPyLibrary):
    def test_check_out_book(self):
        self.fail()

    def test_get_check_out_range(self):
        self.fail()

    def test_get_checkout_info(self):
        self.fail()

    def test_renew_check_out(self):
        self.fail()