from flask import Flask, redirect,render_template,url_for
from flask_bootstrap import Bootstrap
from werkzeug.security  import generate_password_hash, check_password_hash
