"""Adapters package for different logging outputs."""

from lib_logger.adapters.base import BaseAdapter
from lib_logger.adapters.console import ConsoleAdapter
from lib_logger.adapters.gcp import GCPAdapter
from lib_logger.adapters.json import JSONAdapter

__all__ = ["BaseAdapter", "ConsoleAdapter", "JSONAdapter", "GCPAdapter"]
