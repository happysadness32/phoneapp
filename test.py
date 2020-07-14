from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sqlite3
import os
app = Flask(__name__, template_folder="templates",static_folder="static", static_url_path="/static")
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api
UPLOAD_FOLDER = 'static'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route("/",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("up.html")
    else:
        file_dir = os.path.join(BASE_DIR, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['photo']
        if f is not None:
            f.save(os.path.join(file_dir, f.filename))
            conn = sqlite3.connect("info.db")
            cur = conn.cursor()
            cur.execute("UPDATE config SET name=? WHERE id=?", (f.filename, 1))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"success":0,"msg":"上传成功"})
        else:
            return "请选择文件"




@app.route("/config/set/<state>")
def setState(state):
    conn = sqlite3.connect("info.db")
    cur = conn.cursor()
    cur.execute("UPDATE config SET state=? WHERE id=?", (state, 1))
    conn.commit()
    cur.close()
    conn.close()

    return "success"

@app.route("/config/setvalue/<state>")
def setValuestate(state):
    conn = sqlite3.connect("info.db")
    cur = conn.cursor()
    cur.execute("UPDATE config SET name=? WHERE id=?", (state, 1))
    conn.commit()
    cur.close()
    conn.close()

    return "success"

@app.route('/cmt', methods=['GET'])
def get_cmt():
    conn = sqlite3.connect("info.db")
    cur = conn.cursor()
    cur.execute("select * from config where id= ?", (1,))
    state = cur.fetchone()
    cur.close()
    conn.close()
    context = jsonify(
        code=200,
        data=
            {"state": str(state[2]),
             "name": str(state[1])
             },
        )
    return context

if __name__ == '__main__':
    app.run(debug=True)
