import aiosqlite


class AioDataBase:
    def __init__(self, database_path) -> None:
        self.database_path = database_path
        
    async def create_table(self, table_name, columns:dict[str:str]):
        query = '''
            CREATE TABLE IF NOT EXISTS {table_name}(
                {columns}
            )
        '''
        cols = ''
        for column, type in columns.items():
            cols += f'{column} {type},'
        query = query.format(table_name = table_name,
                             columns = cols[:-1])
        await self._execute(query)
            
    async def insert(self, table, data:dict[str:str]):
        '''
        data = {'column_name', 'value'}
        '''
        query = 'INSERT INTO {table} ({columns}) VALUES ({values})'
        cols = ''
        vals = ''
        for column, value in data.items():
            cols += f'{column},'
            vals += f'"{value}",'
        query = query.format(table = table, columns = cols[:-1], values = vals[:-1])
        await self._execute(query)
            
    async def update(self, table, column, value, condition_column, condition_value):
        query = f'''
            UPDATE {table}
            SET {column} = "{value}"
            WHERE {condition_column} = "{condition_value}"
        '''
        await self._execute(query)
            
    async def delete(self, table, condition_column, condition_value):
        query = f'''
            DELETE FROM {table}
            WHERE {condition_column} = "{condition_value}"
        '''
        await self._execute(query)
    
    async def select(self, table, columns, condition_column, condition_value):
        query = f'''
            SELECT {columns}
            FROM {table}
            WHERE {condition_column} = "{condition_value}"
        '''
        rows = []
        async with aiosqlite.connect(self.database_path) as database:
            async with database.execute(query) as cursor:
                async for row in cursor:
                    rows.append(row)
        return rows
            
    
    async def _execute(self, query):
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute(query)
            await database.commit()

