from waitress import serve

import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#
# For local hosting
#
if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8181, debug=True)
    serve(app, host='0.0.0.0', port=80)