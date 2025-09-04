# -*- coding: utf-8 -*-
from flask import Flask, flash, request, render_template, redirect, url_for, session, jsonify
from flask_session import Session
import psycopg2
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import uuid
import os
import re
import g4f
import pytz


#------------------------------------------------------------------------------------------------


'''
'''




#------------------------------------------------------------------------------------------------


UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
current_date = datetime.now().strftime('%Y-%m-%d')


#------------------------------------------------------------------------------------------------


app = Flask(__name__)
app.config['SESSION_FILE_DIR'] = '/var/www/School_websiteV19/flask_session'
app.session_cookie_name = 'my_session_cookie'
PROXY = "http://91.243.71.95:5000"

app.secret_key = os.urandom(24)
TIMEZONE = pytz.timezone("Asia/Almaty")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


try:
    conn = psycopg2.connect(
        database="postgres",
        host="localhost",
        user="postgres",
        password="admin",
        port="5432"
    )
    cursor = conn.cursor()

except Exception as e:
    print(e)


# ключ для админа


secret_key_a : str = """
    CREATE TABLE IF NOT EXISTS key_admin_1 (
        id serial PRIMARY KEY,
        admin_key_a varchar(32) NOT NULL UNIQUE
    );
"""
cursor.execute(query=secret_key_a)
conn.commit()


# фракции/группы


groups : str = """
    CREATE TABLE IF NOT EXISTS group_1 (
        id serial PRIMARY KEY,
        group_name varchar(36) NOT NULL UNIQUE
    );
"""
cursor.execute(query=groups)
conn.commit()


# ключ для участника


secret_key_m : str = """
    CREATE TABLE IF NOT EXISTS key_member_1 (
        id serial PRIMARY KEY,
        admin_key_m varchar(40) NOT NULL UNIQUE
    );
"""
cursor.execute(query=secret_key_m)
conn.commit()


# база данных админа


admin : str = """
    CREATE TABLE IF NOT EXISTS admin_1 (
        id serial PRIMARY KEY,
        first_name varchar(32) NOT NULL,
        second_name varchar(32) NOT NULL,
        email varchar(32) NOT NULL UNIQUE,
        password varchar(32) NOT NULL
    );
"""
cursor.execute(query=admin)
conn.commit()


# база данных участника


member : str = """
    CREATE TABLE IF NOT EXISTS member_1 (
        id serial PRIMARY KEY,
        first_name varchar(32) NOT NULL,
        second_name varchar(32) NOT NULL,
        email varchar(32) NOT NULL UNIQUE,
        password varchar(32) NOT NULL
    );
"""
cursor.execute(query=member)
conn.commit()


# база данных конкурса


events : str = """
    CREATE TABLE IF NOT EXISTS events_1 (
        id serial PRIMARY KEY,
        title varchar(32) NOT NULL,
        group_name varchar(32) NOT NULL,
        description varchar(600) NOT NULL,
        date DATE NOT NULL,
        file varchar(255) NOT NULL
    );
"""
cursor.execute(query=events)
conn.commit()


# база данных проектов


project : str = """
    CREATE TABLE IF NOT EXISTS projects_1 (
        id serial PRIMARY KEY,
        title varchar(32) NOT NULL,
        group_name varchar(32) NOT NULL,
        description varchar(600) NOT NULL,
        date DATE NOT NULL,
        file varchar(255) NOT NULL
    );
"""
cursor.execute(query=project)
conn.commit()


# база данных проектов


people : str = """
    CREATE TABLE IF NOT EXISTS people_1 (
        id serial PRIMARY KEY,
        first_name varchar(32) NOT NULL,
        second_name varchar(32) NOT NULL,
        group_name varchar(32) NOT NULL,
        file varchar(255) NOT NULL
    );
"""
cursor.execute(query=people)
conn.commit()


# база данных новостей


news : str = """
    CREATE TABLE IF NOT EXISTS news_1 (
        id serial PRIMARY KEY,
        title varchar(32) NOT NULL,
        group_name varchar(32) NOT NULL,
        description varchar(600) NOT NULL,
        date DATE NOT NULL,
        file varchar(255) NOT NULL
    );
"""
cursor.execute(query=news)
conn.commit()


# база данных достижений школы


achievements : str = """
    CREATE TABLE IF NOT EXISTS achievements_1 (
        id serial PRIMARY KEY,
        title varchar(32) NOT NULL,
        group_name varchar(32) NOT NULL,
        description varchar(600) NOT NULL,
        date DATE NOT NULL,
        file varchar(255) NOT NULL
    );
"""
cursor.execute(query=achievements)
conn.commit()


# база данных достижений фракций


achievements_frac : str = """
    CREATE TABLE IF NOT EXISTS achievements_frac_1 (
        id serial PRIMARY KEY,
        title varchar(32) NOT NULL,
        group_name varchar(32) NOT NULL,
        description varchar(600) NOT NULL,
        date DATE NOT NULL,
        file varchar(255) NOT NULL
    );
"""
cursor.execute(query=achievements_frac)
conn.commit()


# база данных соц.сетей


social_networks: str = """
    CREATE TABLE IF NOT EXISTS social_networks_1 (
        id serial PRIMARY KEY,
        email varchar(32) NOT NULL,
        phone varchar(32) NOT NULL,
        instagram varchar(32) NOT NULL
    );
"""
cursor.execute(query=social_networks)
conn.commit()


