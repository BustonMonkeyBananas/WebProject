from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField, StringField

class JobForm(FlaskForm):
    team_leader = IntegerField('Id руководителя')
    job = StringField('Описание работы')
    work_size = IntegerField('Обьем работы в часах')
    collaborators = StringField('Участники работы')
    is_finished = BooleanField('Работа завершена')
    submit = SubmitField('Добавить')