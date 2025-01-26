from typing import Tuple

from rich.console import Console
from rich.table import Table

console = Console()

def summarize(success_tasks: list[Tuple[str, str]],  failed_tasks: list[Tuple[str, str]], skipped_tasks:list[Tuple[str, str]] ):
    table = Table("Result", "Count")
    table.add_row("Successfully migrated", str(len(success_tasks)))
    table.add_row("Skipped", str(len(skipped_tasks)))
    table.add_row("Errors", str(len(failed_tasks)))
    console.print(table)

def print_skipped(skipped_tasks: list[Tuple[str, str]]):
    table = Table("Skipped", "Reason")
    for name, reason in skipped_tasks:
        table.add_row(name, reason)
    console.print(table)

def print_errors(failed_tasks: list[Tuple[str, str]]):
    table = Table("Failed", "Reason")
    for name, error in failed_tasks:
        table.add_row(name, error)
    console.print(table)