# база данных аудита


audit: str = """
CREATE TABLE IF NOT EXISTS audit_1 (
    id serial PRIMARY KEY,
    user_id int NOT NULL,
    action varchar(255) NOT NULL,
    action_date timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES member_1 (id)
);
"""
cursor.execute(query=audit)
conn.commit()


# База данных чата с ИИ ассистентом


chatAI = """
CREATE TABLE IF NOT EXISTS chatAI_1 (
    session_id UUID PRIMARY KEY,
    messages JSONB NOT NULL
);
"""

if conn:
    try:
        cursor.execute(chatAI)
        conn.commit()
        print("Table created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")
else:
    print("No database connection.")



#------------------------------------------------------------------------------------------------


# Добавление ключа для админа


secret_key_a: str = "123a"
add_admin_key : str = f"""
    INSERT INTO key_admin_1
    (admin_key_a)
    VALUES ('{secret_key_a}')
    ON CONFLICT DO NOTHING;
    """
cursor.execute(query=add_admin_key)
conn.commit()


# Добавление ключа для участника


secret_key_m: str = "123m"
add_member_key : str = f"""
    INSERT INTO key_member_1
    (admin_key_m)
    VALUES ('{secret_key_m}')
    ON CONFLICT DO NOTHING;
    """
cursor.execute(query=add_member_key)
conn.commit()


# Добавление соц.сетей


cursor.execute("""
    INSERT INTO social_networks_1 (id, email, phone, instagram)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
""", (1, 'example@example.com', '123456789', 'example_insta'))
conn.commit()


#------------------------------------------------------------------------------------------------


get_info : str = "SELECT * FROM member_1;"
cursor.execute(query=get_info)
print(* cursor.fetchall(), sep="\n")




# cursor.execute("DROP SCHEMA public CASCADE;")
# conn.commit()

# cursor.execute("CREATE SCHEMA public;")
# conn.commit()


# cursor.execute("""
#     INSERT INTO social_networks_1 (id, email, phone, instagram)
#     VALUES (%s, %s, %s, %s)
#     ON CONFLICT (id) DO NOTHING;
# """, (1, 'example@example.com', '123456789', 'example_insta'))
# conn.commit()

# cursor.execute("SELECT * FROM social_networks_1;")
# data = cursor.fetchall()
# print(data)

# cursor.execute("SELECT * FROM people_1;")
# data = cursor.fetchall()
# print(data)

# DELETE FROM social_networks_1;

# get_info : str = "SELECT * FROM key_member_1;"
# cursor.execute(query=get_info)
# for data in cursor.fetchall():
#     print(data)
# print(* cursor.fetchall(), sep="\n")


# get_info : str = "SELECT * FROM audit_1;"
# cursor.execute(query=get_info)
# for data in cursor.fetchall():
#     print(data)
# print(* cursor.fetchall(), sep="\n")


# get_info : str = "SELECT * FROM key_admin_1;"
# cursor.execute(query=get_info)
# for data in cursor.fetchall():
#     print(data)
# print(* cursor.fetchall(), sep="\n")


# access = f"""SELECT admin_key_a FROM key_admin_1"""
# cursor.execute(query=access)
# data = cursor.fetchall()[0]
# print(data[0])






#------------------------------------------------------------------------------------------------


# Регистрация админа


