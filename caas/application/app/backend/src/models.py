from flask_marshmallow import Marshmallow
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

# Init db
db = SQLAlchemy()
# Init ma
ma = Marshmallow()


# model definition
class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column('id', db.Integer, primary_key=True)
    item = db.Column('item', db.String(50))
    is_done = db.Column('is_done', db.Boolean)

    def __repr__(self):
        return '<Tasks id={id} item={item!r} is_done={is_done}>'.format(
                id=self.id, item=self.item, is_done=self.is_done)

    def __init__(self, item, is_done=False):
        self.item = item
        self.is_done = is_done

    # validation for item
    @validates('item')
    def validate_item(self, key, item):
        if not item:
            raise AssertionError('No item provided')
        if len(item) < 1:
            raise AssertionError('Todo item must NOT be blank')
        if len(item) > 50:
            raise AssertionError('Todo item must NOT be greater than 50')

        return item


# Schema by Marshmallow for json serialization purpose.
class TasksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'item', 'is_done')
