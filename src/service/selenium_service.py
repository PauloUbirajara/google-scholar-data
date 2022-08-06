from src.model.scholar_info import ScholarInfo

VALUE_IF_NOT_FOUND = 0


class SeleniumService:
    @staticmethod
    def fetch_info(researcher_id: str) -> ScholarInfo:
        info = ScholarInfo()

        return info