@app.route('/admin_registration', methods=["GET", "POST"])
def admin_registration():
    if request.method == "POST":
        first_name = request.form["first_name"]
        second_name = request.form["second_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["password_confirm"]
        key_a = request.form["secret_key"]
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return "Invalid email format. Please enter a valid email address."
        access = "SELECT admin_key_a FROM key_admin_1"
        cursor.execute(query=access)
        data = cursor.fetchall()[0]
        if password == confirm_password and key_a == data[0]:
            print("access 1")
            add_admin = f"""
            INSERT INTO admin_1
            (first_name, second_name, email, password)
            VALUES ('{first_name}', '{second_name}', '{email}', '{password}')
            """
            cursor.execute(query=add_admin)
            conn.commit()
            print("complete")
            session['admin_email'] = email
            return render_template("main_admin.html")
        else:
            return "Error in email, password, or secret key"
    return render_template("admin_registration.html")


# Авторизация админа


@app.route('/admin_autorization', methods=["GET", "POST"])
def admin_autorization():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute("SELECT id, password FROM admin_1 WHERE email = %s", (email))
        data = cursor.fetchone()
        if data and data[1] == password:
            session['admin_email'] = email
            session['role'] = 'admin'
            session['user_id'] = data[0]
            return redirect(url_for('main_admin'))
        else:
            flash("Invalid email or password.")
            return redirect(url_for('admin_autorization')) 
    return render_template("admin_autorization.html")


# Регистрация участника


@app.route('/member_registration', methods=["GET", "POST"])
def member_registration():
    if request.method == "POST":
        first_name = request.form["first_name"]
        second_name = request.form["second_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["password_confirm"]
        key_m = request.form["secret_key"]
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return "Invalid email format. Please enter a valid email address."
        if password != confirm_password:
            return "Passwords do not match. Please confirm your password."
        access1 = "SELECT admin_key_m FROM key_member_1"
        cursor.execute(query=access1)
        data = cursor.fetchall()[0]
        if key_m == data[0]:
            add_member = f"""
                INSERT INTO member_1
                (first_name, second_name, email, password)
                VALUES ('{first_name}', '{second_name}', '{email}', '{password}')
                """
            cursor.execute(query=add_member)
            conn.commit()
            session['member_email'] = email
            return render_template("main_member.html")
        else:
            return "Error in secret key"
    return render_template("member_registration.html")


# Авторизация участника


@app.route('/member_autorization', methods=["GET", "POST"])
def member_autorization():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute("SELECT id, password FROM member_1 WHERE email = %s", (email,))
        data = cursor.fetchone()
        print(data)
        if data and data[1] == password:
            print(1)
            session['member_email'] = email
            session['role'] = 'member'
            session['user_id'] = data[0]
            return redirect(url_for('main_member'))
        else:
            flash("Invalid email or password.")
            return redirect(url_for('member_autorization'))
    return render_template("member_autorization.html")



# Выход из системы


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#------------------------------------------------------------------------------------------------


# Главное меню для всех


@app.route('/', methods=["GET", "POST"])
def main():
    query_projects = "SELECT title, description, date, file FROM projects_1 ORDER BY date DESC LIMIT 3"
    cursor.execute(query_projects)
    projects = cursor.fetchall()
    projects = [dict(zip([column[0] for column in cursor.description], project)) for project in projects]
    query_news = "SELECT title, description, date, file FROM news_1 ORDER BY date DESC LIMIT 3"
    cursor.execute(query_news)
    news = cursor.fetchall()
    news = [dict(zip([column[0] for column in cursor.description], article)) for article in news]
    return render_template("main.html", projects=projects, news=news)


# редакция для админа


@app.route('/main_admin', methods=["GET", "POST"])
def main_admin():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied. Please log in as an admin.")
        return redirect(url_for('admin_autorization'))
    
    return render_template("main_admin.html")



# редакция для участника


@app.route('/main_member', methods=["GET", "POST"])
def main_member():
    if 'role' in session and session['role'] == 'member':
        return render_template("main_member.html")
    else:
        flash("Please log in as a member to access this page.")
        return redirect(url_for('member_autorization'))



#-----------------------------------------------------------------------------------------------


# редакция конкурсов и мероприятий


@app.route('/events', methods=["GET", "POST"])
def events():
    try:
        if 'admin_email' in session:
            if request.method == "POST":
                title = request.form["title"]
                group = request.form["group"]
                description = request.form["description"]
                date = request.form["date"]
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('Файл не выбран')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("""
                    INSERT INTO events_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                user_id = session.get('user_id')
                action = f"Добавлено событие: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                return render_template("events.html", image=filename, title=title, group=group, date=date, description=description)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("events.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        flash("Произошла ошибка при обработке запроса. Попробуйте снова.")
        return redirect(request.url)

                   
# редакция проекта


@app.route('/project_member', methods=["GET", "POST"])
def project_member():
    try:
        if "member_email" in session:
            if request.method == "POST":
                title = request.form["title"]
                group = request.form["group"]
                description = request.form["description"]
                date = request.form["date"]
                if 'file' not in request.files:
                    flash('Нет файла в запросе.')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('Файл не выбран.')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("""
                        INSERT INTO projects_1 (title, description, group_name, date, file)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (title, description, group, date, filename))
                    conn.commit()
                    user_id = session.get('user_id')
                    action = f"Добавлен проект: {title}"
                    cursor.execute("""
                        INSERT INTO audit_1 (user_id, action)
                        VALUES (%s, %s)
                    """, (user_id, action))
                    conn.commit()
                    return render_template("project_member.html", image=filename, title=title, group=group, date=date, description=description)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("project_member.html", groups=groups)
    except Exception as e:
        print(f"Ошибка при добавлении проекта: {e}")
        conn.rollback()
        flash("Произошла ошибка при обработке запроса. Попробуйте снова.")
        return redirect(request.url)

    

# Проекты для админа


@app.route('/project_admin', methods=["GET", "POST"])
def project_admin():
    try:
        if 'admin_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO projects_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                user_id = session.get('user_id')
                action = f"Добавлен проект: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Проект успешно добавлен!")
                return redirect("/project_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении проекта.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("project_admin.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)




# редакция новостей


@app.route('/news_member', methods=["GET", "POST"]) # m
def news_member():
    try:
        if 'member_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO news_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                user_id = session.get('user_id')
                action = f"Добавлена новость: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Новость успешно добавлена!")
                return redirect("/news_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении новости.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("news_member.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)



# редакция достижений


