import os

ENV = os.getenv("ENV", "local")
if ENV == "local":
    from .local import *
else:
    from .production import *