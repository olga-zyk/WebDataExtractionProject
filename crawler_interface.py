import abc


class CrawlerInterface:
    @abc.abstractmethod
    def get_data(self):
        pass
