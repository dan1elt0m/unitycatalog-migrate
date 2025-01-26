import asyncio
from typer import Typer

from ucm.from_databricks import databricks

app = Typer(name="Unity Catalog Migrator", pretty_exceptions_show_locals=False)

app.add_typer(databricks, name="databricks")


def main():
    """Unity Catalog Migrator"""
    asyncio.run(app())



if __name__ == "__main__":
    main()
