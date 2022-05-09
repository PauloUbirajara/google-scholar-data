from sys import argv
from gooey import Gooey, GooeyParser

from helper.logging_helper import info, error
from service.api_service import APIService
from service.google_scholar_service import GoogleScholarService
from src.strings.gooey_strings import description, language, program_name

spreadsheet_filters = [
    "Todos os arquivos|*.*",
    "Planilhas .xlsx|*.xlsx",
    "Planilhas .csv|*.csv",
    "Planilhas .xls|*.xls"
]


@Gooey(
    language=language,
    program_description=description,
    program_name=program_name
)
def render_gui(api: APIService):
    parser = GooeyParser()

    parser.add_argument(
        'planilha',
        metavar='Planilha',
        widget="FileChooser",
        help="Selecione o arquivo contendo os links dos pesquisadores",
        gooey_options={
            'wildcard': '|'.join(spreadsheet_filters)
        }
    )
    parser.add_argument(
        'coluna',
        metavar='Coluna',
        help="Nome da coluna onde estão os links dos pesquisadores",
        type=str
    )
    args = parser.parse_args(argv[1:])
    info(f'{args}')
    planilha, coluna = args.planilha, args.coluna

    try:
        if not planilha:
            err_message = "Não foi definido corretamente a planilha com os pesquisadores!"
            raise TypeError(err_message)

        user_args_message = f'''
        Planilha selecionada: {planilha}
        Coluna selecionada: {coluna}
        '''
        info(user_args_message)
        print(user_args_message)

        df_spreadsheet, errors = api.get_spreadsheet_with_citations(spreadsheet, column)
        if not errors:
            print('Citações obtidas com sucesso!')

        else:
            warn_message = 'Não foi possível obter citação para todos os pesquisadores.\n'
            'Links não realizados:\n'''
            "\n".join(errors)

            print(warn_message)
            warn(warn_message)

        result = f'''
        Citações obtidas com sucesso!
        Planilha final:
        {df_planilha.to_string()}
        '''
        info(result)
        print(result)

    except ValueError as err:
        err_message = "Houve algum erro durante a obtenção das citações da planilha!"
        print(err_message)
        error(err_message)
        error(repr(err))

    except Exception as err:
        err_message = "Houve algum erro durante a execução do programa!"
        print(err_message)
        error(err_message)
        error(repr(err))


if __name__ == '__main__':
    gss = GoogleScholarService()
    render_gui(gss)
