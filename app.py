from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database to use MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'mysql://lambton:admin123@db/student_groups')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 120

db = SQLAlchemy(app)

# Define the GroupSelection model
class GroupSelection(db.Model):
    group_id = db.Column(db.String(255), primary_key=True)  # Unique group names
    remaining_seats = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<GroupSelection {self.group_id}>"

# Define the StudentSelection model
class StudentSelection(db.Model):
    student_id = db.Column(db.String(255), primary_key=True)  # Student ID as primary key
    group_id = db.Column(db.String(255), db.ForeignKey('group_selection.group_id'), nullable=False)  # Foreign key

    # Unique constraint on student_id and group_id to avoid duplicate entries
    __table_args__ = (db.UniqueConstraint('student_id', 'group_id', name='student_group_uc'),)

    def __repr__(self):
        return f"<Selection Student {self.student_id} Group {self.group_id}>"

# Initialize the database with two groups
def init_db():
    db.create_all()
    
    # Check if the groups already exist to avoid duplicating them
    if not GroupSelection.query.first():
        group1 = GroupSelection(group_id="Group A", remaining_seats=1000000000)
        group2 = GroupSelection(group_id="Group B", remaining_seats=1000000000)
        
        db.session.add(group1)
        db.session.add(group2)
        db.session.commit()

@app.route('/')
def index():
    groups = GroupSelection.query.all()
    return render_template('index.html', groups=groups)

@app.route('/select', methods=['POST'])
def select_group():
    student_id = request.form.get('student_id')
    selected_group_id = request.form.get('group_id')
    if student_id and selected_group_id:
        # Fetch the selected group
        selected_group = GroupSelection.query.get(selected_group_id)

        # Check if the group has available seats
        if selected_group.remaining_seats > 0:
            # Check if the student already has a group selection
            existing_selection = StudentSelection.query.filter_by(student_id=student_id).first()

            if existing_selection:
                # If the student already has a selection, get the previous group
                previous_group = GroupSelection.query.get(existing_selection.group_id)

                # Increase seats of the previous group
                previous_group.remaining_seats += 1

                # Remove the student's old selection
                db.session.delete(existing_selection)

            # Decrease seats of the new group
            selected_group.remaining_seats -= 1

            # Add the new group selection for the student
            new_selection = StudentSelection(student_id=student_id, group_id=selected_group_id)
            db.session.add(new_selection)
            db.session.commit()

            return redirect(url_for('index'))

    return redirect(url_for('index'))

# New route to check the student's selected group
@app.route('/check_selection', methods=['GET', 'POST'])
def check_selection():
    if request.method == 'POST':
        student_id = request.form.get('student_id')

        # Find the student's selected group
        selection = StudentSelection.query.filter_by(student_id=student_id).first()

        if selection:
            # Fetch the group details based on group_id
            selected_group = GroupSelection.query.get(selection.group_id)
            return render_template('check_selection.html', selected_group=selected_group)
        else:
            message = "No group selection found for this student ID."
            return render_template('check_selection.html', message=message)

    return render_template('check_selection.html')

if __name__ == '__main__':
    with app.app_context():
        # Initialize the database with groups
        init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
