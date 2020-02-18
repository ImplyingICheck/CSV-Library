import pygsheets


class IOSpreadsheetData:
    def __init__(self, authfile):
        self.authfile = authfile

    def delete_all_files(self):
        gc = pygsheets.authorize(service_file=self.authfile)
        for file in gc.open_all():
            print("File Deleted: " + file.title)
            file.delete()
        print("All files deleted.")

    def print_all_file_names(self):
        gc = pygsheets.authorize(service_file=self.authfile)
        for file in gc.open_all():
            print("File found: " + file.title)
        print("All file names printed.")
