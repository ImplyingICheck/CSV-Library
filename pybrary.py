from collections import OrderedDict
from datetime import date, timedelta
import pygsheets
from typing import List, Tuple, Union
import pybraryexceptions


# worksheet is named LIB
# colheaders are named LIBHEADERS
class Pybrary:

    def __init__(self, authfile: str, libraryname: str, librarypage: int, permheaders: List[str], checkoutlimit: float):
        self.authfile = authfile
        self.libraryname = libraryname
        self.librarypage = librarypage
        self.permheaders = permheaders
        self.checkoutlimit = checkoutlimit

        def get_library_info():
            gc = pygsheets.authorize(service_account_file=self.authfile)
            sh = gc.open(self.libraryname)
            lib = sh[self.librarypage]
            lib_headers = OrderedDict()
            fields = lib.get_row(1, include_tailing_empty=False)
            for idx, field in enumerate(fields):
                # Worksheet is 1 indexed
                lib_headers[field] = idx + 1
            return lib, lib_headers
        self.lib, self.lib_headers = get_library_info()

    def get_property_colnum(self, prop: str) -> int:
        try:
            return self.lib_headers[prop]
        except KeyError:
            raise pybraryexceptions.NonexistentProperty(prop)

    def get_book_row(self, booktitle):
        title_col = self.get_property_colnum('Title')
        query = self.lib.find(booktitle, matchEntireCell=True, cols=(title_col, title_col))
        if len(query) == 0:
            print("No book with that title found.")
        elif len(query) > 1:
            print("Multiple books with that title found.")
        row_num = query[0].row
        return row_num

    def get_book(self, booktitle, returnas='matrix'):
        """
        Returns the information of a book, specified by its Title
        :param booktitle: The title of the book to look up
        :param returnas: The data structure type to return
        :type returnas: Union['matrix', 'range']
        :return: A list of all book information or the Range of the cells in which it is located.
        :rtype: Union[List, Range]
        """
        book_row = self.get_book_row(booktitle)
        book = self.lib.get_row(book_row, returnas=returnas, include_tailing_empty=False)
        return book

    def get_book_property(self, book_title: str = None, book_row: int = None, prop: str = None) -> str:
        """
        Returns a specific property for a given book.
        :param book_title: The title of the book. Used for lookup when the row is not specified
        :param book_row: The row where the book is located. Used for lookup when title is not specified.
        :param prop: The name of the property to lookup
        :return: The information specified by the book row and property column
        :rtype: str
        """
        if book_title:
            row_num = self.get_book_row(book_title)
        elif book_row:
            row_num = book_row
        col_num = self.get_property_colnum(prop)
        prop_value = self.lib.get_value((row_num, col_num))
        return prop_value

    def check_out_book(self, book_title, *addinfo):
        """
        :param book_title:
        :param addinfo: suID, suNet, cellPhone, address
        """
        '''
        #TODO: *addInfo should be well formed (includes all values)
        try:
            validateAddInfo()
        except INVALID
            book = getBookInfo(bookTitle, 'range')
        '''
        book = self.get_book(book_title, 'range')
        book_row = book.start_addr[0]
        perm_book_info = []
        for prop in self.permheaders:
            prop_value = self.get_book_property(book_row=book_row, prop=prop)
            perm_book_info.append(prop_value)
        checkout_info = self.get_checkout_info(perm_book_info, *addinfo)
        book.update_values([checkout_info])
        print(book_title + " has been checked out.")

    def get_check_out_range(self) -> Tuple[str, str]:
        """
        Calculates the due date of the book based upon the specified by self.checkoutlimit.
        The calculation is based on the current date and the time delta uses weeks.
        :return: The date out and date due
        :rtype: Tuple[str, str]
        """
        today = date.today()
        date_out = today.strftime("%d %B %Y")
        date_due = today + timedelta(weeks=self.checkoutlimit)
        date_due = date_due.strftime("%d %B %Y")
        return date_out, date_due

    def get_checkout_info(self, perm_book_info, *addinfo):
        checkout_info = []
        for info in perm_book_info:
            checkout_info.append(info)
        for info in addinfo:
            checkout_info.append(info)
        date_out, date_due = self.get_check_out_range()
        checkout_info.append(date_out)
        checkout_info.append(date_due)
        checkout_info.append('True')
        return checkout_info

    def renew_check_out(self, book_title):
        book = self.get_book(book_title, 'range')
        book_row = book.start_addr[0]
        due_date_col = self.get_property_colnum('Date Due')
        date_due = self.get_check_out_range()[1]
        self.lib.update_value((book_row, due_date_col), str(date_due))
        print(book_title + " is now due on " + date_due + ".")

    def check_in_book(self, book_title):
        book = self.get_book(book_title, 'range')
        book_row = book.start_addr[0]
        perm_book_info = []
        for prop in self.permheaders:
            prop_value = self.get_book_property(book_row=book_row, prop=prop)
            perm_book_info.append(prop_value)
        checkin_info = self.get_check_in_info(perm_book_info)
        book.update_values([checkin_info])
        print(book_title + " has been checked in.")

    def get_check_in_info(self, perm_book_info) -> list:
        """
        Creates a list of all information needed to check in a book.
        :param perm_book_info: Information about the book which stays constant between checkin
        :return: A list combining the perm_book_info and empty string entries corresponding to non-permanent fields
        """
        # -1 Corresponds to isCheckedOut Field
        extraneous_field_len = len(self.lib_headers) - len(self.permheaders) - 1
        checkin_info = perm_book_info + [''] * extraneous_field_len
        checkin_info.append('False')
        return checkin_info
