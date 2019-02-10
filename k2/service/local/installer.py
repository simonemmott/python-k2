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
                            'name': 'local_services',
                            'title': 'Get Local Services',
                            'description': 'Get the local services available in this K2 implementation',
                            'returns': 'A list of service definitions',
                            'return_type': {
                                'type': 'list',
                                'items': {
                                    'type': 'k2.service.local'
                                }
                            },
                            'parameters': []
                        }
                    ]
                }
            }
        
    def configuration_labels(self):
        return []
    
    def source(self):
        return 'TODO: K2 LOCAL SERVICE SCRIPT'
