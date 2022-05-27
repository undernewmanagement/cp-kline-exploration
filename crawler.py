import typer
import coinbase.app as coinbase
import kucoin.app as kucoin

app = typer.Typer()

@app.command()
def boom(name:str):
    typer.echo(f"Boom {name}")


app.add_typer(coinbase.app, name="coinbase")
app.add_typer(kucoin.app, name="kucoin")


if __name__ == "__main__":
    app()