# !/usr/bin/env Python
# # coding=utf-8

import pandas as pd
import sys
from gooey import Gooey, GooeyParser
from os.path import join

from helper.date_helper import timestamp_as_string
from helper.logging_helper import info, warn, error
from service.api_service import APIService
from service.google_scholar_service import GoogleScholarService
from src.strings.gooey_strings import description, language, program_name

spreadsheet_filters = [
    "Planilhas .xls|*.xls",
    "Planilhas .xlsx|*.xlsx",
    # "Planilhas .csv|*.csv"
]


@Gooey(
    disable_stop_button=False,
    language=language,
    program_description=description,
    program_name=program_name
)
def render_gui(api: APIService):
    parser = GooeyParser()

    parser.add_argument(
        'spreadsheet',
        metavar='Planilha',
        widget="FileChooser",
        help="Selecione o arquivo contendo os links dos pesquisadores",
        gooey_options={
            'wildcard': '|'.join(spreadsheet_filters),
            'default_dir': '~/Downloads'
        }
    )
    parser.add_argument(
        'column',
        metavar='Coluna',
        help="Nome da coluna onde estão os links dos pesquisadores",
        type=str
    )

    args = parser.parse_args(sys.argv[1:])
    info(f'{args}')
    spreadsheet, column = args.spreadsheet, args.column

    try:
        # TODO Adicionar funções para verificar / Verificar ao modificar parâmetro
        #  - Verificar se planilha termina com os tipos permitidos
        #  - Verificar se a planilha de saída termina com .xlsx

        # TODO Buscar biblioteca para abrir em .csv (?)
        # TODO Buscar biblioteca para salvar em .xls (?)
        # TODO Verificar/Tratar criação de tabela caso existam células vazias

        if not spreadsheet:
            err_message = "Não foi definido corretamente a planilha com os pesquisadores!"
            raise TypeError(err_message)

        user_args_message = f'''
        Planilha selecionada: {spreadsheet}
        Coluna selecionada: {column}
        '''
        info(user_args_message)
        print(user_args_message, flush=True)

        df_spreadsheet, errors = api.get_spreadsheet_with_citations(spreadsheet, column)

        if df_spreadsheet is None:
            err_message = "Não foi possível continuar a operação, erro ao obter a planilha"
            raise ValueError(err_message)

        if errors:
            warn_message = 'Não foi possível obter citação para todos os pesquisadores.\n'
            'Links não realizados:\n'''
            "\n".join(errors)

            print(warn_message, flush=True)
            warn(warn_message)

        else:
            success_message = 'Citações obtidas com sucesso!'
            print(success_message, flush=True)
            info(success_message)

        result = f'''
        Planilha final:
        {df_spreadsheet.to_string()}
        '''
        info(result)
        print(result, flush=True)

        save_spreadsheet(df_spreadsheet=df_spreadsheet)

    except ValueError as err:
        err_message = "Houve algum erro durante a obtenção das citações da planilha!"
        print(err_message, flush=True)
        error(err_message)
        error(repr(err))

    except Exception as err:
        err_message = "Houve algum erro durante a execução do programa!"
        print(err_message, flush=True)
        error(err_message)
        error(repr(err))


def save_spreadsheet(df_spreadsheet: pd.DataFrame):
    output_folder = '.'
    formated_timestamp = timestamp_as_string()
    output_file = join(output_folder, f'citations_{formated_timestamp}.xlsx')
    try:
        result = f'''
        Salvando planilha em local específicado pelo usuário:
        {output_file}
        '''
        print(result, flush=True)
        info(result)
        df_spreadsheet.to_excel(output_file)

    except NotADirectoryError as err:
        err_message = "Pasta específicada para salvar planilha com citações não existe!"
        print(err_message, flush=True)
        error(err_message)
        error(repr(err))

    except Exception as err:
        err_message = "Houve um erro ao salvar planilha com citações."
        print(err_message, flush=True)
        error(err_message)
        error(repr(err))


if __name__ == '__main__':
    gss = GoogleScholarService()
    render_gui(gss)
