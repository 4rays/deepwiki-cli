"""CLI entry point for DeepWiki."""

from __future__ import annotations

import sys
from typing import NoReturn

import click

from deepwiki import __version__
from deepwiki.client import (
    ConnectionError,
    DeepWikiClient,
    DeepWikiError,
    ToolError,
    run_async,
)


def validate_repo_name(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validate repository name format."""
    if "/" not in value:
        raise click.BadParameter(
            f"Invalid repository format: '{value}'. Expected format: owner/repo (e.g., facebook/react)"
        )
    parts = value.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise click.BadParameter(
            f"Invalid repository format: '{value}'. Expected format: owner/repo (e.g., facebook/react)"
        )
    return value


def handle_error(e: Exception) -> NoReturn:
    """Handle exceptions and print user-friendly error messages."""
    if isinstance(e, ConnectionError):
        click.secho("Error: ", fg="red", nl=False)
        click.echo("Could not connect to DeepWiki server.")
        click.echo("Please check your internet connection and try again.")
        sys.exit(1)
    elif isinstance(e, ToolError):
        click.secho("Error: ", fg="red", nl=False)
        click.echo(str(e))
        sys.exit(1)
    elif isinstance(e, DeepWikiError):
        click.secho("Error: ", fg="red", nl=False)
        click.echo(str(e))
        sys.exit(1)
    else:
        click.secho("Unexpected error: ", fg="red", nl=False)
        click.echo(str(e))
        sys.exit(1)


@click.group()
@click.version_option(version=__version__, prog_name="ask-deepwiki")
def cli() -> None:
    """Query DeepWiki documentation for any GitHub repository.

    DeepWiki provides AI-generated documentation for open source repositories.
    Use this CLI to explore documentation structure, read contents, or ask
    questions about any repository.

    Examples:

        ask-deepwiki structure facebook/react

        ask-deepwiki contents vercel/next.js

        ask-deepwiki ask langchain-ai/langchain "How do I create a chain?"
    """
    pass


@cli.command()
@click.argument("repo", callback=validate_repo_name)
def structure(repo: str) -> None:
    """Get documentation structure (table of contents) for a repository.

    REPO should be in format owner/repo (e.g., facebook/react)
    """
    client = DeepWikiClient()
    try:
        result = run_async(client.read_wiki_structure(repo))
        click.echo(result)
    except Exception as e:
        handle_error(e)


@cli.command()
@click.argument("repo", callback=validate_repo_name)
def contents(repo: str) -> None:
    """Get full documentation contents for a repository.

    REPO should be in format owner/repo (e.g., facebook/react)

    Note: This may return a large amount of text for repositories
    with extensive documentation.
    """
    client = DeepWikiClient()
    try:
        result = run_async(client.read_wiki_contents(repo))
        click.echo(result)
    except Exception as e:
        handle_error(e)


@cli.command()
@click.argument("repo", callback=validate_repo_name)
@click.argument("question")
def ask(repo: str, question: str) -> None:
    """Ask a question about a repository.

    REPO should be in format owner/repo (e.g., facebook/react)

    QUESTION is your question about the repository (use quotes if it
    contains spaces)

    Examples:

        ask-deepwiki ask facebook/react "What is Fiber?"

        ask-deepwiki ask langchain-ai/langchain "How do chains work?"
    """
    client = DeepWikiClient()
    try:
        result = run_async(client.ask_question(repo, question))
        click.echo(result)
    except Exception as e:
        handle_error(e)


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
