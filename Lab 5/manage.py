
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from ctypes import CDLL


# Load OSGeo4W GDAL before importing Django.
# Required for this Windows environment.
if os.name == "nt":
    OSGEO_BIN = r"C:\OSGeo4W\bin"

    _osgeo_dll_directory = os.add_dll_directory(OSGEO_BIN)

    _gdal_preload = CDLL(
        os.path.join(OSGEO_BIN, "gdal313.dll")
    )


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "webgis.settings"
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Check your virtual environment."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
