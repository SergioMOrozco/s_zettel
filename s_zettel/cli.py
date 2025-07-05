# ztl_cli.py (or ztl/cli.py if you use a package)
import click

@click.group()
def ztl():
    """ZTL command line tool."""
    pass

@ztl.command()
def new():
    click.echo("Called: ztl new")

@ztl.command()
def edit():
    click.echo("Called: ztl edit")

@ztl.command()
def list():
    click.echo("Called: ztl list")

if __name__ == "__main__":
    ztl()
