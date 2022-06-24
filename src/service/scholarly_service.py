from scholarly import scholarly

from src.types.scholar_info import ScholarInfo


class ScholarlyService:
    @staticmethod
    def fetch_info(id: str) -> ScholarInfo:
        result = scholarly.search_author_id(id)
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
    return author.get('citedby', 0)


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
