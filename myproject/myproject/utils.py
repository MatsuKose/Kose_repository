import logging
from typing import Tuple

import lxml.html
import readability
from bs4 import BeautifulSoup  # BeautifulSoupクラスをインポート
import MeCab
import collections


# readability-lxmlのDEBUG/INFOレベルのログを表示しないようにする。
# Spider実行時にreadability-lxmlのログが大量に表示されて、ログが見づらくなるのを防ぐため。
logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html: str) -> Tuple[str, str]:
    """
    HTMLの文字列から (タイトル, 本文) のタプルを取得する。
    """
    document = readability.Document(html)
    content_html = document.summary()
    # HTMLタグを除去して本文のテキストのみを取得する。
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    #Mecab-----

    l = []
    mecabTagger = MeCab.Tagger("-Ochasen")
    node = mecabTagger.parseToNode(content_text)
    while node:
        word = node.surface
        l.append(word) if word != "" else print("")
        node = node.next

    return short_title, content_text, len(l)

def bs4_test(html: str) -> Tuple[str, str]:
    soup = BeautifulSoup(html)
    count_img=len(soup.find_all("img")) #画像の枚数
    #デバッグポイントを設置
    # import pdb;pdb.set_trace()
    
    return count_img
