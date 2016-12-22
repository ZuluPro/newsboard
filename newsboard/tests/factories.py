try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import factory
from factory import fuzzy
import faker
from dj_web_rich_object.tests import factories as wro_factories

from newsboard import models

STREAM_TYPES = [k for k, v in models.STREAM_TYPES]

faker = faker.Faker()


def lazy_remote_id(post):
    if post.type == 'facebook':
        return faker.numerify('############')
    elif post.type == 'sitemap':
        return urljoin(post.main_url, 'sitemap.xml')
    else:
        return urljoin(post.main_url, 'feed')


class StreamFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('company')
    description = factory.Faker('sentence', nb_words=25)
    type = fuzzy.FuzzyChoice(models.STREAM_TYPES)

    remote_id = factory.LazyAttribute(lazy_remote_id)
    main_url = factory.Faker('url')

    last_updated = factory.Faker('date_time_between', start_date='-1d', end_date='now')

    auto_enabled = factory.Faker('boolean')
    auto_frequency = factory.fuzzy.FuzzyDecimal(1, 10)

    class Meta:
        model = 'newsboard.Stream'


class PostFactory(wro_factories.WebRichObjectFactory):
    @factory.post_generation
    def streams(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for stream in extracted:
                self.streams.add(stream)

    class Meta:
        model = 'newsboard.Post'
