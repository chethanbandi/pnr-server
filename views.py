from flask import Flask, jsonify
from pnr import PNRClass
from constants import *
from responsecodes import *

app = Flask(__name__)

@app.route('/pnr/v1/<int:pnrno>', methods=['GET'])
def queryPnr(pnrno):
	pnrobject = PNRClass()
	result = pnrobject.queryPnr(pnrno)
	return jsonify(result)

@app.errorhandler(404)
def pageNotFound(error):
	return jsonify({"Status": {"code" : RESPONSE_CODE_INVALID_RESOURCE, "message" : RESPONSE_MESSAGE_INVALID_RESOURCE}})

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5000, debug=True)

