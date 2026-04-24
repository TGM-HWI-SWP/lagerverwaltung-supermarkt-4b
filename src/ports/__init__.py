"""Ports - Re-export from ports.py."""
# Dieses Modul stellt zentrale Schnittstellen bereit

from .repository_port import RepositoryPort  # importiert Repository Schnittstelle
from .ports import ReportPort  # importiert Report Schnittstelle

__all__ = ['RepositoryPort', 'ReportPort']  # definiert öffentliche Exporte