@app.route('/achievements', methods=["GET", "POST"])
def achievements():
    try:
        if 'admin_email' in session or "member_email" in session:
            if request.method == "POST":
                title = request.form["title"]
                group = request.form["group"]
                description = request.form["description"]
                date = datetime.now(TIMEZONE)
                date = date.strtime("%Y-%D %H:%M")
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('Файл не выбран')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("""
                        INSERT INTO achievements_1 (title, description, group_name, date, file)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (title, description, group, date, filename))
                    print(f"Achievement added: {title}, {description}, {group}, {date}, {filename}")
                    conn.commit()
                    user_id = session.get('user_id')
                    action = f"Добавлено достижение: {title}"
                    cursor.execute("""
                        INSERT INTO audit_1 (user_id, action)
                        VALUES (%s, %s)
                    """, (user_id, action))
                    print(f"Audit log added for action: {action}")
                    conn.commit()
                    return render_template("achievements.html", image=filename, title=title, group=group, date=date, description=description)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("achievements.html", groups=groups)
    except Exception as e:
        print(f"Ошибка при добавлении достижения: {e}")
        conn.rollback()
        flash("Произошла ошибка при обработке запроса. Попробуйте снова.")
        return redirect(request.url)


#-----------------------------------------------------------------------------------------------


# просмотр и редакция документов


@app.route('/documents', methods=["GET", "POST"])
def documents():
    return render_template("documents.html")


# просмотр и редакция устава клуба


@app.route('/club_info', methods=["GET", "POST"])
def club_info():
    return render_template("club_info.html")


# просмотр и редакция соц.сетей


@app.route('/social_networks', methods=["GET", "POST"])
def social_networks():
    if 'admin_email' in session:
        if request.method == "POST":
            email = request.form.get("email")
            phone = request.form.get("phone")
            instagram = request.form.get("instagram")
            cursor.execute("SELECT email, phone, instagram FROM social_networks_1 WHERE id = 1")
            current_data = cursor.fetchone()
            if not current_data:
                current_data = ("", "", "")
            new_email = email if email else current_data[0]
            new_phone = phone if phone else current_data[1]
            new_instagram = instagram if instagram else current_data[2]
            cursor.execute("""
                UPDATE social_networks_1
                SET email = %s, phone = %s, instagram = %s
                WHERE id = 1
            """, (new_email, new_phone, new_instagram))
            conn.commit()
            return render_template('main_admin.html')
        cursor.execute("SELECT email, phone, instagram FROM social_networks_1 WHERE id = 1")
        current_data = cursor.fetchone()
        if not current_data:
            current_data = ("", "", "")
    return render_template("social_networks.html", data=current_data)


# редакция участников


@app.route('/people', methods=["GET", "POST"])
def people():
    if 'admin_email' in session:
        if request.method == "POST":
            if 'first_name' in request.form:
                first_name = request.form["first_name"]
                second_name = request.form["second_name"]
                group_name = request.form["group_name"]
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    cursor.execute("""
                        INSERT INTO people_1 (first_name, second_name, group_name, file)
                        VALUES (%s, %s, %s, %s)
                    """, (first_name, second_name, group_name, filename))
                    conn.commit()
            if 'delete_person' in request.form:
                person_id = request.form['delete_person_id']
                cursor.execute("DELETE FROM people_1 WHERE id = %s", (person_id,))
                conn.commit()
        cursor.execute("SELECT * FROM people_1")
        people = cursor.fetchall()
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
    return render_template("people.html", people=people, groups=groups)


# просмотр и редакция участников


@app.route('/member_list', methods=["GET", "POST"])
def member_list():
    if 'admin_email' in session:
        if request.method == "POST":
            member_id = request.form.get("delete_id")
            if member_id:
                cursor.execute("DELETE FROM member_1 WHERE id = %s;", (member_id,))
                conn.commit()
        cursor.execute("SELECT id, first_name, second_name FROM member_1;")
        members = cursor.fetchall()
    return render_template("member_list.html", members=members)


# просмотр аудита 


@app.route('/audit', methods=["GET"])
def audit():
    if 'role' in session and session['role'] == 'admin':
        cursor.execute("""
            SELECT al.action_date, 
                   COALESCE(a.first_name, m.first_name) AS first_name,
                   COALESCE(a.second_name, m.second_name) AS second_name,
                   al.action
            FROM audit_1 al
            LEFT JOIN admin_1 a ON al.user_id = a.id
            LEFT JOIN member_1 m ON al.user_id = m.id
            ORDER BY al.action_date DESC;
        """)
        audit_logs = cursor.fetchall()
        return render_template("audit.html", logs=audit_logs)
    else:
        flash("Access denied. Please log in as an admin.")
        return redirect(url_for('admin_autorization'))



# добавление группы 


@app.route('/groups', methods=["GET", "POST"])
def manage_groups():
    if 'admin_email' in session:
        if request.method == "POST":
            action = request.form.get("action")
            if action == "add":
                new_group = request.form["new_group"]
                add_group = f"""
                    INSERT INTO group_1 (group_name)
                    VALUES (%s)
                """
                cursor.execute(add_group, (new_group,))
                conn.commit()
            elif action == "delete":
                group_to_delete = request.form["group_to_delete"]
                delete_group = f"""
                    DELETE FROM group_1 WHERE group_name = %s
                """
                cursor.execute(delete_group, (group_to_delete,))
                conn.commit()
            elif action == "change":
                old_group = request.form["old_group"]
                new_group = request.form["new_group"]
                update_group = f"""
                    UPDATE group_1
                    SET group_name = %s
                    WHERE group_name = %s
                """
                cursor.execute(update_group, (new_group, old_group))
                conn.commit()
    cursor.execute("SELECT group_name FROM group_1")
    groups = cursor.fetchall()
    return render_template("groups.html", groups=groups)


# изменение ключа админа 


@app.route('/admin_key', methods=["GET", "POST"])
def admin_key():
    if 'admin_email' in session:
        if request.method == "POST":
            admin_key = request.form["admin_key"]
            new_admin_key = request.form["new_admin_key"]
            new_admin_key_confirm = request.form["new_admin_key_confirm"]
            access = f"""SELECT admin_key_a FROM key_admin_1"""
            cursor.execute(query=access)
            data = cursor.fetchall()[0]
            if admin_key == data[0] and new_admin_key == new_admin_key_confirm:
                del_admin_key : str = f"""
                BEGIN; DELETE FROM key_admin_1; COMMIT;
                """
                cursor.execute(query=del_admin_key)
                conn.commit()

                add_admin_key : str = f"""
                INSERT INTO key_admin_1
                (admin_key_a)
                VALUES ('{new_admin_key}')
                """
                cursor.execute(query=add_admin_key)
                conn.commit()
                return render_template("admin_key.html")
            else:
                return "Не удалось поменять ключ для админа"
    return render_template("admin_key.html")


# редактировать ключ участника 


@app.route('/member_key', methods=["GET", "POST"])
def member_key():
    if 'admin_email' in session:
        if request.method == "POST":
            admin_key = request.form["admin_key"]
            new_member_key = request.form["new_member_key"]
            new_member_key_confirm = request.form["new_member_key_confirm"]
            access = f"""SELECT admin_key_a FROM key_admin_1"""
            cursor.execute(query=access)
            data = cursor.fetchall()[0]
            if admin_key == data[0] and new_member_key == new_member_key_confirm:
                del_member_key : str = f"""
                BEGIN; DELETE FROM key_member_1; COMMIT;
                """
                cursor.execute(query=del_member_key)
                conn.commit()
                add_member_key : str = f"""
                INSERT INTO key_member_1
                (admin_key_m)
                VALUES ('{new_member_key}')
                """
                cursor.execute(query=add_member_key)
                conn.commit()
                return render_template("member_key.html")
            else:
                return "Не удалось поменять ключ для участника"
    return render_template("member_key.html")


#-----------------------------------------------------------------------------------------------


# Для гостей!


# Установка сессий ИИ для пользователя


@app.before_request
def setup_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO chatAI_1 (session_id, messages) 
                        VALUES (%s, %s)
                    """, (session['session_id'], json.dumps([])))
                    conn.commit()
            except Exception as e:
                print(f"Error while inserting session data: {e}")


