
class QueryMethod():
    '''
    This is the query method interface. All
    inference methods should inherit from this
    so that we can abstract the details.
    '''
    def query(self, values_dict):
        pass