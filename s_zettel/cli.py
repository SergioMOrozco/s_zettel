import click
from datetime import datetime
from pathlib import Path
import subprocess

@click.group()
def ztl():
    """ZTL command line tool."""
    pass

@ztl.command()
def new():

    # Format the filename: "2025-07-05.md"
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    filename = Path(f"{timestamp}.md")

    # Create the file if it doesn't exist
    if not filename.exists():
        filename.write_text(f"# Notes for {timestamp}\n")
        click.echo(f"Created {filename}")
    else:
        click.echo(f"File {filename} already exists.")

    # Open the file in Vim
    subprocess.run(["vim", str(filename)])

@ztl.command()
def edit():
    click.echo("Called: ztl edit")

@ztl.command()
def list():
    click.echo("Called: ztl list")

if __name__ == "__main__":
    ztl()
