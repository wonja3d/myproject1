from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import math

client = MongoClient('mongodb://test:test@52.78.46.117', 27017)
# client = MongoClient('localhost', 27017)
db = client.totalad

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scrap')
def scrap():
    return render_template('scrapAD.html')


@app.route('/tvcf', methods=['GET'])
def read_tvcf():
    tvcf_k_list = list(db.tvcfk.find({}, {'_id': 0}))
    tvcf_g_list = list(db.tvcfe.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'tvcf_korea_infos': tvcf_k_list, 'tvcf_global_infos': tvcf_g_list})


@app.route('/scrapread', methods=['GET'])
def read_scrap():
    # c_page = request.args.get('page')
    scrap_list = list(db.scrap.find({}, {'_id': False}))
    db_count = len(scrap_list)
    page_num = math.ceil(db_count / 12)
    return jsonify({'result': 'success', 'scrap_list': scrap_list, 'db_count' : db_count, 'page': page_num})

@app.route('/delscrap', methods=['POST'])
def del_scrap():
    url = request.form.get('url')
    if (db.scrap.find_one({"url":url})) is not None:
        db.scrap.delete_one({"url":url})
        msg = '삭제가 되었습니다.'
    else:
        msg = 'DB에 없음'



    return jsonify({'result': 'success', 'msg' : msg})


@app.route('/scrap', methods=['POST'])
def post_scrap():
    url = request.form.get('url')
    comment = request.form.get('comment')
    lang = request.form.get('lang')

    if lang == 'kr':
        scrap_find = db.tvcfk.find_one({"url": url})
    else:
        scrap_find = db.tvcfe.find_one({"url": url})

    db_num = db.scrap.count()+1

    scrap_data = {'title': scrap_find['title'],
                  'date': scrap_find['date'],
                  'type': scrap_find['type'],
                  'url': scrap_find['url'],
                  'img_url': scrap_find['img_url'],
                  'comment' : comment,
                  'db_num' : db_num
                  }
    if (db.scrap.find_one({"url":url})) is not None:
        msg = '이미 스크랩이 되어있습니다.'
    else:
        db.scrap.insert_one(scrap_data)
        msg = '스크랩 완료'
    return jsonify({'result': 'success', 'msg': msg})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
