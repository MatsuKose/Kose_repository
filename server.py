from typing import List  # 型ヒントのためにインポート

from elasticsearch import Elasticsearch
from bottle import route, run, request, template

es = Elasticsearch(['localhost:9200'])


@route('/')
def index():
    """
    / へのリクエストを処理する。
    """
    query = request.query.q  # クエリ（?q= の値）を取得する。
    # クエリがある場合は検索結果を、ない場合は[]をpagesに代入する。
    pages = search_pages(query) if query else []
    # Bottleのテンプレート機能を使って、search.tplというファイルから読み込んだテンプレートに
    # queryとpagesの値を渡してレンダリングした結果をレスポンスボディとして返す。
    return template('search', query=query, pages=pages)


def search_pages(query: str) -> List[dict]:
    """
    引数のクエリでElasticsearchからWebページを検索し、結果のリストを返す。
    """
    # Simple Query Stringを使って検索する。
    result = es.search(index='pages', body={
        "query": {
            "simple_query_string": {
                "query": query,
                "fields": ["title^5", "content"],
                "default_operator": "and"
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


    print(result['hits']['hits'])
    return result['hits']['hits']

if __name__ == '__main__':
    # 開発用のHTTPサーバーを起動する。
    run(host='0.0.0.0', port=8000, debug=True, reloader=True)
