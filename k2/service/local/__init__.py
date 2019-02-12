'''
Created on 10 Feb 2019

@author: simon
'''

service_installers = {}

def local_service():
    '''
    This decorator method registers the decorated class as a local service installer
    '''
    def decorator(cls):
        inst = cls()
        service_installers[inst.service()['ref']] = inst
        return cls
    return decorator


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
                                  
    
class LocalServicesDataLoader(object):
    def __init__(self, Service, Type, Method, Parameter):
        self.Service = Service
        self.Type = Type
        self.Method = Method
        self.Parameter = Parameter
        
    def load(self, installer:LocalServiceInstaller):
        service_data = installer.service()
        service = self.Service.query.filter_by(ref=service_data['ref']).first()
        if not service:
            service = self.Service()
        service.name = service_data['name']
        service.ref = service_data['ref']
        service.title = service_data.get('title')
        service.description = service_data.get('description')
        
        if service_data.get('interface'):
            interface_data = service_data['interface']
            interface = self.Type.query.filter_by(name=interface_data['name']).first()
            if not interface:
                interface = self.Type()
            service.interface = interface
            interface.name = interface_data['name']
            interface.title = interface_data.get('title')
            interface.description = interface_data.get('description')
            interface.type = interface_data['type']
            
            if interface_data.get('methods'):
                for method_data in interface_data['methods']:
                    method = interface.methods.query.filter_by(name=method_data['name']).first()
                    if not method:
                        method = self.Method()
                        interface.methods.append(method)
                    method.name = method_data['name']
                    method.title = method_data.get('title')
                    method.description = method_data.get('description')
                    method.returns = method_data.get('returns')
                    method.return_type = self.Type.query.filter_by(name=method_data['return_type'])
                    
                    if method_data.get('parameters'):
                        for parameter_data in method_data['parameters']:
                            parameter = method.parameters.filter_by(name=method_data['name']).first()
                            if not parameter:
                                parameter = self.Parameter()
                                method.parameters.append(parameter)
                            parameter.name = parameter_data['name']
                            parameter.title = parameter_data.get('title')
                            parameter.description = parameter_data.get('description')
                            parameter.type = self.Type.query.filter_by(name=parameter_data['type']).first()
                            parameter.required = parameter_data.get('required')
                        
                        for parameter in method.parameters.all():
                            if parameter.name not in [p['name'] for p in method_data['parameters']]:
                                method.parameters.filter_by(name=parameter.name).delete()
                
                for method in interface.methods.all():
                    if method.name not in [m.name for m in interface_data['methods']]:
                        interface.methods.filter_by(name=method.name).delete()
        return service      
                    
        
        
        
    

    