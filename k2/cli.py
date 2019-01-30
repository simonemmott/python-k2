'''
Created on 30 Jan 2019

@author: simon
'''
import click

@click.group()
def k2():
    pass

@k2.command()
@k2.argument('name')
def hello(name):
    click.echo('Hello %{name}!'.format(name=name))
    
@k2.command()
def goodbye():
    click.echo('Goodbye')