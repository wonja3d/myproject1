from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.totalad

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tvcf', methods=['GET'])
def read_tvcf():
    tvcf_k_list = list(db.tvcfk.find({},{'_id':False}))
    tvcf_g_list = list(db.tvcfe.find({},{'_id':False}))
    return jsonify({'result': 'success', 'tvcf_korea_infos': tvcf_k_list, 'tvcf_global_infos' : tvcf_g_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
