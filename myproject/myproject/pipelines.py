import MySQLdb


class MySQLPipeline:
    """
    ItemをMySQLに保存するPipeline。
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にMySQLサーバーに接続する。
        itemsテーブルが存在しない場合は作成する。
        """
        settings = spider.settings  # settings.pyから設定を読み込む。
        params = {
            'host': settings.get('MYSQL_HOST', 'KounoMacBook-Pro.local'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'scraping'),  # データベース名
            'user': settings.get('MYSQL_USER', 'root'),  # ユーザー名
            'passwd': settings.get('MYSQL_PASSWORD', 'Ko021200'),  # パスワード
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)  # MySQLサーバーに接続。
        self.c = self.conn.cursor()  # カーソルを取得。
        # itemsテーブルが存在しない場合は作成。
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `items` (
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `title` VARCHAR(200) NOT NULL,
                `url` VARCHAR(120) NOT NULL,
                `content` VARCHAR(5000) NOT NULL,
                `kimoti` double NOT NULL,
                PRIMARY KEY (`id`)
            )
        """)
        self.conn.commit()  # 変更をコミット。

    def close_spider(self, spider):
        """
        Spiderの終了時にMySQLサーバーへの接続を切断する。
        """
        self.conn.close()

    def process_item(self, item, spider):
        """
        Itemをitemsテーブルに挿入する。
        """
        self.c.execute('insert into items (title,url,content,kimoti) values (%(title)s, %(url)s, %(content)s,%(kimoti)s)', dict(item))
        self.conn.commit()  # 変更をコミット。
        return item
