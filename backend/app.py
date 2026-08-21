import os 
import random 
import sys 
import time 
from datetime import datetime 

from flask import Flask,jsonify , request, send_file
from flask_cors import CORS

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "model"))
from predict import predict_eta  

app = Flask(__name__)
CORS(app)

