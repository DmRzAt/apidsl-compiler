import sys

from apidsl.cli import main

sys.stdout.reconfigure(errors="backslashreplace")
sys.stderr.reconfigure(errors="backslashreplace")
raise SystemExit(main())
