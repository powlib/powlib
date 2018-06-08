
class Transaction(object):
    '''
    Used to quickly create a Transaction, which
    is used in a lot of the cocotb high-level operations.
    '''

    def __init__(self, **kwargs):
        '''
        Constructs the Transaction. The name of 
        each field must be specified along with
        an assigned value.
        '''

        for field, value in kwargs.items():
            setattr(self, field, value)

    def __str__(self):
        '''
        Represent the Transaction as a string.
        '''

        indat = "".join("({}={})".format(field, value) for field, value in vars(self).items())
        full  = "{}({})".format(self.__class__.__name__,indat)
        return full

