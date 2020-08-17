<!DOCTYPE HTML>
<html>
<head>
    <meta charset="utf-8">
    <title>Elasticsearchによる全文検索</title>
    <link rel="stylesheet" href="search.css">
    <style>
    
    </style>
</head>
<body>

    
    <!-- 検索フォーム -->
    <div class="header">
        <div class="header_search">
            <form class="search_field">
                    <div class="logo">
                        <a href="http://localhost:8000/">
                            <img src="test3.png" alt="search" height="30" width="92">
                        </a>
                    </div>
                <div class="box">
                    <input type="text" name="q" class="textbox" value="{{ query }}">
                    <input type="submit" class="search_button" value="🔍">
                </div>
            </form>
        </div>
    </div>
    <!-- 検索カテゴリ　-->
    <div class="category">
        <div class="all">
            <a href="http://localhost:8000/?q={{ query }}"><p>🔍全て</p></a>
        </div>

        <div class="know">
            <a href="http://localhost:8000/?q={{ query }}&p=words"><p>知る</p></a>
        </div>

        <div class="watch">
            <a href="http://localhost:8000/?q={{ query }}&p=images"><p>見る</p></a>
        </div>
    </div>


    <!-- 検索結果 -->
    <% for page in pages: %>
    <div class="search">
        <h3><a href="{{ page["_source"]["url"] }}">{{ page["_source"]["title"] }}</a></h3>
        <div class="link">{{ page["_source"]["url"] }}</div>
        <% try: %>
        <div class="fragment">{{! page["highlight"]["content"][0] }}</div>
        <% except : %>
        <p>なし</p>
    <% end %>
    </div>
</body>
</html>
