from src.service.api_service import APIService


class GTKAdapter:
    service: APIService = None

    def __init__(self):
        super().__init__()

    def set_service(self, service: APIService):
        self.service = service
        return self

    # def get_select_spreadsheet_component(self):
    #     select_spreadsheet_component = Listbox()
    #     select_spreadsheet_btn = Button(
    #         master=select_spreadsheet_component,
    #         text='Selecionar planilha'
    #     )
    #     # select_spreadsheet_btn.bind(on_press=)
    #     select_spreadsheet_btn.pack()
    #     return select_spreadsheet_component
    #
    # def get_selected_spreadsheet_component(self):
    #     raise Exception("Not implemented")
    #
    # def get_selected_spreadsheet_preview_component(self):
    #     raise Exception("Not implemented")
    #
    # def get_search_for_citations_component(self):
    #     btn = Button(text='Buscar citações')
    #     btn.bind(on_press=self.search_for_citations)
    #     return btn
    #
    # def search_for_citations(self, _btn):
    #     pass

    def render(self):
        if self.service is None:
            raise ValueError('Não foi definido um serviço do Google Scholar!')

        # bl.add_widget(self.get_select_spreadsheet_component())  # bl.add_widget(self.get_selected_spreadsheet_component())  # bl.add_widget(self.get_selected_spreadsheet_preview_component())  # bl.add_widget(self.get_search_for_citations_component())

        # self.mainloop()
