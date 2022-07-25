class ScholarInfo:
    h_index: int
    h10_index: int
    current_year_citations: int
    previous_5year_citations: int

    def set_h_index(self, new_h_index: int):
        self.h_index = new_h_index

    def set_h10_index(self, new_h10_index: int):
        self.h10_index = new_h10_index

    def set_current_year_citations(self, new_current_year_citations: int):
        self.current_year_citations = new_current_year_citations

    def set_previous_5year_citations(self, new_previous_5year_citations: int):
        self.previous_5year_citations = new_previous_5year_citations
