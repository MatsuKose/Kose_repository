<!DOCTYPE HTML>
<html>
<head>
    <meta charset="utf-8">
    <title>Elasticsearchによる全文検索</title>
    <link rel="stylesheet" href="search_results.css">
    <style>
    </style>
</head>
<body>

    
    <!-- 検索フォーム -->
    <div class="search_top">
        <form class="search_field">
                <!--
                <div class="logo">
                    <a href="http://localhost:8000/">
                        <img src="test3.png" alt="search" height="30" width="92">
                    </a>
                </div>-->
            <div class="box">
                <input type="text" name="q" class="textbox" value="{{ query }}">
                <input type="submit" class="search_button" value="🔍">
            </div>
        </form>
    </div>
    <!-- 検索カテゴリ　-->
    <div class="category">
        <div class="a all">
            <a href="http://localhost:8000/?q={{ query }}" style="color:blue;"><p>🔍全て</p></a>
        </div>

        <div class="a know">
            <a href="http://localhost:8000/?q={{ query }}&p=words"><p>知る</p></a>
        </div>

        <div class="a watch">
            <a href="http://localhost:8000/?q={{ query }}&p=images"><p>見る</p></a>
        </div>
        <div class="a buy">
            <a href="http://localhost:8000/?q={{ query }}&p=buy"><p>買う</p></a>
        </div>
        <div class="a eat">
            <a href="http://localhost:8000/?q={{ query }}&p=eat"><p>食べる</p></a>
        </div>


        <div class="netui">
            <div class="netui-1">
                <a href="http://localhost:8000/?q={{ query }}&p=netui-1" style="color:{{color1}};"><p>熱意なし</p></a>
            </div>
            <div class="netui1">
                <a href="http://localhost:8000/?q={{ query }}&p=netui1" style="color:{{color2}};"><p>熱意Level1</p></a>
            </div>
            <div class="netui2">
                <a href="http://localhost:8000/?q={{ query }}&p=netui2" style="color:{{color3}};"><p>熱意Level2</p></a>
            </div>
            <div class="netui3">
                <a href="http://localhost:8000/?q={{ query }}&p=netui3" style="color:{{color4}};"><p>熱意Level3</p></a>
            </div>
        </div>
    </div>


    <!-- 検索結果 -->
    <% for i,page in enumerate(pages): %>
        <div class="search"> 
            <div class="result">
                <h3><a href="{{ page["_source"]["url"] }}">{{ page["_source"]["title"] }}</a></h3>
                <div class="link">{{ page["_source"]["url"] }}</div>
                <% try: %>
                <div class="fragment">{{! page["highlight"]["content"][0] }}</div>
                <% except : %>
                <p>なし</p>
    <% end %>
            </div>
        </div>
</body>
</html>
