#!/usr/bin/env python
from __future__ import print_function

import digitalocean as do
import click
import os
import keyring
import getpass

APPNAME = "do-utils"

# python 2 and 3 compatibility
try:
    input = raw_input
except NameError:
    pass


# TODO a token class
def set_token():
    token = getpass.getpass("Please Input the DigitalOcean Access Token: ")
    # TODO: let user input the name
    username = input("Do you want to specify user name? ")
    if username is None:
        username = getpass.getuser()

    keyring.set_password(APPNAME, username, token)


def get_token(username):
    return keyring.get_password(APPNAME, username)


def get_droplets(token):
    # TODO cache the information somewhere
    manager = do.Manager(token=token)

    my_droplets = manager.get_all_droplets()
    drop_dict = {}

    for droplet in my_droplets:
        drop_dict[droplet.name] = droplet

    return drop_dict


@click.group()
def cli():
    pass


@cli.command()
@click.option('--user', default="demo", help="User Name")
def show(user):
    token = get_token(user)
    click.echo("Name\tIP")
    for name, drop in get_droplets(token).items():
        click.echo("{}\t{}".format(name, drop.ip_address))


@cli.command()
@click.option('--name', default="Demo", help="Droplet Name")
@click.option('--user', default="demo", help="User Name")
@click.option('--port', default="22", help="SSH Port Number")
def conn(name, user, port):
    # TODO: default user name should be the same as login name
    token = get_token(user)
    drop_dict = get_droplets(token)
    ip = drop_dict[name].ip_address
    cmd = "ssh -p {} {}@{}".format(port, user, ip)
    click.echo("Connecting to {} at {}".format(name, ip))
    os.system(cmd)


@cli.command()
def setup():
    """Initial setup
    """
    set_token()


if __name__ == '__main__':
    cli()
