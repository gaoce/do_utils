#!/usr/bin/env python
from __future__ import print_function

import digitalocean as do
import click
import os

# TODO: store user name in config files
TOKEN = ""


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
def list_drop():
    for name, drop in get_droplets(TOKEN).items():
        click.echo("{}\t{}".format(name, drop.ip_address))


@cli.command()
@click.option('--name', default="Flask", help="Droplet Name")
@click.option('--user', default="flask", help="User Name")
@click.option('--port', default="22", help="SSH Port Number")
def conn(name, user, port):
    drop_dict = get_droplets(TOKEN)
    ip = drop_dict[name].ip_address
    cmd = "ssh -p {} {}@{}".format(port, user, ip)
    click.echo("Connecting to {} at {}".format(name, ip))
    os.system(cmd)


if __name__ == '__main__':
    cli()
