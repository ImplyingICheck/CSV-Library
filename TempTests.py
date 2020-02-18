from pybrary import Pybrary
from iospreadsheetdata import IOSpreadsheetData
import pygsheets
import secretsecret


def create_test_sheet(num_books=10):
    '''
    Creates a test sheet
    '''
    AUTHFILE = secretsecret.authfile()
    MAINGOOGLEACCOUNT = secretsecret.email()
    gc = pygsheets.authorize(service_account_file=AUTHFILE)
    test_col_titles = ['Title', 'Author', 'SUID', 'SUNet', 'Cell Phone', 'Address', 'Date Out', 'Date Due', 'Is Checked Out']
    num_titles = len(test_col_titles)
    test_books = []
    for idx in range(1, num_books + 1):
        book_info = []
        for val in test_col_titles[:len(test_col_titles) - 1]:
            book_info.append(val + " " + str(idx))
        book_info.append("False")
        test_books.append(book_info)

    sh = gc.sheet.create('testSheet')
    sh = gc.open('testSheet')
    wks = sh.sheet1
    # Writes Column Names
    col_titles = pygsheets.DataRange(start=(1, 1), end=(1, num_titles), worksheet=wks)
    col_titles.update_values([test_col_titles])
    # Writes Book Information
    books = pygsheets.DataRange(start=(2, 1), end=(num_books + 1, num_titles), worksheet=wks)
    books.update_values(test_books)
    # Shares sheet to main google account
    sh.share(MAINGOOGLEACCOUNT, role='writer', type='user')


def hackyTest():
    headers = ['Title', 'Author']
    create_test_sheet()
    testLib = Pybrary('libraryKeyDev.json', 'testSheet', 0, headers, 2)
    print('getBookInfo Tests:')
    print(testLib.get_book('Title 1'))
    print(testLib.get_book('Title 2'))
    print(testLib.get_book('Title 3'))
    print()
    print('getBookProperty Tests:')
    print(testLib.get_book_property(book_title='Title 1', prop='Title'))
    print(testLib.get_book_property(book_title='Title 2', prop='Title'))
    print(testLib.get_book_property(book_title='Title 3', prop='Title'))
    print(testLib.get_book_property(book_row=2, prop='Title'))
    print(testLib.get_book_property(book_row=3, prop='Title'))
    print(testLib.get_book_property(book_row=4, prop='Title'))
    print()
    print('checkOutBook Tests:')
    testLib.check_out_book('Title 1', 123, 'testSUNET', 2214324536, 'Somewhere')
    print()
    print('renewCheckOut Tests:')
    testLib.renew_check_out('Title 3')
    print()
    print('checkInBook Tests: ')
    testLib.check_in_book('Title 2')
    print("Test run done.")


io = IOSpreadsheetData('libraryKeyDev.json')
io.print_all_file_names()
hackyTest()
io.print_all_file_names()
io.delete_all_files()
