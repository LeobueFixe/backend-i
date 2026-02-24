import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Heloo {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms.{name}. Have a good day.")
    else:
        print(f"bye {name}!")

@app.command()
def main(name: str):
    message = typer.style(f"{name}, seu careca bunito", fg=typer.colors.BLUE, bold=True)
    print(message)

if __name__ == "__main__":
    app()