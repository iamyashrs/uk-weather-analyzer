#!/usr/bin/env python
import os
import sys

from uk_weather_analyzer.boot import fix_path
fix_path()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uk_weather_analyzer.settings")

    from djangae.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
