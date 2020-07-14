from flask_script import Manager
from flask import Flask, render_template, request,  send_from_directory, abort, jsonify
import os
app = Flask(__name__, template_folder="templates",static_folder="static",static_url_path="/static")
UPLOAD_FOLDER = 'static'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
manager	= Manager(app)

@app.route("/",methods=["POST", "GET"])
def upload():
    if request.method == "GET":
        return render_template("up.html")
    else:
        file_dir = os.path.join(BASE_DIR, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['photo']
        if f is not None:
            f.save(os.path.join(file_dir,f.filename))
            return jsonify({"success":"success"})
        else:
            return "请选择文件"

if __name__ == "__main__":
#    app.run(host="0.0.0.0",port=80)
    manager.run()
