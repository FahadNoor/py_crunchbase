from .base import Entity, Collection, CardType


class Jobs(Collection):

    _name = 'jobs'
    _facet_name = 'job'


class JobCardType(CardType):

    organization = 'organization'
    person = 'person'


class Job(Entity):

    ENTITY_DEF_ID = 'job'
    Collection = Jobs
    CardType = JobCardType
