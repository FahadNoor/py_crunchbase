from .base import Entity, Collection, CardType


class Acquisitions(Collection):

    _name = 'acquisitions'
    _facet_name = 'acquisition'


class AcquisitionCardType(CardType):

    acquiree_organization = 'acquiree_organization'
    acquirer_organization = 'acquirer_organization'
    press_references = 'press_references'


class Acquisition(Entity):

    ENTITY_DEF_ID = 'acquisition'
    Collection = Acquisitions
    CardType = AcquisitionCardType
