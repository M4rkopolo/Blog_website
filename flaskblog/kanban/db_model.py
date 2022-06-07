from flask import Blueprint
from flaskblog import db
from flaskblog.util.utils import PSTNow
from flask_wtf import FlaskForm


class Note(db.Model):
    __tablename__ = "kanban_note"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    stage_name = db.Column(db.String(30), db.ForeignKey('kanban_stage.name'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String, default=PSTNow)
    kanban_table = db.Column(db.Integer, db.ForeignKey('kanban_table.id'))

    def __init__(self, content, stage_name, user_id,kanban_table):
        self.content = content
        self.stage_name = stage_name
        self.user_id = user_id
        self.kanban_table = kanban_table


class Stage(db.Model):
    __tablename__ = "kanban_stage"

    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship("Note", backref="stage")
    name = db.Column(db.String(30), nullable=False)
    inside_kanban_table = db.Column(db.Integer, db.ForeignKey('kanban_table.id'))


# user_name = db.Column(db.String, db.ForeignKey(user_name))

class Kanban_Table(db.Model):
    __tablename__ = "kanban_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String)
    stages = db.relationship("Stage", backref="kanban_table")
    notes = db.relationship("Note", backref="kanban_notes")
    owner_user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
    # access_users_name = db.Column(db.String, db.ForeignKey('users.user_name'))
