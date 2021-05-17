class DetailsPayee():

    def __init__(self, details: str, payee: str = '', category: str = '', subcategory: str = ''):
        self.details = ' '.join(details.split()).lower()
        self.payee = payee
        self.category = category
        self.subcategory = subcategory

    def __iter__(self):
        return iter([
            self.details,
            self.payee,
            self.category,
            self.subcategory
        ])

