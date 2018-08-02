from pydblite.sqlite import Database, Table


class DatabaseService:

    user_schema = ('name', 'TEXT'), ('telegram_id', 'TEXT')
    character_subscription_schema = ('user_name', 'TEXT'), ('region', 'TEXT'),\
                                    ('realm', 'TEXT'), ('character_name', 'TEXT')

    def __init__(self):
        self.db = Database("db/raider_io.db")

        self.users_table = self.create_schema(self.db, 'users_table', self.user_schema)
        self.character_subscription_table = self.create_schema(self.db, 'character_subscription_table',
                                                               self.character_subscription_schema)

    @staticmethod
    def create_schema(db, table_name, table_schema):
        table = Table(table_name, db)
        if len(table.info()) is 0:
            table.create(*table_schema)
        else:
            table.open()
        return table