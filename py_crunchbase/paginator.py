class Paginator:

    def __init__(self, api: 'Paginated'):
        self.api = api
        self.current_list = None

    def next(self):
        if self.current_list is not None:
            try:
                self.api.set_next(self.current_list)
            except IndexError as exc:
                raise StopIteration from exc

        self.current_list = self.api.execute()
        return self.current_list

    def previous(self):
        if self.current_list is not None:
            try:
                self.api.set_previous(self.current_list)
            except IndexError as exc:
                raise StopIteration from exc

        self.current_list = self.api.execute()
        return self.current_list

    def __iter__(self):
        return self

    def __next__(self):
        data = self.next()
        if not data:
            raise StopIteration
        return data


class Paginated:
    """
    This is an interface that should be implemented by the class that needs to provide a paginator.
    """

    paginator_cls = Paginator

    def set_next(self, *args, **kwargs):
        """
        This method will receive current page (list of data). Paginated class can use last entry in the data
        to figure out next page. It should be used just for configuration.
        """
        raise NotImplementedError

    def set_previous(self, *args, **kwargs):
        """
        This method will receive current page (list of data). Paginated class can use first entry in the data
        to figure out previous page. It should be used just for configuration.
        """
        raise NotImplementedError

    def execute(self) -> list:
        """
        This should return next/previous page depending on the configuration
        """
        raise NotImplementedError

    def iterate(self):
        """
        returns Paginator to go through pages
        Usage:
        for page in api.iterate():
            for data in page:
                print(data)
        """
        return self.paginator_cls(self)
