__author__ = 'fla'

class mylist(object):
    "store file metadata"
    def __init__(self, data=None):
        self.data = data

    def insert(self, data):
        self.data = data

    def delete(self):
        self.data = []

    @staticmethod
    def sum(data):
        if len(data) > 1:
            return mylist(data[0]) + mylist.sum(data[1:])
        elif len(data) == 1:
            return mylist(data[0])
        else:
            return float(0)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        """ add the values of the list except the first one,
        """
        if isinstance(other, mylist):
            result = mylist()
            result.data = self.data
            for i in range(1, len(self.data)):
                result.data[i] = self.data[i] + other.data[i]

            return result




    def get(self):
        return self.data

    @classmethod
    def isdata(self, data):
        '''check that data is a valid data'''
        if isinstance(data, mylist) and isinstance(data.get(), list):
            if len(data) == 4:
                return True
            else:
                return False
        else:
            return False

