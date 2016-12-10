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
