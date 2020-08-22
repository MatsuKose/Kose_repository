from typing import List  # 型ヒントのためにインポート
import re
from elasticsearch import Elasticsearch
from bottle import route, run, request, template, static_file

from myproject.myproject.standard.resipi import resi
from myproject.myproject.standard.kau import kau
from myproject.myproject.standard.taberu import taberu
from myproject.myproject.standard.netui import netui
import random
import collections
import MeCab
from operator import itemgetter

es = Elasticsearch(['localhost:9200'])

@route('/<filename:path>')  #静的ファイルを使う
def send_static(filename):
    return static_file(filename, root='')


@route('/')
def index():
    """
    / へのリクエストを処理する。
    """
    query = request.query.q # クエリ（?q= の値）を取得する。

    
    # クエリがある場合は検索結果を、ない場合は[]をpagesに代入する。
    pages = search_pages(query) if query else []


    l = []
    r = []

    # Bottleのテンプレート機能を使って、search.tplというファイルから読み込んだテンプレートに
    # queryとpagesの値を渡してレンダリングした結果をレスポンスボディとして返す。
    return template('search', query=query, pages=pages) #search.tqlにqueryとpagesを渡す

def netui():
    query = request.query.p
    n1 = -10
    n2 = 10
    if query == "netui-1":
        n1 = -1.0
        n2 = 0.04
    elif query == "netui1":
        n1 = 0.04
        n2 = 0.06
    elif query == "netui2":
        n1 = 0.06
        n2 = 0.18
    elif query == "netui3":
        n1 = 0.18
        n2 = 5.0
    
    return n1 , n2

def search_pages(query: str) -> List[dict]:


    n1,n2 = netui()


    """
    引数のクエリでElasticsearchからWebページを検索し、結果のリストを返す。
    """
    result = es.search(index='pages', body={
        "size": 100,    #出す件数
        "_source": [    #使用するフィールドを決める（分かりやすい
            "url",
            "title",
            "content",
            "kimoti"
        ],
        "query": {  #検索基準作ります
            "bool": {   #複数作ります
                "must": {   #どれぐらい一致しているかでスコアが変わる
                
                    "multi_match" : { #キーワードにマッチ（マッチ複数
                        "query":    query,  #キーワード 
                        "fields": [ "title^5", "content"]   #キーワードのターゲット
                    }
                },
                "filter":{
                    "range": {
                        "kimoti": {
                                "gte":n1,
                                "lt":n2
                        }
                    }
                }
            }
        },
        # contentフィールドでマッチする部分をハイライトするよう設定。
        "highlight": {
            "fields": {
                "content": {
                    "fragment_size": 150,
                    "number_of_fragments": 1,
                    "no_match_size": 150
                }
            }
        }
    })

    
    query = request.query.p
    if query == "words":
        m = []
        for i,n in enumerate(result['hits']['hits']):
            m.append(result['hits']['hits'][i]['_source']['hinshi'])
        c = zip(result['hits']['hits'], m)  #まとめる
        c = sorted(c, key = lambda x: x[1],reverse=True)    #hinshiを基準に並び替え
        #a, b = list(zip(*c)) タプル型になってしまう
        result['hits']['hits'], b = list(map(list, (zip(*c))))   #元の形で返す

    """if query == "images":
        m = []
        for i,n in enumerate(result['hits']['hits']):
            m.append(result['hits']['hits'][i]['_source']['count_image'])
        c = zip(result['hits']['hits'], m)  #まとめる
        c = sorted(c, key = lambda x: x[1],reverse=True)    #count_imageを基準に並び替え
        #a, b = list(zip(*c)) タプル型になってしまう
        result['hits']['hits'], b = list(map(list, (zip(*c))))   #元の形で返す

    if query == "buy":
        count = 0
        l = []
        for i,n in enumerate(result['hits']['hits']):
            m = kau(result['hits']['hits'][i]['_source']['content'])
            if m != []:
                print(m)
                print(result['hits']['hits'][i]['_source']['title'])
                l.append(result['hits']['hits'][i])
                count += 1
        print(count)
        del result['hits']['hits'][:]
        result['hits']['hits'] = l

    if query == "eat":
        l = []
        b = []
        for i,n in enumerate(result['hits']['hits']):
            m = taberu(result['hits']['hits'][i]['_source']['content'])
            if m != []:
                print(m)
                print(result['hits']['hits'][i]['_source']['title'])
                l.append(result['hits']['hits'][i])
                b.append(len(m))
        print(b)
        del result['hits']['hits'][:]
        result['hits']['hits'] = l

        c = zip(result['hits']['hits'], b)  #まとめる
        c = sorted(c, key = lambda x: x[1],reverse=True)    #単語数を基準に並び替え
        result['hits']['hits'], a = list(map(list, (zip(*c))))   #元の形で返す

    netuikun = []
    for i,n in enumerate(result['hits']['hits']):
        n = netui(result['hits']['hits'][i]["_source"]["content"])
        netuikun.append(n)
        print(n,len(result['hits']['hits']),len(netuikun))

    c = zip(result['hits']['hits'], netuikun)  #まとめる
    c = sorted(c, key = lambda x: x[1],reverse=True)
    a, b = list(map(list, (zip(*c))))   #元の形で返す
    for i,n in enumerate(a):
        print(a[i]['_source']['title'])"""
        
        
        


    for i,n in enumerate(result['hits']['hits']):   #本当はクローリング時にやる事
        title = result['hits']['hits'][i]['_source']['title']
        url = result['hits']['hits'][i]['_source']['url']
        if len(title) >= 30:
            result['hits']['hits'][i]['_source']['title'] = title[:30] + "......"
        if len(url) >= 70:
            result['hits']['hits'][i]['_source']['url'] = url[:70] + "...."


    print("最初だよ!!!!!!")
    def keykun(result,kazu):
        for key, value in zip(result.keys(), result.values()):
            #テスト-----------------
            nakami = ""
            if len(str(value)) < 41:  #タイトルが40文字だったので
                nakami = "　　　　|" + str(value)
            else:
                nakami = "　　　　|" #文字が長すぎる
            #-----------------------
            print("　"*kazu +"┗" + key + nakami)

            if isinstance(value, dict):
                keykun(value,kazu+1)
            
            if isinstance(value, list):
                for i,d in enumerate(value):
                    print("検索 {}".format(i+1)) if key == "hits" else  print("")
                    if isinstance(d, dict):
                        keykun(d,kazu+1)

    keykun(result,1)

    #print(result['hits']['hits'])
    return result['hits']['hits']

if __name__ == '__main__':
    # 開発用のHTTPサーバーを起動する。
    run(host='0.0.0.0', port=8000, debug=True, reloader=True)
