"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

# How a database and a cursor are made
db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""
# Query we want to execute- don't need semicolon- use question mark instead of filter for where clause
    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone() # Use method fetchone(), which returns just one row
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_projects_by_title(title):
    """Given a project id, print information about the project title."""
# Query we want to execute- don't need semicolon- use question mark instead of filter for where clause
    QUERY = """
        SELECT id, title, description, max_grade
        FROM Projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone() # Use method fetchone(), which returns just one row, as a tuple
    print "Project ID: %s\nTitle: %s\nDescription: %s\nMax Grade: %s" % (
        row[0], row[1], row[2], row[3])

def get_grade_by_github_and_project_title(student_github, project_title):
    """Given a github account name and project title, print the grade of a matching student."""
# Query we want to execute- don't need semicolon- use question mark instead of filter for where clause
    QUERY = """
        SELECT student_github, project_title, grade
        FROM Grades
        WHERE student_github = ? AND project_title = ?
        """
    db_cursor.execute(QUERY, (student_github, project_title))
    row = db_cursor.fetchone() # Use method fetchone(), which returns just one row, as a tuple
    print "Github: %s\nProject Title: %s\nGrade: %s" % (
        row[0], row[1], row[2])

def give_grade_to_student(project_title):
    """Give a grade to a student."""
# Query we want to execute- don't need semicolon- use question mark instead of filter for where clause
    QUERY = """
        SELECT project_title, grade
        FROM Grades
        WHERE project_title = ?
        """
    db_cursor.execute(QUERY, (project_title,))
    row = db_cursor.fetchone() # Use method fetchone(), which returns just one row, as a tuple
    print "Project Title: %s\nGrade: %s" % (
        row[0], row[1])

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_title":
            title = args[0]
            get_projects_by_title(title)

        elif command == "grade":
            student_github, project_title = args
            get_grade_by_github_and_project_title(student_github, project_title)

        elif command == "assigned_grade":
            # project_title = raw_input("Project Title: ") #Cynthia asked about multiple inputs
            project_title = args[0]
            give_grade_to_student(project_title)

if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close() #After the main loop returns, we close our database connection.