# Добавление ИИ ассистента


@app.route('/chatAI', methods=["GET", "POST"])
def chatAI():
    session_id = session.get('session_id')
    if not session_id:
        session['session_id'] = os.urandom(16).hex()
        session_id = session['session_id']
    if request.method == "POST":
        user_message = request.json.get('user_message')
        requirements = ("Слушай внимательно инструкцию. Ты можешь отвечать только на вопросы, "
                        "связанные с географией, естествознанием, немного похожими науками и экологией. "
                        "Если отвечают не по теме, то ты говоришь, что не можешь ответить на эту тему. "
                        "После инструкции можешь прочитать сообщения пользователя:")
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        request_ai = f"{requirements} {user_message}"
        messages = session.get('messages', [])
        messages.append({"role": "user", "content": request_ai})
        try:
            print("Sending request to AI model with the following messages:", messages)
            response = g4f.ChatCompletion.create(
                model=g4f.models.default,
                messages=messages
            )
            print("AI response:", response)
            if isinstance(response, str):
                ai_message = response
            elif isinstance(response, dict) and 'choices' in response:
                ai_message = response['choices'][0].get('message', {}).get('content', "Извините, я не смог ответить.")
            else:
                ai_message = "Ошибка: модель вернула неожиданный формат ответа."
        except g4f.exceptions.ProxyError as e:
            print(f"Proxy error: {e}")
            ai_message = "Ошибка с прокси-соединением, попробуйте позже."
        except Exception as e:
            print(f"Error with AI response: {e}")
            ai_message = "Ошибка обработки ответа AI."
        messages.append({"role": "assistant", "content": ai_message})
        session['messages'] = messages
        return jsonify({'response': ai_message, 'messages': messages})
    return render_template("chatAI.html", messages=[])


# конец сессии пользователя с ИИ


@app.route('/logout_chatAI', methods=["POST"])
def logout_chatAI():
    session_id = session.pop('session_id', None)
    if session_id:
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM chatAI_1 WHERE session_id = %s", (session_id,))
                    conn.commit()
            except Exception as e:
                print(f"Error while deleting session data: {e}")
    return jsonify({"message": "Session ended and data cleared."}), 200


# Ивенты


@app.route('/events_list', methods=["GET"])
def events_list():
    query = "SELECT title, group_name, description, date, file FROM events_1 ORDER BY date DESC"
    cursor.execute(query)
    events = cursor.fetchall()
    return render_template("events_list.html", events=events)


# Проекты


@app.route('/project_list', methods=["GET"])
def project_list():
    query = "SELECT title, group_name, description, date, file FROM projects_1 ORDER BY date DESC"
    cursor.execute(query)
    projects = cursor.fetchall()
    return render_template("project_list.html", projects=projects)


# Новости


@app.route('/news_list', methods=["GET"])
def news_list():
    query = "SELECT title, group_name, description, date, file FROM news_1 ORDER BY date DESC"
    cursor.execute(query)
    news = cursor.fetchall()
    return render_template("news_list.html", news=news)


