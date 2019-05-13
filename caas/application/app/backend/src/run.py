from flask import Flask
from flask_restful import Api
from apis import TaskList, Task, Initialization


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # init path with routing
    api = Api(app)
    api.add_resource(TaskList, '/tasks')
    api.add_resource(Task, '/tasks/<int:id>')
    api.add_resource(Initialization, '/initialize')

    # init db
    from models import db
    db.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=9200, debug=True)
