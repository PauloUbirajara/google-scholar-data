from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from src.exception.exceptions import FetchException
from src.helper.logging_helper import error, warn
from src.model.scholar_info import ScholarInfo

VALUE_IF_NOT_FOUND = 0


def open_researcher_profile(driver: Firefox, researcher_id: str):
    # Abrir link na página do pesquisador
    researcher_url_template = "https://scholar.google.com.br/citations?user={}"
    researcher_url = researcher_url_template.format(researcher_id)

    driver.get(researcher_url)
    assert driver.find_element(By.ID, "gsc_prf_pup-img") is not None

    info = ScholarInfo(researcher_id)
    h_index_str = driver.find_element(
        By.XPATH,
        "/html/body/div/div[12]/div[2]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]"
    ).get_attribute('innerText')
    info.set_h_index(int(h_index_str))

    i10_index_str = driver.find_element(
        By.XPATH,
        "/html/body/div/div[12]/div[2]/div/div[1]/div[1]/table/tbody/tr[3]/td[2]"
    ).get_attribute("innerText")
    info.set_i10_index(int(i10_index_str))

    citations_elements = driver.find_element(
        By.XPATH,
        "/html/body/div/div[12]/div[2]/div/div[1]/div/div/div[3]/div"
    )

    citations_years = [
        html_element.get_attribute('textContent')
        for html_element in citations_elements.find_elements(By.CLASS_NAME, "gsc_g_t")
    ]

    citations_values = [0] * len(citations_years)

    for html_element in citations_elements.find_elements(By.TAG_NAME, "a"):
        current_zindex = html_element.value_of_css_property('z-index')
        if current_zindex == 'auto':
            continue

        citation_index = len(citations_years) - int(current_zindex)
        citations_values[citation_index] = int(html_element.get_attribute('textContent'))

    warn(f'id: {info.id}')
    warn(f'citation_years: {citations_years}')
    warn(f'citation_values: {citations_values}')

    citations_dict = dict(zip(citations_years, citations_values))
    info.set_citations_dict(citations_dict)

    return info


def new_options_for_firefox_driver():
    options = Options()
    options.headless = True
    return options


class SeleniumService:
    @staticmethod
    def fetch_info(researcher_id: str) -> ScholarInfo:

        driver = Firefox(options=new_options_for_firefox_driver())

        info = None

        try:
            info = open_researcher_profile(driver, researcher_id)
            INTERVAL_BETWEEN_QUERIES = 25
            sleep(INTERVAL_BETWEEN_QUERIES)

        except WebDriverException:
            error("Erro ao obter dados de pesquisador - Selenium")

        except Exception as e:
            error("Erro ao obter dados de pesquisador")
            error(repr(e))

        driver.close()

        if info is None:
            raise FetchException("Erro ao buscar dados de pesquisador - Selenium")

        return info
