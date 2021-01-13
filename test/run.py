import flask
from api.controllers import taskController, deskController

app = flask.Flask(__name__, template_folder="api/templates")
app.config["DEBUG"] = True

app.secret_key = "key"

@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return flask.render_template("index.html")

app.register_blueprint(taskController.task_page)
app.register_blueprint(deskController.desk_page)

app.run()