# Достижения


@app.route('/achievements_list', methods=["GET"])
def achievements_list():
    query = "SELECT title, group_name, description, date, file FROM achievements_1 ORDER BY date DESC"
    cursor.execute(query)
    achievements = cursor.fetchall()
    return render_template("achievements_list.html", achievements=achievements)


# Действующие лица


@app.route('/people_list', methods=["GET"])
def people_list():
    try:
        cursor.execute("SELECT first_name, second_name, group_name, file FROM people_1")
        people = cursor.fetchall()
        return render_template("people_list.html", people=people)
    except Exception as e:
        print(f"Ошибка при загрузке списка людей: {e}")
        flash("Произошла ошибка при загрузке данных. Попробуйте снова.")
        return redirect("/")



# # Действующие лица админ


@app.route('/people_admin', methods=["GET", "POST"])
def people_admin():
    try:
        if 'admin_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            first_name = request.form.get("first_name", "").strip()
            second_name = request.form.get("second_name", "").strip()
            group_name = request.form.get("group_name", "").strip()
            file = request.files.get("file")
            filename = None
            if file and file.filename != '':
                if not allowed_file(file.filename):
                    flash("Недопустимый формат файла.")
                    return redirect(request.url)
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor.execute("""
                INSERT INTO people_1 (first_name, second_name, group_name, file)
                VALUES (%s, %s, %s, %s)
            """, (first_name, second_name, group_name, filename))
            conn.commit()
            flash("Человек успешно добавлен!")
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        cursor.execute("SELECT first_name, second_name, group_name, file FROM people_1")
        people = cursor.fetchall()
        return render_template("people_admin.html", groups=groups, people=people)
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)
    


@app.route('/people_member', methods=["GET", "POST"])
def people_member():
    try:
        if 'member_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            first_name = request.form.get("first_name", "").strip()
            second_name = request.form.get("second_name", "").strip()
            group_name = request.form.get("group_name", "").strip()
            file = request.files.get("file")
            filename = None
            if file and file.filename != '':
                if not allowed_file(file.filename):
                    flash("Недопустимый формат файла.")
                    return redirect(request.url)
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor.execute("""
                INSERT INTO people_1 (first_name, second_name, group_name, file)
                VALUES (%s, %s, %s, %s)
            """, (first_name, second_name, group_name, filename))
            conn.commit()
            flash("Человек успешно добавлен!")
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        cursor.execute("SELECT first_name, second_name, group_name, file FROM people_1")
        people = cursor.fetchall()
        return render_template("people_member.html", groups=groups, people=people)
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)




# Западный Казахстан 1


@app.route('/batys_kaz', methods=["GET"])
def batys_kaz():
    return render_template("o_batys_kaz.html")


# Атырау 2


@app.route('/atyrau', methods=["GET"])
def atyrau():
    return render_template("o_atyrau.html")


# Мангыстау 3


@app.route('/mangystau', methods=["GET"])
def mangystau():
    return render_template("o_mangystau.html")


# Актобе 4


@app.route('/aktobe', methods=["GET"])
def aktobe():
    return render_template("o_aktobe.html")


# Костанай 5


@app.route('/kostanay', methods=["GET"])
def kostanay():
    return render_template("o_kostanay.html")


# Улытау 6


@app.route('/ulytau', methods=["GET"])
def ulytau():
    return render_template("o_ulytau.html")


# Кызылорда 7


@app.route('/kyzylorda', methods=["GET"])
def kyzylorda():
    return render_template("o_kyzylorda.html")


# Туркистан 8


@app.route('/turkystan', methods=["GET"])
def turkystan():
    return render_template("o_turkystan.html")

 
# Акмола 9


@app.route('/akmola', methods=["GET"])
def akmola():
    return render_template("o_akmola.html")


# Северный Казахстан 10


@app.route('/soltustyk_kaz', methods=["GET"])
def soltustyk_kaz():
    return render_template("o_soltustyk_kaz.html")


# Павлодар 11


@app.route('/pavlodar', methods=["GET"])
def pavlodar():
    return render_template("o_pavlodar.html")


# Абай 12


@app.route('/abai', methods=["GET"])
def abai():
    return render_template("o_abai.html")


# Жетысу 13


@app.route('/jetisu', methods=["GET"])
def jetisu():
    return render_template("o_jetisu.html")


# Восточный Казахстан 14


@app.route('/shygys_kaz', methods=["GET"])
def shygys_kaz():
    return render_template("o_shygys_kaz.html")


# Алматы 15


@app.route('/almaty', methods=["GET"])
def almaty():
    return render_template("o_almaty.html")


# Жамбыл 16


@app.route('/jambyl', methods=["GET"])
def jambyl():
    return render_template("o_jambyl.html")


# Караганда 17


@app.route('/karaganda', methods=["GET"])
def karaganda():
    return render_template("o_karaganda.html")


# Балхаш


@app.route('/balhash', methods=["GET"])
def balhash():
    return render_template("z_balhash.html")


# Каспи


@app.route('/kaspi', methods=["GET"])
def kaspi():
    return render_template("z_kaspi.html")



# Семипалатинск


@app.route('/semipalatinsk', methods=["GET"])
def semipalatinsk():
    return render_template("z_semipalatinsk.html")


