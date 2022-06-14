import sqlite3

from common.config import Config


class Sql:
    def __init__(self):
        self.db_config = Config().db_config
        self.conn = sqlite3.connect(self.db_config['db_path'])
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS gitlab (id type UNIQUE, commit_id)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS github (id type UNIQUE, commit_id)''')
        self.conn.commit()

    def find_last_commit_id(self, table_name, project_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * from gitlab where id == :project_id", {"project_id": project_id})
        return_data = cur.fetchone()
        if return_data:
            _, commit_id = return_data
        else:
            commit_id = None
        return commit_id

    def add_commit_to_db(self, table_name, project_id, commit_id):
        sql_statement = f"INSERT OR REPLACE INTO {table_name} VALUES ({project_id}, \"{commit_id}\")"
        cur = self.conn.cursor()
        cur.execute(sql_statement)
        self.conn.commit()
