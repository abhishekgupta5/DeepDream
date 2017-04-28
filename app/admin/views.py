# app/admin/views.py

from flask import abort, flash, redirect, url_for, render_template
from flask_login import current_user, login_required
from . import admin
from .forms import DepartmentForm, RoleForm
from .. import db
from ..models import Department, Role

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
        department = Department(name=form.name.data, description=form.description.data)
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
def edit_department(id):
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
def delete_department(id):
    """Delete a department from the database"""
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted a department.')

    #Redirect to departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

@admin.route("/roles")
@login_required
def list_roles():
    """List all roles"""
    check_admin()

    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Roles')

@admin.route("/roles/add", methods=['GET', 'POST'])
@login_required
def add_role():
    """Add a role to the database"""
    check_admin()
    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)
        try:
            #Add role to the db
            db.session.add(role)
            db.session.commit()
            flash("You've successfully addded a new role.")
        except:
            #In case Role name already exists
            flash("Error: Role name already exists.")
        #Redirects to the to the roles page.
        return redirect(url_for('admin.list_roles'))
    #Load role template
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """Edit a role"""
    check_admin()
    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash("You have successfully edited the role.")

        #redirect to the roles page
        return redirect(url_for('admin.list_roles'))
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Edit Role')

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """Delete a role from the db"""
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash("You've successfully deleted the role.")
    #redirects to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")
