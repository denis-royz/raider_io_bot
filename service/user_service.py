from model.user import User


class UserService:

    def __init__(self, database_service):
        self.users_table = database_service.users_table
        self.character_subscription_table = database_service.character_subscription_table
        self.db = database_service.db

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
        records = self.character_subscription_table(user_name=user.name,
                                                    region=region, realm=realm, character_name=character_name)
        if (len(records))is 0:
            self.character_subscription_table.insert(user_name=user.name,
                                                     region=region, realm=realm, character_name=character_name)
            self.users_table.commit()
            return 1
        return 0

    def unsubscribe_all(self, user):
        records = self.character_subscription_table(user_name=user.name)
        for record in records:
            del self.character_subscription_table[record['__id__']]

    def get_subscriptions(self, user):
        return self.character_subscription_table(user_name=user.name)


