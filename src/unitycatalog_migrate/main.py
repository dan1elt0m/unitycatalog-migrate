from __future__ import annotations

import asyncio
from typing import List

import typer
from databricks.sdk import WorkspaceClient
from typer import Typer
from unitycatalog.client import CatalogsApi, SchemasApi, TablesApi

from unitycatalog_migrate.coro import coro, run_migration_tasks
from unitycatalog_migrate.uc import (
    get_uc_client,
    create_catalog,
    create_schema,
    create_table,
)

app = Typer(name="Unity Catalog Migrator", pretty_exceptions_show_locals=False)


@app.command()
@coro
async def migrate_catalog(
    names: List[str] = typer.Argument(..., help="Catalog names to migrate"),
    profile: str = typer.Option("default", help="Databricks Config profile"),
    token: str = typer.Option(None, help="UC Access token"),
):
    """Migrates catalogs from Databricks to Unity Catalog"""
    w = WorkspaceClient(profile=profile)
    async with get_uc_client(token) as uc_client:
        tasks = [
            (name, create_catalog(w, CatalogsApi(uc_client), name)) for name in names
        ]
        await run_migration_tasks(tasks)


@app.command()
@coro
async def migrate_schema(
    names: List[str] = typer.Argument(
        ..., help="Schema names to migrate. Format: catalog_name.schema_name"
    ),
    profile: str = typer.Option("default", help="Databricks Config profile"),
    token: str = typer.Option(None, help="UC Access token"),
):
    """Migrates schemas from Databricks to Unity Catalog"""
    w = WorkspaceClient(profile=profile)
    async with get_uc_client(token) as uc_client:
        tasks = [
            (name, create_schema(w, SchemasApi(uc_client), name)) for name in names
        ]
        await run_migration_tasks(tasks)


@app.command()
@coro
async def migrate_table(
    names: List[str] = typer.Argument(
        ..., help="Table names to migrate. Format: catalog_name.schema_name.table_name"
    ),
    profile: str = typer.Option("default", help="Databricks Config profile"),
    token: str = typer.Option(None, help="UC Access token"),
):
    """Migrates tables from Databricks to Unity Catalog"""
    w = WorkspaceClient(profile=profile)
    async with get_uc_client(token) as uc_client:
        tasks = [(name, create_table(w, TablesApi(uc_client), name)) for name in names]
        await run_migration_tasks(tasks)


def main():
    """Unity Catalog Migrator"""
    asyncio.run(app())


if __name__ == "__main__":
    main()
