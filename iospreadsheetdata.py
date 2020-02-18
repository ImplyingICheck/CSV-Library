import pygsheets
import secretsecret


class IOSpreadsheetData:
    def __init__(self, authfile):
        self.gc = pygsheets.authorize(service_account_file=authfile)

    def delete_all_files(self, verbose=False):
        files = self.gc.open_all()
        for file in files:
            if verbose:
                print("File Deleted: " + file.title)
            file.delete()
        print("All files deleted.")

    def print_all_file_names(self):
        files = self.gc.open_all()
        for file in files:
            print("File found: " + file.title)
        print("All file names printed.")

    def share_sheet(self, sheet_title, gmail):
        sh = self.gc.open(sheet_title)
        sh.share(gmail, role='writer', type='user')
        print('File Shared')
