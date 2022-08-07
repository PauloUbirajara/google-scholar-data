from typing import Dict


class ScholarInfo:
    id: str
    h_index: int
    h10_index: int
    citations_dict: Dict[str, int]

    def __init__(self, researcher_id: str):
        self.id = researcher_id
        self.h_index = 0
        self.h10_index = 0
        self.citations_dict = {}

    def __str__(self):
        return '\n'.join(['', f'id: {self.id}', f'h_index: {self.h_index}', f'i10_index: {self.h10_index}',
                          f'citation_dict: {self.citations_dict}'])

    def set_h_index(self, new_h_index: int):
        self.h_index = new_h_index

    def set_i10_index(self, new_h10_index: int):
        self.h10_index = new_h10_index

    def set_citations_dict(self, new_citations_dict: Dict[str, int]):
        self.citations_dict = new_citations_dict
