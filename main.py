# -*- coding: utf-8 -*-
import uvicorn
from server.server import app
from dotenv import load_dotenv
load_dotenv()

uvicorn.run(app, log_level='debug', host='localhost')