'''
Created on 5 Feb 2019

@author: simon
'''
import requests, sys
import os.path
from urllib.parse import urlparse

base = os.environ['K2_BASE']
host = None

def install(src, path=base, name=None):
    global host
    
    response = requests.get(src)
    parsed_uri = urlparse(src)
    host = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    
    if not base:
        raise EnvironmentError('The environment variable K2_BASE is not set')
    
    if not path:
        raise ValueError('The install path must be defined')
    
    if not os.path.exists(path):
        raise FileNotFoundError('The install path: {path} does not exist'.format(path=path))
    
    content_type = response.headers.get('content-type')
    if content_type == 'application/k2-directory':
        write_directory(response, path, name)
    elif content_type == 'application/k2-package':
        write_python_package(response, path, name)
    elif content_type.split('/')[0] == 'text':
        write_file(response, path, name)
    else:
        raise ValueError('{src} returned an unexpected content type: {type}'.format(src=src, type=response.content_type))
    
    
def write_directory(response, path, name):
    given_name = None

    contents = {}
    for key, value in response.headers.items():
        if key == '__name__':
            given_name = value.strip()
        elif key[:6] == 'alias-':
            contents[key[6:]] = value.strip()
        
    if name:
        build = '/'.join([path, name])
    else:
        if not given_name:
            raise ValueError('Either a name or given name must be defined')
        build = '/'.join([path, given_name])
    
    try:
        os.mkdir(build)
    except FileExistsError as err:
        if os.path.isdir(build):
            print('The directory {dir} already exists. Contents will be overwritten'.format(dir=build))
        else:
            raise err
    
    for alias, src in contents.items():
        url = host+src
        install(url, build, alias)
        
    return build
    

def write_python_package(response, path, name):
    build = write_directory(response, path, name)
    
    with open('/'.join([build, '__init__.py']), 'w') as fp:
        fp.write(response.text)
    
    return build

def write_file(response, path, name):
    build = '/'.join([path, name])
    
    with open(build, 'w') as fp:
        fp.write(response.text)
        
    return build
        
if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 2:
        install(sys.argv[1])
    elif len(sys.argv) == 3:
        install(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        install(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        raise ValueError('Incorrect number of arguments')



