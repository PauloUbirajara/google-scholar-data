from json import loads, JSONDecodeError, dumps
from os.path import exists
from re import findall, sub
from time import sleep
from urllib.parse import urlparse

import pandas as pd
from requests import get

from src.helper.logging_helper import info, error
from src.service.api_service import APIService

ENDPOINT_INTERVAL = 10


class GoogleScholarService(APIService):
    __errors: [str] = []

    def reset_error_count(self):
        self.__errors = []

    def increase_error_count(self, researcher_url):
        self.__errors.append(researcher_url)

    def current_errors(self):
        return self.__errors

    def get_spreadsheet_with_citations(
            self,
            file_path: str,
            column_name: str
    ) -> (pd.DataFrame, [str]):
        try:
            info("Reiniciar contagem de erros")
            self.reset_error_count()

            info("Tentar carregar a planilha")
            info(file_path)
            df_spreadsheet = self.__load_spreadsheet(file_path)

            info("Tentar obter a coluna")
            info(column_name)
            df_spreadsheet['Citações'] = df_spreadsheet[column_name].apply(self.__get_citations)

            info("Planilha obtida com sucesso")
            info(df_spreadsheet.to_string())

            return df_spreadsheet, self.current_errors()

        except KeyError as err:
            err_message = "Houve algum erro ao selecionar a coluna!"
            print(err_message, flush=True)
            error(err_message)
            error(repr(err))

        except Exception as err:
            err_message = "Houve outro tipo de erro ao buscar citações a partir de coluna!"
            print(err_message, flush=True)
            error(err_message)
            error(repr(err))

        finally:
            print("\n" * 3, flush=True)

        return None, self.current_errors()

    def __load_spreadsheet(self, file_path: str) -> pd.DataFrame:
        if not exists(file_path):
            raise ValueError("Planilha não existe")

        df_spreadsheet = pd.read_excel(file_path)
        df_filtered_spreadsheet = df_spreadsheet.dropna()

        return df_filtered_spreadsheet

    def __get_citations(self, researcher_url: str) -> int:
        while True:
            try:
                print("Iniciar busca para:", flush=True)
                print(researcher_url, flush=True)

                info("Tentar extrair user_id")
                user_id = self.__get_researcher_id(researcher_url)

                info(f'ID obtido: {user_id}')
                info("Tentar buscar na API")
                user_json = self.__get_citation_for_user_id(user_id)
                info("Dados obtidos da API")
                info(dumps(user_json))

                info("Tentar extrair citações do ano atual do texto")
                citations = self.__get_latest_year_citation_from_user_json(user_json)

                print("Citações obtidas com sucesso!", flush=True)
                info("Citações obtidas, esperar para não sobrecarregar o endpoint")
                sleep(ENDPOINT_INTERVAL)
                return citations

            except ValueError as err:
                err_message = f'Houve algum erro ao tentar obter citações para pesquisador:\n{researcher_url}'
                print(err_message, flush=True)
                error(err_message)
                error(repr(err))

            finally:
                print('\n', flush=True)

    def __get_researcher_id(self, profile_url: str) -> str:
        result = urlparse(profile_url)
        if not result.query:
            raise ValueError('Sem query')

        query = result.query
        pattern = r"user=[\-A-Za-z0-9]+"

        has_user_id = findall(pattern, query)

        if not has_user_id:
            info("Obter user_id de query")
            info(f'{query=}')
            info(f'{pattern=}')
            info(f'{has_user_id=}')
            raise ValueError('Sem id do usuário')

        _, user_id = has_user_id[0].split('=')
        return user_id

    def __get_citation_for_user_id(self, user_id: str) -> dict:
        endpoint = f'http://cse.bth.se/~fer/googlescholar-api/googlescholar.php?user={user_id}'
        info("Tentar acessar endpoint")
        info(endpoint)

        page = get(endpoint)
        info("Requisição feita - Estado da página:")
        info(str(page.ok))
        info(page.text)

        if not page.ok:
            raise ValueError('Erro ao completar requisição para API')

        try:
            filter_bad_params_pattern = r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})'
            filtered_page = sub(filter_bad_params_pattern, '', page.text)
            result = loads(filtered_page)
            return result

        except JSONDecodeError as err:
            err_message = 'Erro ao transformar conteúdo de página para dicionário'
            error(err_message)
            error(repr(err))
            raise ValueError(err_message)

        except Exception as err:
            err_message = 'Erro ao obter dados da API'
            error(err_message)
            error(repr(err))
            raise ValueError(err_message)

    def __get_latest_year_citation_from_user_json(self, user_info: dict) -> int:
        _, citations = [*user_info['citations_per_year'].items()][-1]
        return citations
