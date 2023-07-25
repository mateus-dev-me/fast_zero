import factory
from faker import Faker

from fast_zero.models import User

fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f'{fake.user_name()}')
    email = factory.Sequence(lambda n: f'{fake.email()}')
    password = factory.Sequence(lambda n: f'{fake.password()}')
