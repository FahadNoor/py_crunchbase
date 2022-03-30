from .base import Entity, Collection, BaseCards


class Jobs(Collection):

    _name = 'jobs'


class JobCards(BaseCards):

    organization = 'organization'
    person = 'person'


class Job(Entity):

    ENTITY_DEF_ID = 'job'
    Collection = Jobs
    Cards = JobCards
