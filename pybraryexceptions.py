class NonexistentProperty(Exception):
    def __init__(self, prop):
        self.prop = prop
        self.message = 'The property ' + str(prop) + ' does not exist in the Library.'