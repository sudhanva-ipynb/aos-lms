import sqlite3
import uuid


def add_user(username,email,password,role,phone):
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    c.execute("""
                WITH role_match as (SELECT id FROM roles WHERE name = ? LIMIT 1) 
    
                 INSERT INTO users(id,username,email,password,phone,role_id,created_at) SELECT ?,?,?,?,?,id,CURRENT_TIMESTAMP FROM role_match;
                    
                    """,(role,str(uuid.uuid4()),username,email,password,phone))
    conn.commit()
    conn.close()

def create_course(instructor,name,code):
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    c.execute("""
                     WITH instructor_match as (SELECT u.id FROM users u WHERE username = ? LIMIT 1) 
    
                 INSERT INTO courses(id,course_name,course_code,instructor_id,created_at) SELECT ?,?,?,id,CURRENT_TIMESTAMP FROM instructor_match;

                        """,(instructor,str(uuid.uuid4()),name,code))
    conn.commit()
    conn.close()

def create_roles(name):
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    c.execute("""
                    INSERT INTO roles(name,id) VALUES(?,?);

                        """,(name,str(uuid.uuid4())))
    conn.commit()


# def create_terms(name):
#     conn = sqlite3.connect('lms.db')
#     c = conn.cursor()
#     c.execute("""
#                     INSERT INTO term(id,term_name,created_at) VALUES(?,?,CURRENT_TIMESTAMP);
#
#                         """,(str(uuid.uuid4()),name))
#     conn.commit()

# def insert_config():
#     conn = sqlite3.connect('lms.db')
#     c = conn.cursor()
#     c.execute("""INSERT INTO config(id,cur_term) SELECT ?,id FROM term WHERE term_name = 'Fall 2024' """,(str(uuid.uuid4()),))
#     conn.commit()
#     conn.close()

def enroll_students():
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    c.execute("""INSERT INTO course_enrolled SELECT u.id,c.id,CURRENT_TIMESTAMP FROM courses c , users u WHERE u.role_id = 'c39f83e2-cf23-4ffc-9002-b20da120edbc';

                            """)
    conn.commit()


# enroll_students()
# execute_query()
# create_roles('Instructor')
# create_terms("Spring 2025")
# insert_config()
# create_course("sudhanva","AOS","CS001")
# add_user('h20240196','h20240196@pilani.bits-pilani.ac.in','9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c','Student','9094473645')