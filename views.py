from flask import Flask, jsonify
from pnr import PNRClass
from constants import *

app = Flask(__name__)

@app.route('/pnr/v1/<int:pnrno>', methods=['GET'])
def queryPnr(pnrno):
	pnrobject = PNRClass()
	result = pnrobject.queryPnr(pnrno)
	return jsonify(result)

@app.errorhandler(404)
def pageNotFound(error):
	return jsonify({"Status": {"code" : STATUS_INVALID_RESOURCE, "message" : "Invalid resource uri"}})

if __name__ == '__main__':
	app.debug = False
	app.run()

