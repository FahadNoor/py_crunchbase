from src.py_crunchbase.entities import Collection, BaseCards, Entity
from src.py_crunchbase.entities.jobs import Jobs, JobCards, Job


def test_jobs():
    assert issubclass(Jobs, Collection)
    assert Jobs._name == 'jobs'


def test_job_cards():
    assert issubclass(JobCards, BaseCards)
    assert JobCards.organization == 'organization'
    assert JobCards.person == 'person'


def test_job():
    assert issubclass(Job, Entity)
    assert Job.ENTITY_DEF_ID == 'job'
    assert Job.Collection is Jobs
    assert Job.Cards is JobCards
