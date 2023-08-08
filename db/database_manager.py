import sqlite3

def dict_factory(c, r):
    d = {}
    for i, name in enumerate(c.description):
        d[name[0]] = r[i]
        d[i] = r[i]
    return d

class DataBaseManager():

    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = dict_factory

    def __del__(self):
        self.conn.close()

    def _execute(self, command: str, values = None):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(command, values or [])
            return cursor
        
    def create_table(self, table_name: str, columns: dict) -> None:
        colums_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(colums_with_types)});
            '''
        )

    def add(self, table_name: str, data: dict) -> None:
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values
        )
    
    def delete (self, table_name: str, criteria: dict) -> None:
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values()),
        )

    def select(self, table_name: str, criteria=None, order_by=None, limit=100) -> sqlite3.Cursor:
        criteria = criteria or {}
        
        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by}'
        
        query += f' LIMIT {limit}'

        return self._execute(
            query,
            tuple(criteria.values())
        )
    