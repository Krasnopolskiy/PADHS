import logging
from functools import reduce

from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/process", methods=["POST"])
def compute():
    data = request.get_json()
    product = reduce(lambda x, y: x * y, data["numbers"])
    logger.info("Computed: %s", product)
    return jsonify(product)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
