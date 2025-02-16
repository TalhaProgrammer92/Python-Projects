# Importing Modules
import sqlite3 as sq

"""
=========================================================================
SQLite 3 Data Types:
=========================================================================
- NULL: NULL / Empty
- INTEGER: To store integer values i.e. whole numbers
- REAL: To store floating-point values
- TEXT: To store string
- BLOB: To store objects i.e. images, videos, files, etc

=========================================================================
SQLite 3 Constraints:
=========================================================================
- PRIMARY KEY: To make row a primary key of a certain table
"""

# Connecting to database server
#db = sq.connect(':memory:')        # In-memory (Not Permanent)
db = sq.connect('student.db')      # In-storage (Permanent)

# Cursor Creation
cursor = db.cursor()

# Execute SQL commands / queries
# cursor.execute("""
# -- Creating a table in the student.db
# CREATE TABLE Students_Info (
#         -- Header
#         Roll INTEGER PRIMARY KEY,
#         First_name TEXT,
#         Last_name TEXT,
#         Age INTEGER
#     )
# """)

# Insert data
# cursor.execute("""
# INSERT INTO Students_Info VALUES (
#         2238,
#         'Rayan',
#         'Zulfiqar',
#         19
#     )
# """)

# Commit the commands / queries
db.commit()

# Close the database connection
db.close()

# Message
print('Successful!')
