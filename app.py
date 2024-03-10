import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('catalog.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/query', methods=['GET'])
def query_catalog_items():
    params = request.args
    if len(params) == 0:
        return "No query string found in the request"
    elif params.keys().__contains__("topic"):
        conn = get_db_connection()
        topic = params["topic"]
        query_res = conn.cursor().execute("SELECT * FROM catalog_item WHERE topic = ?", (topic,))
        return jsonify([dict(row) for row in query_res.fetchall()])
    elif params.keys().__contains__("item_number"):
        conn = get_db_connection()
        item_number = params["item_number"]
        query_res = conn.cursor().execute("SELECT * FROM catalog_item WHERE itemnumber = ?", (item_number,))
        return jsonify(dict(query_res.fetchone()))

    else:
        return "Invalid query parameters"


@app.route('/update', methods=['PATCH'])
def update_catalog_item():
    data = request.json
    if data is None or not data:
        return "Invalid request data"
    if data.keys().__contains__("item_number") and (
            data.keys().__contains__("stock_count") or data.keys().__contains__("cost")):

        if data.keys().__contains__("stock_count"):
            conn = get_db_connection()
            stock_count = data["stock_count"]
            item_number = data["item_number"]
            conn.cursor().execute("UPDATE catalog_item SET count=  count + ? WHERE itemnumber = ?",
                                  (stock_count, item_number))
            conn.commit()
        if data.keys().__contains__("cost"):
            conn = get_db_connection()
            cost = data["cost"]
            item_number = data["item_number"]
            conn.cursor().execute("UPDATE catalog_item SET cost = ? WHERE itemnumber = ?", (cost, item_number))
            conn.commit()
        return "Updated record successfully"
    else:
        return "Invalid request data or missing item number"


if __name__ == '__main__':
    app.run(debug=True)
