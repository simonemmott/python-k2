class ReferenceError(Exception):
    pass

class RefItem(object):
    __reference__ = None;
    
    def __ref__(self):
        ref_attr = self.__class__.__reference__
        if ref_attr:
            if hasattr(self, ref_attr):
                ref = getattr(self, ref_attr)
                if ref:
                    if callable(ref):
                        return ref()
                    else:
                        return ref
                else:
                    raise ReferenceError('The reference attribute {ref} of class {cls} returned a null value'.format(cls=self.__class__.__name__, ref=ref_attr))
            else:
                raise ReferenceError('The class {cls} does not have the defined reference attribute {ref}'.format(cls=self.__class__.__name__, ref=ref_attr))
        else:
            raise ReferenceError('The class {cls} does not define a reference attribute'.format(cls=self.__class__.__name__))
        
    def __repr__(self):
        return self.__ref__()
    
    
def reference(reference:str):
    def decorator(cls):
        cls.__reference__ = reference
        return cls
    return decorator
    