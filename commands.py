import click

from api import app, db
from api.models.user import UserModel


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:") or 'admin'
    password = input("Password[default 'admin']:") or 'admin'
    user = UserModel(username, password, role="admin", is_staff=True)
    user.save()
    if user.id:
        print(f"Superuser create successful! id={user.id}")
    else:
        print(f"Superuser with name {user.username} already exist!")


@app.cli.command('user')
@click.argument('param', type=click.Choice(['create', 'delete', 'show-all'], case_sensitive=False))
@click.option('--all', is_flag=True, help='Delete all users')
def create_superuser(param, all):
    """
    Run user [create/delete/show-all]
    """
    if param == 'show-all':
        users = UserModel.query.all()
        for user in users:
            print(f"User id: {user.id} {user.username}")
    elif param == 'delete':
        if all:
            res = input("Do you want delete all users from DB?(y/n)") or 'n'
            if res == 'y':
                UserModel.query.delete()
                db.session.commit()
                print("All users deleted from DB!")
            return

        username = input("Enter user name:")
        note = UserModel.query.filter_by(username=username).first()
        if not note:
            print(f"User {username} not found")
            return
        note.delete()
        print(f"Note {username} deleted.")
    elif param == 'create':
        username = input("Username[default 'user']:") or 'user'
        password = input("Password[default 'user']:") or 'user'
        user = UserModel(username, password, role="simple_user", is_staff=False)
        user.save()
        if user.id:
            print(f"User create successful! id={user.id}")
        else:
            print(f"User with name {user.username} already exist!")
    else:
        print(f"Unknown command - {param}")


@app.cli.command('fixture')
@click.argument('param')
def load_fixture(param):
    """
    Load fixture by file name
    """
    if param == "load":
        filename = input("Enter fixture file name:")
        if filename:
            load_fixture(filename)
    else:
        print(f"Unknown command - {param}")


