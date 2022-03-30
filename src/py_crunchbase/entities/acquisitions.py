from .base import Entity, Collection, BaseCards


class Acquisitions(Collection):

    _name = 'acquisitions'


class AcquisitionCards(BaseCards):

    acquiree_organization = 'acquiree_organization'
    acquirer_organization = 'acquirer_organization'
    press_references = 'press_references'


class Acquisition(Entity):

    ENTITY_DEF_ID = 'acquisition'
    Collection = Acquisitions
    Cards = AcquisitionCards