# Орал


@app.route('/oral', methods=["GET"])
def oral():
    return render_template("z_oral.html")


#-----------------------------------------------------------------------------------------------


# Устав


@app.route('/ustav', methods=["GET"])
def ustav():
    return render_template("ustav.html", ustav = ustav)


# Устав редактировать


@app.route('/red_ustav', methods=["GET"])
def red_ustav():
    return render_template("red_ustav.html")


# Редактор достижения фракции участник


@app.route('/achievements_member', methods=["GET", "POST"]) 
def achievments_member_member():
    try:
        if 'member_email' in session:
            if request.method == "POST":
                title = request.form.get("title", "").strip()
                group = request.form.get("group", "").strip()
                description = request.form.get("description", "").strip()
                date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
                if 'file' not in request.files or request.files['file'].filename == '':
                    flash("Файл не выбран.")
                    return redirect(request.url)
                file = request.files['file']
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    try:
                        cursor.execute("""
                            INSERT INTO news_1 (title, description, group_name, date, file)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (title, description, group, date, filename))
                        conn.commit()
                        user_id = session.get('user_id')
                        action = f"Добавлена новость: {title}"
                        cursor.execute("""
                            INSERT INTO audit_1 (user_id, action)
                            VALUES (%s, %s)
                        """, (user_id, action))
                        conn.commit()
                        flash("Новость успешно добавлена!")
                        return redirect("/news_list") 
                    except Exception as db_error:
                        conn.rollback()
                        print(f"Ошибка базы данных: {db_error}")
                        flash("Ошибка при добавлении новости.")
                        return redirect(request.url)
                else:
                    flash("Недопустимый формат файла.")
                    return redirect(request.url)
            cursor.execute("SELECT group_name FROM group_1")
            groups = cursor.fetchall()
            return render_template("achievements_member.html", groups=groups)
        flash("Вы не авторизованы для доступа к этой странице.")
        return redirect("/login")
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


# Просмотр достижения фракции 


@app.route('/achievements_frac_list', methods=["GET"])
def achievements_frac_list():
    query = "SELECT title, group_name, description, date, file FROM achievements_frac_1 ORDER BY date DESC"
    cursor.execute(query)
    achievements = cursor.fetchall()
    return render_template("achievements_frac_list.html", achievements=achievements)



# Редактор достижения фракций админ


@app.route('/achievements_frac_admin', methods=["GET", "POST"]) 
def achievements_frac_admin():
    try:
        if 'admin_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO achievements_frac_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                user_id = session.get('user_id')
                action = f"Добавлено достижение: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Достижение успешно добавлено!")
                return redirect("/achievements_frac_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении достижения.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("achievements_frac_admin.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


# Редактор достижения фракций участник


@app.route('/achievements_frac_member', methods=["GET", "POST"]) # m
def achievements_frac_member():
    try:
        if 'member_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO achievements_frac_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                user_id = session.get('user_id')
                action = f"Добавлено достижение: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Достижение успешно добавлено!")
                return redirect("/achievements_frac_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении достижения.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("achievements_frac_member.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)



# Редактор достижения школы для участника


@app.route('/achievements_member', methods=["GET", "POST"]) # m
def achievements_member():
    try:
        if 'member_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO achievements_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                
                user_id = session.get('user_id')
                action = f"Добавлено достижение: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Достижение успешно добавлено!")
                return redirect("/achievements_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении достижения.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("achievements_member.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


# Редактор достижения школы для админа


@app.route('/achievements_admin', methods=["GET", "POST"]) #
def achievements_admin(): 
    try:
        if 'admin_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO achievements_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                
                user_id = session.get('user_id')
                action = f"Добавлено достижение: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Достижение успешно добавлено!")
                return redirect("/achievements_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении достижения.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("achievements_admin.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)



# Редактор мероприятий для админа


@app.route('/events_admin', methods=["GET", "POST"]) #
def events_admin():
    try:
        if 'admin_email' in session:
            if request.method == "POST":
                title = request.form.get("title", "").strip()
                group = request.form.get("group", "").strip()
                description = request.form.get("description", "").strip()
                date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
                if 'file' not in request.files or request.files['file'].filename == '':
                    flash("Файл не выбран.")
                    return redirect(request.url)
                file = request.files['file']
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    try:
                        cursor.execute("""
                            INSERT INTO events_1 (title, description, group_name, date, file)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (title, description, group, date, filename))
                        conn.commit()
                        user_id = session.get('user_id')
                        action = f"Добавлено событие: {title}"
                        cursor.execute("""
                            INSERT INTO audit_1 (user_id, action)
                            VALUES (%s, %s)
                        """, (user_id, action))
                        conn.commit()
                        flash("Событие успешно добавлено!")
                        return redirect("/events_list")
                    except Exception as db_error:
                        conn.rollback()
                        print(f"Ошибка базы данных: {db_error}")
                        flash("Ошибка при добавлении события.")
                        return redirect(request.url)
                else:
                    flash("Недопустимый формат файла.")
                    return redirect(request.url)
            cursor.execute("SELECT group_name FROM group_1")
            groups = cursor.fetchall()
            return render_template("events_admin.html", groups=groups)
        flash("Вы не авторизованы для доступа к этой странице.")
        return redirect("/login")
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


