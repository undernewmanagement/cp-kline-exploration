import typer
from google.cloud import bigtable, client

c = bigtable.Client(project='coinpanel-dev', admin=True)

def main(name: str):

    typer.echo(c.list_instances())

if __name__ == "__main__":
    typer.run(main)