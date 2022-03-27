from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.acquisitions import Acquisitions, AcquisitionCards, Acquisition


def test_acquisitions():

    assert issubclass(Acquisitions, Collection)
    assert Acquisitions._name == 'acquisitions'


def test_acquisition_cards():
    assert issubclass(AcquisitionCards, BaseCards)
    assert AcquisitionCards.acquiree_organization == 'acquiree_organization'
    assert AcquisitionCards.acquirer_organization == 'acquirer_organization'
    assert AcquisitionCards.press_references == 'press_references'


def test_acquisition():
    assert issubclass(Acquisition, Entity)
    assert Acquisition.ENTITY_DEF_ID == 'acquisition'
    assert Acquisition.Collection is Acquisitions
    assert Acquisition.Cards is AcquisitionCards
