from src.service.api_service import APIService
from tkinter import Listbox, Button, PanedWindow, Tk, StringVar
from tkinter.filedialog import FileDialog


# TODO Adicionar biblioteca Gooey ao invés de tkinter (cli para gui, não testado para windows)
class GTKAdapter(Tk):
    service: APIService = None

    def __init__(self):
        super().__init__()
        self.spreadsheet = StringVar()

    def set_service(self, service: APIService):
        self.service = service
        return self

    def get_select_spreadsheet_component(self, master):
        select_spreadsheet_component = Listbox(master)
        select_spreadsheet_btn = Button(
            master=select_spreadsheet_component,
            text='Selecionar planilha',
            textvariable=self.spreadsheet
        )
        select_spreadsheet_btn.bind('click', self.set_spreadsheet)
        select_spreadsheet_btn.pack()
        return select_spreadsheet_component

    def set_spreadsheet(self):
        fd = FileDialog(self, title='Selecionar planilha de pesquisadores')
        files = fd.files

        if not files:
            return

        self.spreadsheet.set(files.get(first=0))

    def get_selected_spreadsheet_component(self, master):
        selected_spreadsheet_component = Listbox(master)
        return selected_spreadsheet_component
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
        pw = PanedWindow(master=self)
        self.get_select_spreadsheet_component(master=pw).pack()
        self.get_selected_spreadsheet_component(master=pw).pack()
        pw.pack(expand=1)

        self.mainloop()
