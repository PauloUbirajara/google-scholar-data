from json import loads, JSONDecodeError
from os.path import exists
from re import match
from urllib.parse import urlparse

import pandas as pd
from requests import get

from src.service.api_service import APIService


class GoogleScholarService(APIService):
    def get_spreadsheet_with_citations(
            self,
            file_path: str,
            column_name: str
    ) -> pd.DataFrame:
        df_spreadsheet = self.__load_spreadsheet(file_path)

        try:
            df_spreadsheet['Citações'] = df_spreadsheet[f'{column_name};'].apply(self.__get_citations)
            return df_spreadsheet

        except KeyError as err:
            print("Houve algum erro ao selecionar a coluna")
            print(repr(err))

        except Exception as err:
            print("Houve outro tipo de erro ao buscar citações a partir de coluna")
            print(repr(err))

    def __load_spreadsheet(self, file_path: str) -> pd.DataFrame:
        if not exists(file_path):
            raise ValueError("Planilha não existe")

        df_spreadsheet = pd.read_excel(file_path)
        df_filtered_spreadsheet = df_spreadsheet.dropna(axis=1)

        return df_filtered_spreadsheet

    def __get_citations(self, researcher_url: str) -> int:
        user_id = self.__get_researcher_id(researcher_url)
        user_json = self.__get_citation_for_user_id(user_id)
        citations = self.__get_latest_year_citation_from_user_json(user_json)
        return citations

    def __get_researcher_id(self, profile_url: str) -> str:
        result = urlparse(profile_url)
        if not result.query:
            raise ValueError('Sem query')

        query = result.query
        pattern = "user=[0-9a-zA-Z]+"
        has_user_id = match(pattern, query)

        if not has_user_id:
            raise ValueError('Sem id do usuário')

        user_id = has_user_id.group().split('=')[1]
        return user_id

    def __get_citation_for_user_id(self, user_id: str) -> dict:
        endpoint = f'http://cse.bth.se/~fer/googlescholar-api/googlescholar.php?user={user_id}'
        page = get(endpoint)

        if not page.ok:
            raise ValueError('Erro ao completar requisição para API')

        try:
            result = loads(page.text)
            return result

        except JSONDecodeError as json_err:
            print(json_err)
            raise ValueError('Erro ao transformar conteúdo de página para dicionário')

        except Exception as err:
            print(err)
            raise ValueError('Erro ao obter dados da API')

    def __get_latest_year_citation_from_user_json(self, user_info: dict) -> int:
        _, citations = [*user_info['citations_per_year'].items()][-1]
        return citations
