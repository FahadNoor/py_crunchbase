from .base import Entity, Collection, Cards


class Jobs(Collection):

    _name = 'jobs'
    _facet_name = 'job'


class JobCards(Cards):

    organization = 'organization'
    person = 'person'


class Job(Entity):

    ENTITY_DEF_ID = 'job'
    Collection = Jobs
    Cards = JobCards
