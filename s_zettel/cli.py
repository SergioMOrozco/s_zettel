import click
from datetime import datetime
from pathlib import Path
#from ops import new_file, new_metdata
import subprocess

def new_file(timestamp, metadata= False):

    filename = Path(f"{timestamp}.md")

    # Create the file if it doesn't exist
    if not filename.exists():
        filename.write_text(f"# Unique Title\n")
        click.echo(f"Created {filename}")
    else:
        click.echo(f"File {filename} already exists.")

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
def link(source, target):
    """Add a reference from target to source under '# References'."""
    source_path = Path(source)
    target_path = Path(target)

    # Extract title from source file
    with open(source_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip() # get rid of leading/trailing white space
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                break
        else:
            title = source_path.stem  # stem is the the file prefix 

    # Read and parse target file
    lines = target_path.read_text(encoding='utf-8').splitlines()

    try:
        # gets the line where references title can be found
        ref_index = next(i for i, line in enumerate(lines) if line.strip() == "# References")
    except StopIteration:

        # Add references title if it doesn't exist
        lines.append("")
        lines.append("# References")
        ref_index = len(lines) - 1

    # Existing references. Assumes that everything after references line is a reference
    ref_lines = lines[ref_index + 1:]
    existing_refs = [line.strip() for line in ref_lines if line.strip().startswith("[")]

    # Prevent duplicates in existing references
    if any(source_path.name in line for line in existing_refs):
        click.echo(f"Reference to {source_path.name} already exists in {target_path.name}")
        return

    # Add new reference
    ref_number = len(existing_refs) + 1
    ref_text = f"[{ref_number}] [{title}]({source_path.name})"
    lines.insert(ref_index + 1 + len(existing_refs), ref_text)

    # Write updated content
    target_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
    click.echo(f"Added reference to {source_path.name} with title \"{title}\"")

if __name__ == "__main__":
    ztl()
