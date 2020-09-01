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
            <div class="logo">
                <a href="http://localhost:8000/">
                    <img src="yamato2.png" alt="search" height="40" width="100">
                </a>
            </div>
            <div class="box">
                <div class="space">
                    <input type="text" name="q" class="textbox" value="{{ query }}">
                    <input type="submit" class="search_button" value="🔍">
                </div>
            </div>
        </form>
    </div>
    <!-- 検索カテゴリ　-->
    <div class="search_bar">
        <div class="category">
            <ul class="items">
                <li class="a all">
                    <a href="http://localhost:8000/?q={{ query }}" style="color:blue;"><p>全て</p></a>
                </li>

                <li class="a know">
                    <a href="http://localhost:8000/?q={{ query }}&p=words"><p>知る</p></a>
                </li>

                <li class="a watch">
                    <a href="http://localhost:8000/?q={{ query }}&p=images"><p>見る</p></a>
                </li>
                <li class="a buy">
                    <a href="http://localhost:8000/?q={{ query }}&p=buy"><p>買う</p></a>
                </li>
                <li class="a eat">
                    <a href="http://localhost:8000/?q={{ query }}&p=eat"><p>食べる</p></a>
                </li>
            </ul>
        </div>
    </div>

    <div class="netui" style="background-color:{{color0}};">
        <div class="n -1">
            <a class="netu -1" href="http://localhost:8000/?q={{ query }}&p=netui-1" style="color:{{color1}};"><p>冷静</p></a>
        </div>
        <div class="n 1">
            <a class="netu 1" href="http://localhost:8000/?q={{ query }}&p=netui1" style="color:{{color2}};"><p>ちょっと熱い</p></a>
        </div>
        <div class="n 2">
            <a class="netu 2" href="http://localhost:8000/?q={{ query }}&p=netui2" style="color:{{color3}};"><p>情熱</p></a>
        </div>
        <div class="n 3">
            <a class="netu 3" href="http://localhost:8000/?q={{ query }}&p=netui3" style="color:{{color4}};"><p>激しく燃える</p></a>
        </div>
    </div>

    <div class="result_field">
        <!-- 検索結果 -->
        <% for i,page in enumerate(pages): %>
            <div class="search"> 
                <div class="result">
                    <h3><a class="page_link" href="{{ page["_source"]["url"] }}">{{ page["_source"]["title"] }}</a></h3>
                    <div class="link">{{ page["_source"]["url"] }}</div>
                    <% try: %>
                    <div class="fragment">{{! page["highlight"]["content"][0] }}</div>
                    <% except : %>
                    <p>なし</p>
                    <div class="search_bar">
        <% end %>
                    </div>
                </div>
            </div>
    </div>
</body>
</html>
