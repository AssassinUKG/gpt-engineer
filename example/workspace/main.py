
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/vulnerabilities'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VulnerabilityDAO:
    def get_all_vulnerabilities(self):
        return Vulnerability.query.all()

    def get_vulnerability_by_id(self, id):
        return Vulnerability.query.get(id)

    def search_vulnerabilities(self, query):
        return Vulnerability.query.filter(Vulnerability.title.contains(query) | Vulnerability.description.contains(query)).all()

    def add_vulnerability(self, vulnerability):
        db.session.add(vulnerability)
        db.session.commit()

    def update_vulnerability(self, vulnerability):
        db.session.commit()

    def delete_vulnerability(self, vulnerability):
        db.session.delete(vulnerability)
        db.session.commit()

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class VulnerabilityForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    severity = StringField('Severity', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    vulnerabilities = VulnerabilityDAO().get_all_vulnerabilities()
    search_form = SearchForm()
    return render_template('index.html', vulnerabilities=vulnerabilities, search_form=search_form)

@app.route('/search', methods=['POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        query = search_form.query.data
        vulnerabilities = VulnerabilityDAO().search_vulnerabilities(query)
        return render_template('search.html', vulnerabilities=vulnerabilities, search_form=search_form)
    flash('Invalid search query')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = VulnerabilityForm()
    if form.validate_on_submit():
        vulnerability = Vulnerability(title=form.title.data, description=form.description.data, severity=form.severity.data)
        VulnerabilityDAO().add_vulnerability(vulnerability)
        flash('Vulnerability added successfully')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    vulnerability = VulnerabilityDAO().get_vulnerability_by_id(id)
    if vulnerability is None:
        flash('Vulnerability not found')
        return redirect(url_for('index'))
    form = VulnerabilityForm(obj=vulnerability)
    if form.validate_on_submit():
        form.populate_obj(vulnerability)
        VulnerabilityDAO().update_vulnerability(vulnerability)
        flash('Vulnerability updated successfully')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    vulnerability = VulnerabilityDAO().get_vulnerability_by_id(id)
    if vulnerability is None:
        flash('Vulnerability not found')
        return redirect(url_for('index'))
    VulnerabilityDAO().delete_vulnerability(vulnerability)
    flash('Vulnerability deleted successfully')
    return redirect(url_for('index'))