import csv
from io import open

from .constants import MIN_RECODES, MAX_RECODES

class DotAccessibleDict(dict):
    def __init__(self, dict_):
        super(DotAccessibleDict, self).__init__(dict_.items())
        if isinstance(dict_, dict):
            for k, v in dict_.items():
                self[k] = v

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError as e:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, attr))
        #return self.get(attr)

    def __setattr__(self, key, value): self.__setitem__(key, value)
    def __setitem__(self, key, value):
        super(DotAccessibleDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})
    def __delattr__(self, item): self.__delitem__(item)
    def __delitem__(self, key):
        super(DotAccessibleDict, self).__delitem__(key)
        del self.__dict__[key]


class TraningDataSizeLimitationException(Exception):
    pass


def is_valid_recode_num(file_):
    reader = csv.reader(file_)
    recode_num = sum(1 if len(recode) > 1 else 0 for recode in reader)
    
    if not MIN_RECODES <= recode_num:
        raise TraningDataSizeLimitationException(
                'Data too small, Description: The number of traning entries = %s, ' \
                'witch is smaller than the required mininum of %s' %(recode_num, MIN_RECODES))
    elif not recode_num <= MAX_RECODES:
        raise TraningDataSizeLimitationException(
                'Too many data instances, Description: The number of traning entries = %s,' \
                ' witch is larger than the permitted maximum of %s' %(recode_num, MAX_RECODES))

    file_.seek(0)
    return file_
