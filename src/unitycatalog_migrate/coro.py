from __future__ import annotations
import asyncio
from functools import wraps
from typing import Tuple, Coroutine

from rich.console import Console
from rich.live import Live

from unitycatalog_migrate.output import print_skipped, summarize, print_errors
from unitycatalog_migrate.uc import SystemCatalogError

RESULT = {
    "SUCCESS": "[green] Success [reset]",
    "FAILED": "[red] Failed [reset]",
    "SKIPPED": "[yellow] Skipped [reset]",
}

console = Console()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if asyncio.get_event_loop().is_running():
            return asyncio.create_task(f(*args, **kwargs))
        else:
            return asyncio.run(f(*args, **kwargs))

    return wrapper


async def handle_task(
    task,
    name: str,
    success_tasks: list[Tuple[str, str]],
    failed_tasks: list[Tuple[str, str]],
    skipped_tasks: list[Tuple[str, str]],
    live,
):
    """Handle task execution"""
    with live:
        try:
            await task
            result = RESULT["SUCCESS"]
            success_tasks.append((name, "Success"))
        except SystemCatalogError:
            result = RESULT["SKIPPED"]
            skipped_tasks.append((name, "Can't migrate system catalog"))
        except Exception as e:
            if "already exists" in str(e):
                result = RESULT["SKIPPED"]
                skipped_tasks.append((name, "Already exists"))
            else:
                result = RESULT["FAILED"]
                failed_tasks.append((name, str(e)))

        console.log(f"[{result}] {name}")


async def run_migration_tasks(tasks: list[Tuple[str, Coroutine]]):
    """Run migration tasks and summarize results"""
    success_tasks = []
    failed_tasks = []
    skipped_tasks = []
    run_tasks = []
    with console.status("[bold green] Migrating..."), Live() as live:
        for name, task in tasks:
            run_tasks.append(
                handle_task(
                    task, name, success_tasks, failed_tasks, skipped_tasks, live
                )
            )
        await asyncio.gather(*run_tasks, return_exceptions=False)

    summarize(success_tasks, failed_tasks, skipped_tasks)

    if skipped_tasks:
        print_skipped(skipped_tasks)

    if failed_tasks:
        print_errors(failed_tasks)
