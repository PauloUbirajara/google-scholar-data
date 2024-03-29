from os.path import exists
from re import findall
from urllib.parse import urlparse

import pandas as pd
from gooey import Gooey, GooeyParser

from src.exception.exceptions import InvalidInputException, InvalidResearcherURLException, FetchException
from src.helper.date_helper import timestamp_as_string
from src.helper.logging_helper import info, error, warn
from src.model.scholar_info import ScholarInfo
from src.service.selenium_service import SeleniumService, VALUE_IF_NOT_FOUND
from src.strings.gooey_strings import program_name, description, language

CURRENT_RESEARCHER_INDEX = 0
SPREADSHEET_RESEARCHER_COUNT = 1
SCHOLAR_SERVICE = SeleniumService


@Gooey(program_name=program_name, program_description=description, language=language)
def render():
    info("Preparar interface")
    parser = setup_gooey_fields()

    info("Receber parâmetros")
    args = parser.parse_args()
    fields = args.__dict__

    info("Validar parâmetros")
    validate_fields(fields)

    info("Iterar pela planilha")
    fetch_data_from_fields(fields)


def setup_gooey_fields() -> GooeyParser:
    parser = GooeyParser()

    add_spreadsheet_field(parser)
    add_column_field(parser)

    return parser


def validate_fields(fields: dict):
    try:
        spreadsheet = fields.get('spreadsheet')
        validate_spreadsheet(spreadsheet)
        info("Campo 'Planilha' validado corretamente")

        column = fields.get('column')
        validate_column(spreadsheet, column)
        info("Campo 'Coluna' validado corretamente")

    except InvalidInputException as err:
        error("Erro ao validar campos")
        error(repr(err))
        raise err


def add_spreadsheet_field(parser: GooeyParser):
    file_options = '|'.join(
        ["Planilha (*.xls)|*.xls", "Planilha (*.xlsx)|*.xlsx"]
    )
    gooey_options = {
        'wildcard': file_options, 'message': "Escolha uma planilha"
    }
    parser.add_argument(
        'spreadsheet',
        metavar="Planilha",
        help="Planilha contendo os dados de pesquisadores do Google Scholar",
        widget='FileChooser',
        gooey_options=gooey_options
    )


def add_column_field(parser: GooeyParser):
    parser.add_argument(
        'column', metavar="Coluna", help="Coluna contendo apenas links do Google Scholar", type=str
    )


def validate_spreadsheet(file: str):
    if not exists(file):
        raise InvalidInputException(
            field_name='Planilha', reason='Não existe'
        )

    SPREADSHEET_TYPES = ('.xlsx', '.xls')

    if not file.lower().endswith(SPREADSHEET_TYPES):
        raise InvalidInputException(
            field_name='Planilha', reason='Extensão inválida'
        )


def validate_column(spreadsheet: str, column: str):
    df_spreadsheet = pd.read_excel(spreadsheet)
    if column not in df_spreadsheet.columns:
        raise InvalidInputException(
            field_name='Coluna', reason='Não existe na planilha'
        )


def fetch_data_from_fields(fields: dict):
    spreadsheet_file = fields.get('spreadsheet')
    spreadsheet = pd.ExcelFile(spreadsheet_file)
    column = fields.get('column')

    researcher_data = {}
    info(f'Iniciar busca em planilha "{spreadsheet_file}"')

    output_file = f'citations_{timestamp_as_string()}.xlsx'

    for page in spreadsheet.sheet_names:
        info(f'Iniciar busca na página "{page}"')

        df_spreadsheet = pd.read_excel(
            io=spreadsheet_file, sheet_name=page
        )

        global CURRENT_RESEARCHER_INDEX
        global SPREADSHEET_RESEARCHER_COUNT

        CURRENT_RESEARCHER_INDEX = 1
        SPREADSHEET_RESEARCHER_COUNT = df_spreadsheet.shape[0]

        # Adicionar colunas com novos resultados
        df_spreadsheet[expected_columns_from_service()] = df_spreadsheet.apply(
            func=lambda researcher: fetch_researcher_from_row(researcher[column]),
            axis=1,
            result_type='expand'
        )
        warn("Dados coletados:")
        warn(df_spreadsheet.to_string())
        researcher_data[page] = df_spreadsheet

        info("Salvar na planilha nova")
        save_researcher_data_to_new_spreadsheet(output_file, researcher_data)


def save_researcher_data_to_new_spreadsheet(output_file: str, researcher_data: dict):
    info(f'Salvar dados em planilha "{output_file}"')

    with pd.ExcelWriter(path=output_file, engine='openpyxl') as writer:
        for page, content in researcher_data.items():
            info(f'Salvar dados na página "{page}"')
            content.to_excel(writer, sheet_name=page)


def fetch_researcher_from_row(link: str):
    if pd.isna(link):
        invalid_researcher_data = [pd.NA] * len(expected_columns_from_service())
        return invalid_researcher_data

    researcher_data = [0] * len(expected_columns_from_service())

    show_current_progress()
    increase_current_progress()

    try:
        info(f"Buscando pesquisador: {link}")

        researcher = fetch_link_from_service(link)

        info('Pesquisador OK')
        warn(researcher.__str__())

        researcher_data = [
            researcher.h_index,
            researcher.h10_index,
            *[
                researcher.citations_dict.get(year, VALUE_IF_NOT_FOUND)
                for year in expected_years()
            ]
        ]

        warn(str(researcher_data))

    except FetchException as err:
        info('Erro ao buscar link de pesquisador na API')
        info(link)
        error(repr(err))

    print(flush=True)

    return researcher_data


def fetch_link_from_service(link: str) -> ScholarInfo:
    try:
        if pd.isna(link):
            raise FetchException("Link nulo")

        researcher_id = get_researcher_id(link)
        researcher = SCHOLAR_SERVICE.fetch_info(researcher_id)

        if researcher is None:
            raise FetchException("Erro durante busca de informações na API")

        return researcher

    except InvalidResearcherURLException:
        raise FetchException("URL fornecida inválida")


def expected_years():
    return ['2015', '2016', '2016', '2017', '2018', '2019', '2020', '2021', '2022']


def expected_columns_from_service():
    return ['H Index', 'H10 Index', 'Citações - 2015', 'Citações - 2016', 'Citações - 2016', 'Citações - 2017',
            'Citações - 2018', 'Citações - 2019', 'Citações - 2020', 'Citações - 2021', 'Citações - 2022']


def get_researcher_id(link: str) -> str:
    result = urlparse(link)

    if not result.query:
        raise InvalidResearcherURLException(link)

    query = result.query
    pattern = r"user=[\-\_A-Za-z0-9]+"

    has_user_id = findall(pattern, query)

    if not has_user_id:
        raise InvalidResearcherURLException(link)

    _, user_id = has_user_id[0].split('=')
    return user_id


def show_current_progress():
    global CURRENT_RESEARCHER_INDEX
    global SPREADSHEET_RESEARCHER_COUNT

    current_count = CURRENT_RESEARCHER_INDEX
    total_count = SPREADSHEET_RESEARCHER_COUNT

    progress_percentage = float(current_count) / float(total_count) * 100.0
    progress_str = f'Pesquisador {current_count}/{total_count} ({progress_percentage:.2f}%)'
    print(progress_str, flush=True)


def increase_current_progress():
    global CURRENT_RESEARCHER_INDEX
    CURRENT_RESEARCHER_INDEX += 1
