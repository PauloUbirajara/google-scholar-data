from sys import argv

import pandas as pd
from gooey import Gooey, GooeyParser

from service.api_service import APIService
from service.google_scholar_service import GoogleScholarService
from src.strings.gooey_strings import description, language, program_name

columns = None


@Gooey(
    language=language,
    program_name=program_name,
    program_description=description,
)
def render_gui(api: APIService):
    parser = GooeyParser()
    parser.add_argument(
        'Planilha',
        widget="FileChooser",
        help="Selecione o arquivo contendo os links dos pesquisadores",
        gooey_options={
            'wildcard':
                "Todos os arquivos (*.*)|*.*|"
                "Planilhas .csv|*.csv|"
                "Planilhas .xls|*.xls|"
                "Planilhas .xlsx|*.xlsx|"
        }
    )
    parser.add_argument('Coluna', help="Nome da coluna onde estão os links dos pesquisadores", type=str)
    args = parser.parse_args()
    # print(args)
    # print(argv)
    try:
        planilha, coluna = argv[2:]
        df_planilha = api.get_spreadsheet_with_citations(planilha, coluna)
        print(df_planilha)
    except ValueError as err:
        print("Houve algum erro durante a obtenção das citações da planilha!")
        print(repr(err))


def change_spreadsheet(file: str):
    spreadsheet_types = ('xlsx', 'xls', 'csv')

    if not file.lower().endswith(spreadsheet_types):
        raise TypeError("Tipo de arquivo selecionado não é uma planilha")

    return pd.read_csv(file)


if __name__ == '__main__':
    gss = GoogleScholarService()
    render_gui(gss)
