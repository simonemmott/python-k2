'''
Created on 30 Jan 2019

@author: simon
'''
import click, os, grp, pwd, getpass, shutil
from os import path
from k2 import app_installer

@click.group()
def k2():
    pass   

@k2.command()
@click.option('--base', help='Identify the location of the k2 base directory. If not set defaults to the current directory')
@click.option('--user', help='Identify the OS user that is the owner of the k2 web apps environment. Defaults the current owner of the base directory or the current user if the current base directory does not exist')
@click.option('--group', help='Identify the OS group that is the owner of the k2 web apps environment. Defaults the group the base directory or the group of the current user if the current base directory does not exist')
def config(base, user, group):
    '''
    Configure the current directory or the given base as the K2 base directory
    '''
    k2_base, k2_user, k2_group = _get_base_user_group(base, user, group)
    
    _k2_env_summary(k2_base, k2_user, k2_group)

    if not path.exists(k2_base):
        print('Base directory does not exist. Creating...')
        os.mkdir(k2_base, 0o775)
    
    shutil.chown(k2_base, user=k2_user, group=k2_group)
    
    alias, export = _read_profile(k2_user)
    
    profile = _get_profile(k2_user)
    
    if alias != None:
        if not alias:
            print('{profile} does not include k2 alias. Adding...')
            with open(profile, 'a') as fp:
                fp.write('\n\n')
                fp.write(_alias_k2(k2_base))
        
    if export != None:
        if not export:
            print('{profile} does not include export of k2_BASE. Adding...')
            with open(profile, 'a') as fp:
                fp.write('\n\n')
                fp.write(_export_k2_base(k2_base))
    
    
def _k2_env_summary(base, user, group):
    print()
    print('K2_BASE: {base}'.format(base=base))
    print('K2 Owner: {owner}'.format(owner=user))
    print('K2 Group: {group}'.format(group=group))
    print()
    
def _alias_k2(base):
    return 'alias k2={base}/venv/bin/k2'.format(base=os.path.abspath(base))

def _export_k2_base(base):
    return 'export K2_BASE={base}'.format(base=os.path.abspath(base))

def _get_profile(user):
    home = os.path.expanduser('~'+user)
    if os.path.exists(home):
        if os.path.exists(home+'/.profile'):
            return home+'/.profile'
        elif os.path.exists(home+'/.bash_profile'):
            return home+'/.bash_profile'
        elif os.path.exists(home+'/.bash_rc'):
            return home+'/.bash_rc'

def _read_profile(user):
    profile = _get_profile(user)
    
    if profile:
        with open(profile, 'r') as fp:
            lines = fp.readlines()
                
        alias = False
        export = False
        
        for line in lines:
            if line.strip()[0:9] == 'alias k2=':
                alias = True
            if line.strip()[0:15] == 'export K2_BASE=':
                export = True
        
        return alias, export
    return None, None
        
def _get_base_user_group(base=None, user=None, group=None):
    k2_base = base if base else os.getcwd()
    
    if path.exists(k2_base):
        stat_info = os.stat(k2_base)
        k2_base_user = pwd.getpwuid(stat_info.st_uid)[0]
        k2_base_group = grp.getgrgid(stat_info.st_gid)[0]
    else:
        k2_base_user = getpass.getuser()
        k2_base_group = grp.getgrgid(pwd.getpwnam(k2_base_user).pw_gid).gr_name        
        
    k2_user = user if user else k2_base_user
    k2_group = group if group else k2_base_group
    
    return k2_base, k2_user, k2_group
  
@k2.command()
@click.argument('src')
@click.option('--name')
@click.option('--base')
def install(src, base, name):
    '''
    Install the application source identified by the src URL as a Flask application directory within the current
    K2 base directory identified by the environment variable $K2_BASE
    '''
    if not base:
        base = os.environ['K2_BASE']
        if not base:
            raise ValueError('The environment variable $K2_BASE is not set')
    
    app_installer.install(src, base, name)

if __name__ == '__main__':
    k2()
    
        
    