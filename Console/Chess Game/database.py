import os
import sqlite3 as sql


########################
# Database Class
########################
class Database:
    def __init__(self, file: str):
        """ Constructor """
        # If folder doesn't exist
        if not os.path.exists('save'):
            os.mkdir('save')

        # Create database objects
        self.database = sql.connect(f'save/{file}')
        self.cursor = self.database.cursor()

    # Commit Query
    def commit(self, query: str) -> None:
        """ Method to commit queries to database """
        self.cursor.execute(query)
        self.database.commit()

    # Table Maker
    def createTable(self, name: str, header: list[str]) -> None:
        """ Method to create table """
        self.commit(f"""
            CREATE TABLE IS NOT EXISTS {name}(

                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                {','.join(head + ' INTEGER NOT NULL' for head in header)}
            )
        """)

    # Data Insertion
    def insertDataTo(self, table: str, header: list[str], values: list[int] | list[str]) -> None:
        """ Method to insert data into table """
        self.commit(f"INSERT INTO {table} {tuple(header)} VALUES ({','.join(['?' for i in range(len(values))])})",
                    tuple(values))

    # Data Retrieval
    def retrieveDataFrom(self, table: str, header: list[str], condition: str = "") -> list:
        """ Method to retrieve data from table """
        # Query
        query: str = f"SELECT {','.join(header) if len(header) > 1 else ''.join(header)} FROM {table}"

        # Condition
        if len(condition) > 0:
            query += f" WHERE {condition}"

        # Fetch data
        self.cursor.execute(query)
        data: list = self.cursor.fetchall()
        return data

    # Data Update
    def updateDataOf(self, table: str, header: list[str], values: list[int] | list[str], condition: str = "") -> None:
        """ Method to update data of a table """
        # Query
        query: str = f"UPDATE {table} SET {tuple(header)}"

        # Adding data that will be updated
        if isinstance(header, str) or len(header) == 1:
            query += f"{header} = '{values}'" if isinstance(values, str) else f"{header} = {values}"
        else:
            query += ', '.join(
                f"{header[i]} = '{v}'" if isinstance(v, str) else f"{header[i]} = {v}"
                for i, v in enumerate(values)
            )

        # Condition
        if len(condition) > 0:
            query += f" WHERE {condition};"

        # Query commit
        self.commit(query)

    # Data Deletion
    def removeDataFrom(self, table: str, condition: str) -> None:
        """ Method to remove data from a table """
        self.commit(f"DELETE FROM {table} WHERE {condition}")

    # Destructor
    def __del__(self):
        self.database.close()