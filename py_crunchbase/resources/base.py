from ..utils import DataDict


class Resource(DataDict):
    """
    Base class to represent all resources
    """

    API_PATH = ''
    AVAILABLE_FIELDS = tuple()
    ENTITY_DEF_ID = ''

    def __init__(self, data: dict, uuid: str = None, cards: dict = None):
        self._original_response = data
        self.uuid = uuid or data.get('uuid')
        cards = cards or data.get('cards')
        self.cards = DataDict(cards) if isinstance(cards, dict) else cards
        data = data.get('properties', data)
        super().__init__(data)

    @property
    def cb_web_url(self) -> str:
        return f'https://www.crunchbase.com/{self.ENTITY_DEF_ID}/{self.identifier.permalink}'
