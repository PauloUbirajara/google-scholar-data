from datetime import datetime

from scholarly import scholarly, ProxyGenerator

from src.model.scholar_info import ScholarInfo


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

        current_year_citations = get_current_year_citations(author_info)
        h10_index = calculate_h10_index(author_info)
        h_index = get_hindex(author_info)
        previous_5year_citations = get_5year_citations(author_info)

        info = ScholarInfo(
            current_year_citations=current_year_citations,
            h10_index=h10_index,
            h_index=h_index,
            previous_5year_citations=previous_5year_citations
        )

        return info


def get_current_year_citations(author) -> int:
    citations_per_year: dict = author.get('cites_per_year')
    CITATIONS_ON_ERROR = -1

    if citations_per_year is None:
        return CITATIONS_ON_ERROR

    current_year = datetime.now().year
    current_year_citation = citations_per_year.get(current_year, CITATIONS_ON_ERROR)
    return current_year_citation


def calculate_h10_index(author) -> int:
    publications = author.get('publications', [])
    paper_citations = [
        paper.get('num_citations', 0)
        for paper in publications
    ]
    papers_with_10_or_more_citations = [
        citation
        for citation in paper_citations
        if citation > 10
    ]
    h10_index = sum(papers_with_10_or_more_citations)
    return h10_index


def get_hindex(author) -> int:
    return author.get('hindex', 0)


def get_5year_citations(author) -> int:
    return author.get('citedby5y', 0)
