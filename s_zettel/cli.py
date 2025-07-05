import click
from datetime import datetime
from pathlib import Path
#from ops import new_file, new_metdata
import subprocess

def new_file(timestamp, metadata= False):

    if metadata:

        # create metadata dir if it doesn't exist
        metadata_dir = Path("./metadata")
        metadata_dir.mkdir(parents=True, exist_ok=True)

        filename = Path(f"./metadata/{timestamp}.json")
    else:
        filename = Path(f"{timestamp}.md")

    # Create the file if it doesn't exist
    if not filename.exists():
        filename.write_text(f"# Unique Title\n")
        click.echo(f"Created {filename}")
    else:
        click.echo(f"File {filename} already exists.")

    return filename

def new_metadata(timestamp):

    filename = new_file(timestamp, metadata=True)

    filename.write_text("{ }")

    return filename

@click.group()
def ztl():
    """ZTL command line tool."""
    pass

@ztl.command()
def new():

    # Format the filename: "2025-07-05.md"
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    filename = new_file(timestamp)
    filename_metadata = new_metadata(timestamp)


    # Open the file in Vim
    subprocess.run(["vim", str(filename)])

@ztl.command()
@click.option('--file', '-f', type=click.Path(exists=True), required=True, help="Markdown file to edit")
def edit(file):
    """Edit a markdown file."""
    filepath = Path(file)

    # Open the file in Vim
    subprocess.run(["vim", str(filepath)])


@ztl.command()
def list():

    md_files = Path("./").glob("*.md")

    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    print(f"{md_file.name} \t ==> \t {line}")
                    break
            else:
                print(f"{md_file.name} \t ==> \t (no title found)")

@ztl.command()
@click.option('--source', '-s', type=click.Path(exists=True), required=True, help="Source file of relationship")
@click.option('--target', '-t', type=click.Path(exists=True), required=True, help="Target file of relationship")
def link():
    click.echo("Called: ztl link")

if __name__ == "__main__":
    ztl()
