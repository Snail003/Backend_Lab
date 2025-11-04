from flask import Flask

app = Flask(__name__)

import myapp.views
import myapp.user
import myapp.category
import myapp.record