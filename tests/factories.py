import factory
import factory.fuzzy
from faker import Faker

from fast_zero.models import Todo, TodoState, User

fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f'{fake.user_name()}')
    email = factory.Sequence(lambda n: f'{fake.email()}')
    password = factory.Sequence(lambda n: f'{fake.password()}')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Sequence(lambda n: f'{fake.text()[:20]}')
    description = factory.Sequence(lambda n: f'{fake.text()}')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = factory.SubFactory(UserFactory)
