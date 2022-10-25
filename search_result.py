"""
SearchResult
"""


class SearchResult:  # pylint: disable=R0903
    """
    Holds the place and its match count for search query
    """
    def __init__(self, place, match_amount: float):
        self.place = place
        self.match_amount = match_amount