# Редактор мероприятий для участники


@app.route('/events_member', methods=["GET", "POST"]) # m
def events_member():
    try:
        if 'member_email' in session:
            if request.method == "POST":
                title = request.form.get("title", "").strip()
                group = request.form.get("group", "").strip()
                description = request.form.get("description", "").strip()
                date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
                if 'file' not in request.files or request.files['file'].filename == '':
                    flash("Файл не выбран.")
                    return redirect(request.url)
                file = request.files['file']
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    try:
                        cursor.execute("""
                            INSERT INTO events_1 (title, description, group_name, date, file)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (title, description, group, date, filename))
                        conn.commit()
                        user_id = session.get('user_id')
                        action = f"Добавлено событие: {title}"
                        cursor.execute("""
                            INSERT INTO audit_1 (user_id, action)
                            VALUES (%s, %s)
                        """, (user_id, action))
                        conn.commit()
                        flash("Событие успешно добавлено!")
                        return redirect("/events_list")
                    except Exception as db_error:
                        conn.rollback()
                        print(f"Ошибка базы данных: {db_error}")
                        flash("Ошибка при добавлении события.")
                        return redirect(request.url)
                else:
                    flash("Недопустимый формат файла.")
                    return redirect(request.url)
            cursor.execute("SELECT group_name FROM group_1")
            groups = cursor.fetchall()
            return render_template("events_member.html", groups=groups)
        flash("Вы не авторизованы для доступа к этой странице.")
        return redirect("/login")
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


# Редактор новостей для админа


@app.route('/news_admin', methods=["GET", "POST"]) #
def news_admin():
    try:
        if 'admin_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            group = request.form.get("group", "").strip()
            description = request.form.get("description", "").strip()
            date = request.form.get("date", "").strip() or datetime.now().strftime('%Y-%m-%d')
            file = request.files.get('file')
            if not file or file.filename == '':
                flash("Файл не выбран.")
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash("Недопустимый формат файла.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                cursor.execute("""
                    INSERT INTO news_1 (title, description, group_name, date, file)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, group, date, filename))
                conn.commit()
                user_id = session.get('user_id')
                action = f"Добавлена новость: {title}"
                cursor.execute("""
                    INSERT INTO audit_1 (user_id, action)
                    VALUES (%s, %s)
                """, (user_id, action))
                conn.commit()
                flash("Новость успешно добавлена!")
                return redirect("/news_list")
            except Exception as db_error:
                conn.rollback()
                print(f"Ошибка базы данных: {db_error}")
                flash("Ошибка при добавлении новости.")
                return redirect(request.url)
        cursor.execute("SELECT group_name FROM group_1")
        groups = cursor.fetchall()
        return render_template("news_admin.html", groups=groups)
    except Exception as e:
        conn.rollback()
        print(f"Общая ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)
    

# Удаление поста по названию для админа


@app.route('/delete_post_admin', methods=["GET", "POST"])
def delete_post_admin():
    try:
        if 'admin_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            selected_id = request.form.get("post_id")
            table_name = request.form.get("table_name")
            if not selected_id or not table_name:
                flash("Выберите запись для удаления.")
                return redirect(request.url)
            try:
                query = f"DELETE FROM {table_name} WHERE id = %s"
                cursor.execute(query, (selected_id,))
                conn.commit()
                flash("Запись успешно удалена!")
            except Exception as e:
                conn.rollback()
                print(f"Ошибка при удалении: {e}")
                flash("Произошла ошибка при удалении записи.")
        table_name = request.args.get("category", "news_1")
        date_filter = request.args.get("date", "")
        query = f"SELECT id, title, date FROM {table_name}"
        params = []
        if date_filter:
            query += " WHERE date = %s"
            params.append(date_filter)
        cursor.execute(query, params)
        posts = cursor.fetchall()
        return render_template("delete_post_admin.html", posts=posts, table_name=table_name, date_filter=date_filter)
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


# Удаление поста по названию для участника


@app.route('/delete_post_member', methods=["GET", "POST"])
def delete_post_member():
    try:
        if 'member_email' not in session:
            flash("Вы не авторизованы для доступа к этой странице.")
            return redirect("/login")
        if request.method == "POST":
            selected_id = request.form.get("post_id")
            table_name = request.form.get("table_name")
            if not selected_id or not table_name:
                flash("Выберите запись для удаления.")
                return redirect(request.url)
            try:
                query = f"DELETE FROM {table_name} WHERE id = %s"
                cursor.execute(query, (selected_id,))
                conn.commit()
                flash("Запись успешно удалена!")
            except Exception as e:
                conn.rollback()
                print(f"Ошибка при удалении: {e}")
                flash("Произошла ошибка при удалении записи.")
        table_name = request.args.get("category", "news_1")
        date_filter = request.args.get("date", "")
        query = f"SELECT id, title, date FROM {table_name}"
        params = []
        if date_filter:
            query += " WHERE date = %s"
            params.append(date_filter)
        cursor.execute(query, params)
        posts = cursor.fetchall()
        return render_template("delete_post_member.html", posts=posts, table_name=table_name, date_filter=date_filter)
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        flash("Произошла ошибка. Попробуйте снова.")
        return redirect(request.url)


#-----------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(
        #host='91.243.71.95', port=5000, debug = True
	debug = True
    )