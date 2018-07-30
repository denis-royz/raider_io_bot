from pydblite.sqlite import Database, Table
from model.user import User


class UserService:

    def __init__(self):
        self.getByTelegramId = None
        self.db = Database("db/raider_io.db")

        self.users_table = Table('users_table', self.db)
        if len(self.users_table.info()) is 0:
            self.users_table.create(('name', 'TEXT'), ('telegram_id', 'TEXT'))
        else:
            self.users_table.open()

        self.subscription_table = Table('subscription_table', self.db)
        if len(self.subscription_table.info()) is 0:
            self.subscription_table.create(('user_name', 'TEXT'), ('region', 'TEXT'),
                                           ('realm', 'TEXT'), ('character_name', 'TEXT'))
        else:
            self.subscription_table.open()

    def insert(self, user):
        self.users_table.insert(name=user.name, telegram_id=user.telegram_id)
        self.users_table.commit()

    def authorize_or_create(self, telegram_id):
        user = self.authorize(telegram_id=telegram_id)
        if user is None:
            user = User(telegram_id, telegram_id)
            self.insert(user)
        return user

    def authorize(self, telegram_id):
        records = self.users_table(telegram_id=telegram_id)
        if len(records) == 0:
            return None
        if len(records) > 1:
            raise Exception('Expected one result, but got {0}'.format(len(records)))
        record = records[0]
        user = User(record['name'], record['telegram_id'])
        return user

    def subscribe(self, user, region, realm, character_name):
        records = self.subscription_table(user_name=user.name,
                                          region=region, realm=realm, character_name=character_name)
        if (len(records))is 0:
            self.subscription_table.insert(user_name=user.name,
                                           region=region, realm=realm, character_name=character_name)
            self.users_table.commit()
            return 1
        return 0

    def get_subscriptions(self, user):
        return self.subscription_table(user_name=user.name)


