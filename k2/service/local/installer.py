'''
Created on 10 Feb 2019

@author: simon
'''
from k2.service.local import LocalServiceInstaller
from k2.service.local import local_service


@local_service()
class Installer(LocalServiceInstaller):
    
    def service(self):
        return {
            'name': 'LocalServices',
            'ref': 'k2.service.local',
            'title': 'K2 Local Services',
            'description': 'This service manages the local services available in a given k2 installation',
            'interface': {
                'name': 'k2.service.local',
                'title': 'K2 Local Services Type',
                'description': 'The interface of the K2 Local Services service',
                'type': 'INTERFACE',
                'methods': [
                        {
                            'name': 'services',
                            'title': 'Get Local Services',
                            'description': 'Get the local services available in this K2 implementation',
                            'returns': 'A list of service definitions',
                            'return_type': {
                                'type': 'array',
                                'items': {
                                    'type': 'k2.service.local'
                                }
                            },
                            'parameters': []
                        },
                        {
                            'name': 'installer',
                            'title': 'Get Local Service Installer',
                            'description': 'Get local service installer for the given service',
                            'returns': 'An instance of LocalServiceInstaller for the requested service',
                            'return_type': {
                                'type': 'k2.service.local.LocalServiceInstaller',
                            },
                            'parameters': [
                                {
                                    'name': 'service_ref',
                                    'title': 'Service Reference',
                                    'description': 'The reference of the service for which to return the local service installer',
                                    'type': 'string',
                                    'required': True
                                }
                            ]
                        }
                    ]
                }
            }
        
    def configuration_labels(self):
        return []
    
    def source(self):
        return '''
from k2.service.local import service_installers

def services():
    return [inst.service() for _, inst in service_installers.items()]


def installer(service_name):
    return service_installers[service_name]
'''
