from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOADED_REQUIREMENTS_DEST'] = 'uploads/requirements'
db = SQLAlchemy(app)
uploads = UploadSet('requirements', DOCUMENTS)
configure_uploads(app, uploads)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    table_title = db.Column(db.String(100))
    table_text = db.Column(db.String(200))
    literature = db.Column(db.String(100))
    requirements_file = db.Column(db.String(100), nullable=True)

@app.route('/')
def index():
    templates = Template.query.all()
    return render_template('index.html', templates=templates)

@app.route('/create_template', methods=['GET', 'POST'])
def create_template():
    if request.method == 'POST':
        name = request.form['name']
        table_title = request.form['table_title']
        table_text = request.form['table_text']
        literature = request.form['literature']
        requirements_file = request.files['requirements_file']
        if requirements_file:
            filename = uploads.save(requirements_file)
        else:
            filename = None
        template = Template(name=name, table_title=table_title, table_text=table_text,
                            literature=literature, requirements_file=filename)
        db.session.add(template)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_template.html')

@app.route('/edit_template/<int:template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    template = Template.query.get(template_id)
    if request.method == 'POST':
        template.name = request.form['name']
        template.table_title = request.form['table_title']
        template.table_text = request.form['table_text']
        template.literature = request.form['literature']
        requirements_file = request.files['requirements_file']
        if requirements_file:
            filename = uploads.save(requirements_file)
            template.requirements_file = filename
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_template.html', template=template)

@app.route('/delete_template/<int:template_id>')
def delete_template(template_id):
    template = Template.query.get(template_id)
    if template.requirements_file:
        uploads.delete(template.requirements_file)
    db.session.delete(template)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/requirements/<filename>')
def requirements_file(filename):
    return send_from_directory(app.config['UPLOADED_REQUIREMENTS_DEST'], filename)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
