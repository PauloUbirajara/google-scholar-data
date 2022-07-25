from scholarly import scholarly, ProxyGenerator

from src.helper.date_helper import current_year
from src.model.scholar_info import ScholarInfo

VALUE_IF_NOT_FOUND = 0


class ScholarlyService:
    has_set_proxies = False

    @staticmethod
    def setup_proxies():
        ScholarlyService.has_set_proxies = True

        # Usar proxies para evitar rastreamento pelo Google Scholar
        pg = ProxyGenerator()
        pg.FreeProxies()
        scholarly.use_proxy(pg)

    @staticmethod
    def fetch_info(researcher_id: str) -> ScholarInfo:
        if not ScholarlyService.has_set_proxies:
            ScholarlyService.setup_proxies()

        result = scholarly.search_author_id(researcher_id)
        author_info = scholarly.fill(result)

        h_index = get_hindex(author_info)
        h10_index = calculate_h10_index(author_info)
        current_year_citations = get_current_year_citations(author_info)
        previous_5year_citations = get_5year_citations(author_info)

        info = ScholarInfo()

        info.set_h_index(h_index)
        info.set_h10_index(h10_index)
        info.set_current_year_citations(current_year_citations)
        info.set_previous_5year_citations(previous_5year_citations)

        return info


def get_hindex(author) -> int:
    h_index = author.get('hindex', VALUE_IF_NOT_FOUND)
    return h_index


def calculate_h10_index(author) -> int:
    h10_index = author.get('i10index', VALUE_IF_NOT_FOUND)
    return h10_index


def get_current_year_citations(author) -> int:
    citations_per_year: dict = author.get('cites_per_year')

    if citations_per_year is None:
        return VALUE_IF_NOT_FOUND

    current_year_citation = citations_per_year.get(current_year(), VALUE_IF_NOT_FOUND)
    return current_year_citation


def get_5year_citations(author) -> int:
    return author.get('citedby5y', VALUE_IF_NOT_FOUND)
