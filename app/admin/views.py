# app/admin/views.py

from flask import abort, flash, redirect, url_for, render_template,
from flask_login import current_user, login_required
from . import admin
from forms import DepartmentForm
from .. import db
from ..models import Department

def check_admin():
    """Prevent non-admins from accessing this page"""
    if not current_user.is_admin:
        abort(403)

#Department views
@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """List all departments"""
    check_admin()
    departments = Department.query.all()

    return render_template('admin/departments/departments.html', departments=departments, title='Departments')

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """Add a department to the database"""
    check_admin()
    add_department = True
    form = DepartmentForm()

    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.descrioption.data)
        try:
            #Add department to the database
            db.session.add(department)
            db.session.commit()
            flash("You've successfully added a new Department.")
        except:
            #In case department name already exists
            flash("Error: Department name aready exists.")

        #Redirects to departments page
        return redirect(url_for('admin.list_departments'))

    #Load Department template
    return render_template('admin/departments/department.html', action='Add', add_department=add_department, form=form, title='Add Department')

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department():
    """Edit a department"""
    check_admin()
    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash("You have successfully edited a department.")

        #Redirect to the departments page
        return redirect(url_for('admin.list_departments'))
    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action='Edit', add_department=add_department, form=form, department=department, title='Edit Department')

@admin.route('/departments/delete<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department():
    """Delete a department from the database"""
    check_admin()

    department = Department.query.get_or_404(id):
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted a department.')

    #Redirect to departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")
