import typer

app = typer.Typer()


@app.command()
def all_pairs():
    typer.echo(f"Todo: Fetching all pairs for Kucoin")


@app.command()
def fetch_all_klines(name: str):
    typer.echo(f"TODO: Fetch all klines for {name}")


if __name__ == "__main__":
    app()