from flask import Flask, jsonify, request
from pnr import PNRClass
from constants import *
from responsecodes import *
from models.pnrstats import *

app = Flask(__name__)

@app.route('/pnr/v1/<int:pnrno>', methods=['GET'])
def queryPnr(pnrno):
	userAgent = request.headers.get('User-Agent')
	remoteAddress = request.remote_addr

	pnrStats = PNRStats()
	pnrStats.open()

	pnrStatsId = pnrStats.save(pnrno, userAgent, remoteAddress)

	pnrobject = PNRClass()
	result = pnrobject.queryPnr(pnrno)

	code = result["Status"]["code"]
	message = result["Status"]["message"]

	pnrStats.update(pnrStatsId, code, message)
	pnrStats.close()

	return jsonify(result)

@app.errorhandler(404)
def pageNotFound(error):
	return jsonify({"Status": {"code" : RESPONSE_CODE_INVALID_RESOURCE, "message" : RESPONSE_MESSAGE_INVALID_RESOURCE}})

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5000, debug=True)

