import subprocess

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from models import Tasks, TasksSchema, db

# For easy JSON formatting
task_schema = TasksSchema(strict=True)
tasks_schema = TasksSchema(many=True, strict=True)


# endpoint /tasks
class TaskList(Resource):

    # List all of the tasks
    def get(self):
        try:
            all_tasks = Tasks.query.all()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error_msg": str(e)}, 403
        return tasks_schema.jsonify(all_tasks)

    # validation check in model
    def post(self):
        try:
            task_dict = request.get_json(force=True)
            new_task = Tasks(task_dict['item'])
            db.session.add(new_task)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error_msg": str(e)}, 403

        return task_schema.jsonify(new_task)


class Task(Resource):

    def get(self, id):
        # if not valid id, response 404
        try:
            task = Tasks.query.get_or_404(id)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error_msg": str(e)}, 403

        return task_schema.jsonify(task)

    def delete(self, id):
        # if not valid id, response 404
        try:
            task = Tasks.query.get_or_404(id)
            db.session.delete(task)
            db.session.commit()
        except AttributeError:
            return {"error_msg": "id not existing"}, 404
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error_msg": str(e)}, 403

        return {"message": "Deleted"}, 204

    def put(self, id):
        # if not valid id, response 404
        task = Tasks.query.get_or_404(id)
        task_dict = request.get_json(force=True)
        try:
            task_schema.validate(task_dict)
            for key, value in task_dict.items():
                setattr(task, key, value)

            db.session.commit()
            return self.get(id)

        except AttributeError:
            return {"error_msg": "id not existing"}, 404
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error_msg": str(e)}, 403

        return task_schema.jsonify(task)


class Initialization(Resource):
    """
    Init DB before benchmarking
    """

    def get(self):
        res = subprocess.call('./init.sh')
        if res == 0:
            return "OK"
        else:
            return "NG", 500
