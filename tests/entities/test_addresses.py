from py_crunchbase.entities import Collection, BaseCards, Entity
from py_crunchbase.entities.addresses import Addresses, AddressCards, Address


def test_addresses():
    assert issubclass(Addresses, Collection)
    assert Addresses._name == 'addresses'


def test_address_cards():
    assert issubclass(AddressCards, BaseCards)
    assert AddressCards.event == 'event'
    assert AddressCards.organization == 'organization'


def test_address():
    assert issubclass(Address, Entity)
    assert Address.ENTITY_DEF_ID == 'address'
    assert Address.Collection is Addresses
    assert Address.Cards is AddressCards
