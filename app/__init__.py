from flask import Flask
import matplotlib
app = Flask(__name__)

from app import routes


if __name__ == '__main__':
    app.run(debug=True)
    matplotlib.use('SVG')
