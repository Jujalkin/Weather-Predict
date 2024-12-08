from flask import Flask, render_template, request
import requests
import os
from config import API_KEY

app = Flask(__name__)