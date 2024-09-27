import sqlite3

def create_users(cur):
    query = """
    CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY,
    username text,
    password text,
    email text,
    phone text,
    role_id uuid,
    created_at timestamp,
    FOREIGN KEY(role_id) REFERENCES roles(id)
    )
    """
    cur.execute(query)

def create_roles(cur):
    query = """
    CREATE TABLE IF NOT EXISTS roles (
    id uuid PRIMARY KEY,
    name text
    )
    """
    cur.execute(query)

def create_course_enrolled(cur):
    query = """
    CREATE TABLE IF NOT EXISTS course_enrolled (
    course_id uuid,
    user_id uuid,
    created_at timestamp,
    PRIMARY KEY(course_id, user_id),
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    cur.execute(query)

# def create_term(cur):
#     query = """
#     CREATE TABLE IF NOT EXISTS term (
#     id uuid PRIMARY KEY,
#     term_name text,
#     created_at timestamp
#     )
#     """
#     cur.execute(query)

def create_course(cur):
    query = """
    CREATE TABLE IF NOT EXISTS courses (
    id uuid PRIMARY KEY,
    course_name text,
    course_code text,
    instructor_id uuid,
    created_at timestamp,
    FOREIGN KEY(instructor_id) REFERENCES users(id)
    )
    """
    cur.execute(query)

def create_assignments(cur):
    query = """
    CREATE TABLE IF NOT EXISTS assignments (
    id uuid PRIMARY KEY,
    name text,
    due_date timestamp,
    description text,
    course_id uuid,
    created_at timestamp,
    FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """
    cur.execute(query)

def create_assignment_submissions(cur):
    query = """
    CREATE TABLE IF NOT EXISTS assignment_submissions (
    assignment_id uuid,
    user_id uuid,
    filename text,
    created_at timestamp,
    PRIMARY KEY(assignment_id, user_id),
    FOREIGN KEY(assignment_id) REFERENCES assignments(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    cur.execute(query)

def create_materials(cur):
    query = """
    CREATE TABLE IF NOT EXISTS materials (
    id uuid PRIMARY KEY,
    name text,
    course_id uuid,
    file_name text,
    created_at timestamp,
    FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """
    cur.execute(query)

def create_queries(cur):
    query = """
    CREATE TABLE IF NOT EXISTS queries (
    id uuid PRIMARY KEY,
    query_text text,
    posted_by uuid,
    reply_to uuid,
    created_at timestamp,
    FOREIGN KEY(posted_by) REFERENCES users(id),
    FOREIGN KEY(reply_to) REFERENCES queries(id)
    )
    """
    cur.execute(query)

# def create_config(cur):
#     query = """
#     CREATE TABLE IF NOT EXISTS config (
#     id uuid PRIMARY KEY,
#     cur_term uuid,
#     FOREIGN KEY(cur_term) REFERENCES term(id)
#     )
#     """
#     cur.execute(query)

def create_everything():
    try:
        with sqlite3.connect('lms.db') as conn:
            cur = conn.cursor()
            create_roles(cur)
            create_users(cur)
            # create_term(cur)
            create_course(cur)
            create_assignments(cur)
            create_course_enrolled(cur)
            create_assignment_submissions(cur)
            create_materials(cur)
            create_queries(cur)
            # create_config(cur)
    except Exception as e:
        print(e)
        conn.rollback()
    else:
        conn.commit()
        cur.close()

create_everything()
