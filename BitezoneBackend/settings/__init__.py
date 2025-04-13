import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("PIPELINE") == "production":
    from .production import *
else:
    from .local import *
