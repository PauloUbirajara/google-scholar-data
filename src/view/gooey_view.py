from gooey import Gooey, GooeyParser

from src.service.scholarly_service import ScholarlyService


@Gooey
def render():
    service = ScholarlyService

    fields = setup_gooey_fields()

    args = fields.parse_args()


def setup_gooey_fields() -> GooeyParser:
    parser = GooeyParser()

    # Preparar interface
    add_spreadsheet_field(parser)
    add_column_field(parser)

    # TODO Receber parâmetros e iterar pela planilha
    return parser


def add_spreadsheet_field(parser: GooeyParser):
    parser.add_argument(
        'spreadsheet',
        metavar="Planilha",
        help="Planilha contendo os dados de pesquisadores do Google Scholar",
        widget='FileChooser'
    )


def add_column_field(parser: GooeyParser):
    parser.add_argument(
        'column',
        metavar="Coluna",
        help="Coluna contendo apenas links do Google Scholar",
        type=str
    )
