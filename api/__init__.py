"""Expose the FastAPI ``app`` at package level so `uvicorn api:app` works.

The project previously assumed a module named ``api`` or ``main``. This
repo uses ``bert.py`` as the FastAPI app module. Try importing in the
following order and raise a clear ImportError if none are found.
"""
import importlib
import importlib.util

PREFERRED = ["bert", "api", "main"]

for name in PREFERRED:
    full = f"{__name__}.{name}"
    if importlib.util.find_spec(full) is not None:
        app = importlib.import_module(full).app
        break
else:
    raise ImportError("Could not find an app module. Expected one of: 'bert', 'api', 'main' in the package.")

__all__ = ["app"]
