"""Factories for generating fake catalog data."""
# pylint: disable=missing-docstring, invalid-name
from functools import partial

import factory
from faker import Faker


fake = Faker()


def generate_instances(factory_class, count=3):
    """
    Use this to populate fields with values derived from other factories. If
    the array is used directly, the same value will be used repeatedly.
    """
    return factory_class.create_batch(count)


def generate_course_key():
    return '+'.join(fake.words(2))


def generate_course_run_key():
    return 'course-v1:' + '+'.join(fake.words(3))


def generate_zulu_datetime():
    """
    The catalog returns UTC datetimes formatted using Z, the zone designator
    for the zero UTC offset, not the +00:00 offset. For more, see
    https://en.wikipedia.org/wiki/ISO_8601#UTC.
    """
    return fake.date_time().isoformat() + 'Z'


def generate_price_ranges():
    return [{
        'currency': 'USD',
        'max': 1000,
        'min': 100,
        'total': 500
    }]


class DictFactoryBase(factory.Factory):
    """
    Subclass this to make factories that can be used to produce fake API response
    bodies for testing.
    """
    class Meta(object):
        model = dict


class ImageFactoryBase(DictFactoryBase):
    height = factory.Faker('random_int')
    width = factory.Faker('random_int')


class ImageFactory(ImageFactoryBase):
    """
    For constructing dicts mirroring the catalog's serialized representation of ImageFields.

    See https://github.com/edx/course-discovery/blob/master/course_discovery/apps/api/fields.py.
    """
    description = factory.Faker('sentence')
    src = factory.Faker('image_url')


class StdImageFactory(ImageFactoryBase):
    """
    For constructing dicts mirroring the catalog's serialized representation of StdImageFields.

    See https://github.com/edx/course-discovery/blob/master/course_discovery/apps/api/fields.py.
    """
    url = factory.Faker('image_url')


def generate_sized_stdimage():
    return {
        size: StdImageFactory() for size in ['large', 'medium', 'small', 'x-small']
    }


class OrganizationFactory(DictFactoryBase):
    key = factory.Faker('word')
    name = factory.Faker('company')
    uuid = factory.Faker('uuid4')
    logo_image_url = factory.Faker('image_url')


class SeatFactory(DictFactoryBase):
    type = factory.Faker('word')
    price = factory.Faker('random_int')
    currency = 'USD'


class CourseRunFactory(DictFactoryBase):
    eligible_for_financial_aid = True
    end = factory.LazyFunction(generate_zulu_datetime)
    enrollment_end = factory.LazyFunction(generate_zulu_datetime)
    enrollment_start = factory.LazyFunction(generate_zulu_datetime)
    image = ImageFactory()
    key = factory.LazyFunction(generate_course_run_key)
    marketing_url = factory.Faker('url')
    pacing_type = 'self_paced'
    seats = factory.LazyFunction(partial(generate_instances, SeatFactory))
    short_description = factory.Faker('sentence')
    start = factory.LazyFunction(generate_zulu_datetime)
    title = factory.Faker('catch_phrase')
    type = 'verified'
    uuid = factory.Faker('uuid4')


class CourseFactory(DictFactoryBase):
    course_runs = factory.LazyFunction(partial(generate_instances, CourseRunFactory))
    image = ImageFactory()
    key = factory.LazyFunction(generate_course_key)
    owners = factory.LazyFunction(partial(generate_instances, OrganizationFactory, count=1))
    title = factory.Faker('catch_phrase')
    uuid = factory.Faker('uuid4')


class JobOutlookItemFactory(DictFactoryBase):
    value = factory.Faker('sentence')


class PersonFactory(DictFactoryBase):
    bio = factory.fuzzy.FuzzyText()
    given_name = factory.Faker('first_name')
    family_name = factory.Faker('last_name')
    profile_image_url = factory.Faker('image_url')
    uuid = factory.Faker('uuid4')


class EndorserFactory(DictFactoryBase):
    person = PersonFactory()
    quote = factory.Faker('sentence')


class ExpectedLearningItemFactory(DictFactoryBase):
    value = factory.Faker('sentence')


class FAQFactory(DictFactoryBase):
    answer = factory.Faker('sentence')
    question = factory.Faker('sentence')


class ProgramFactory(DictFactoryBase):
    authoring_organizations = factory.LazyFunction(partial(generate_instances, OrganizationFactory, count=1))
    applicable_seat_types = ['verified']
    banner_image = factory.LazyFunction(generate_sized_stdimage)
    card_image_url = factory.Faker('image_url')
    courses = factory.LazyFunction(partial(generate_instances, CourseFactory))
    expected_learning_items = factory.LazyFunction(partial(generate_instances, CourseFactory))
    individual_endorsements = factory.LazyFunction(partial(generate_instances, EndorserFactory))
    is_program_eligible_for_one_click_purchase = True
    faq = factory.LazyFunction(partial(generate_instances, FAQFactory))
    job_outlook_items = factory.LazyFunction(partial(generate_instances, JobOutlookItemFactory))
    marketing_slug = factory.Faker('slug')
    marketing_url = factory.Faker('url')
    max_hours_effort_per_week = factory.fuzzy.FuzzyInteger(21, 28)
    min_hours_effort_per_week = factory.fuzzy.FuzzyInteger(7, 14)
    overview = factory.Faker('sentence')
    price_ranges = factory.LazyFunction(generate_price_ranges)
    staff = factory.LazyFunction(partial(generate_instances, PersonFactory))
    status = 'active'
    subtitle = factory.Faker('sentence')
    title = factory.Faker('catch_phrase')
    type = factory.Faker('word')
    uuid = factory.Faker('uuid4')
    weeks_to_complete = factory.fuzzy.FuzzyInteger(1, 45)


class ProgramTypeFactory(DictFactoryBase):
    name = factory.Faker('word')
    logo_image = factory.LazyFunction(generate_sized_stdimage)
