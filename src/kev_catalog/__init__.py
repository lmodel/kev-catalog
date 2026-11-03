"""kev-catalog.

CISA Known Exploited Vulnerabilities (KEV) Catalog (LinkML)
"""

try:
    from kev_catalog._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
