from .base import Entity, Collection, Cards


class Acquisitions(Collection):

    _name = 'acquisitions'
    _facet_name = 'acquisition'


class AcquisitionCards(Cards):

    acquiree_organization = 'acquiree_organization'
    acquirer_organization = 'acquirer_organization'
    press_references = 'press_references'


class Acquisition(Entity):

    ENTITY_DEF_ID = 'acquisition'
    Collection = Acquisitions
    Cards = AcquisitionCards
