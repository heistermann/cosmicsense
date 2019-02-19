# Skeleton of a CLI

import click

import cosmicsense


@click.command('cosmicsense')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(cosmicsense.has_legs)
