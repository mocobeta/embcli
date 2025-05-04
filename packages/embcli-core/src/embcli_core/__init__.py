from . import cli
from .hookspecs import hookimpl

__all__ = ["hookimpl", "main"]


def main():
    cli.cli()
