#!/usr/bin/python3
# vim: set fileencoding=utf8
#
# Usage: synonyms/scripts/restapi.py DICT UMATRIX SMATRIX PORT
#
# Example: synonyms/scripts/restapi.py data_synonyms/nametag.1.LR.dict data_synonyms/nametag.1.LR.ppmi.mat.10000.svd.U.npz data_synonyms/nametag.1.LR.ppmi.mat.10000.svd.s.npz 5060
# curl -H 'Content-Type: application/json; charset="utf-8"' -X POST -d '{"word": "manžel"}' http:/localhost:5060/synonyms; echo

import sys
sys.path.append('.')

from flask import *
import numpy as np
from scipy.io import mmread

from synonyms.dictionary import Dictionary
from synonyms.synonyms import SVDModel


app = Flask(__name__)


@app.route('/synonyms', methods=['POST'])
def get_synonyms():
    if not request.json['word']:
        return jsonify({'syn': []}), 200

    word = request.json['word']
    k = request.json.get('k', 10)

    synonyms, ids, score = model.get_synonyms(word, k, return_ids=True, return_score=True)

    return jsonify({'syn': [{'word': syn, 'score': sc} for syn, sc in zip(synonyms, score)]}), 200


if __name__ == "__main__":
    print(sys.argv[1])
    dictionary = Dictionary(filename=sys.argv[1])
    print(sys.argv[3])
    s = np.load(sys.argv[3])['arr_0']
    print(sys.argv[2])
    U = np.load(sys.argv[2])['arr_0']
    print('SVDModel')
    model = SVDModel(U, s, dictionary)
    model.dimensions = 2500
    model.caron_p = 0.25

    print("Running...")
    app.run(port=int(sys.argv[4]), host='::', debug=True, use_reloader=True)
