# -*- coding: utf-8 -*-
import uvicorn
from server.server import app
from dotenv import load_dotenv
from model.ownSentiment import loadModel

load_dotenv()
loadModel()

uvicorn.run(app, log_level='debug', host='localhost')