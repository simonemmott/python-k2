from pkginfo import installed

class LocalServiceInstaller(object):
    '''
    The interface of all local service installers
    '''
    
    def service(self):
        '''
        Return the definition of the service to be installed
        '''
        raise NotImplementedError('The class {cls} does not implement the method {meth}'.format(cls=self.__class__.__name__, meth='service'))
                                  

    def configuration_labels(self):
        '''
        Return a list of the names of configuration items that configure the service 
        '''
        raise NotImplementedError('The class {cls} does not implement the method {meth}'.format(cls=self.__class__.__name__, meth='configuration_labels'))
    
    
    def source(self):
        '''
        Return the python source code of the service script.
        This script offers all the methods of the service as defined by the interface of the service defintion
        '''
        raise NotImplementedError('The class {cls} does not implement the method {meth}'.format(cls=self.__class__.__name__, meth='source'))                       
                                  
    
    