import sqlite3
from flask import Flask, render_template, request
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)  # 初始化Freezer



@app.route("/")
def index():
    return render_template("home.html")


@app.route("/home")
def home():
    return index()


# @app.route("/table")
# def table():
#     datalist = []
#     con = sqlite3.connect("movie.db")
#     cur = con.cursor()
#     sql = "select * from top250"
#     data = cur.execute(sql)
#     for item in data:
#         datalist.append(item)
#     cur.close()
#     con.close()
#     return render_template("table.html", movies=datalist)


@app.route("/table")
def table():
    # 获取分页参数（默认为第1页，每页20条）
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    # 计算偏移量
    offset = (page - 1) * per_page

    datalist = []
    con = sqlite3.connect("movie.db")
    cur = con.cursor()

    # 查询总数据量
    cur.execute("SELECT COUNT(*) FROM top250")
    total_count = cur.fetchone()[0]

    # 分页查询当前页数据
    sql = "SELECT * FROM top250 LIMIT ? OFFSET ?"
    data = cur.execute(sql, (per_page, offset))

    for item in data:
        datalist.append(item)

    cur.close()
    con.close()

    # 计算总页数
    total_pages = (total_count + per_page - 1) // per_page

    return render_template(
        "table.html",
        movies=datalist,
        current_page=page,
        total_pages=total_pages,
        total_count=total_count,
        per_page=per_page,
    )

    # TBC
    # @app.route("/chart")
    # def chart():
    #     con = sqlite3.connect("movie.db")
    #     cur = con.cursor()

    #     # 简化：只获取评分分布数据
    #     sql = """
    #     SELECT
    #         CASE
    #             WHEN rating >= 9.0 THEN '9.0-10.0'
    #             WHEN rating >= 8.0 THEN '8.0-9.0'
    #             WHEN rating >= 7.0 THEN '7.0-8.0'
    #             WHEN rating >= 6.0 THEN '6.0-7.0'
    #             ELSE '6.0以下'
    #         END as score_range,
    #         COUNT(*) as count
    #     FROM top250
    #     GROUP BY
    #         CASE
    #             WHEN rating >= 9.0 THEN '9.0-10.0'
    #             WHEN rating >= 8.0 THEN '8.0-9.0'
    #             WHEN rating >= 7.0 THEN '7.0-8.0'
    #             WHEN rating >= 6.0 THEN '6.0-7.0'
    #             ELSE '6.0以下'
    #         END
    #     ORDER BY MIN(rating) DESC
    #     """

    #     cur.execute(sql)
    #     score_distribution = cur.fetchall()

    #     # 获取平均评分
    #     cur.execute("SELECT AVG(rating) FROM top250")
    #     avg_score = cur.fetchone()[0]

    #     cur.close()
    #     con.close()

    #     # 转换为列表格式
    #     categories = [item[0] for item in score_distribution]
    #     counts = [item[1] for item in score_distribution]

    #     return render_template(
    #         "chart_simple.html",
    #         categories=categories,
    #         counts=counts,
    #         avg_score=round(avg_score, 2) if avg_score else 0,
    #         total_movies=sum(counts)
    #     )

    # @app.route("/wordcloud")
    # def word_cloud():
    return render_template("wordcloud.html")


@app.route("/team")
def team():
    return render_template("team.html")


if __name__ == "__main__":
    freezer.freeze()