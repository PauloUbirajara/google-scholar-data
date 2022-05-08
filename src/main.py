from adapter.tkinter_adapter import GTKAdapter
from service.google_scholar_service import GoogleScholarService


if __name__ == '__main__':
    GTKAdapter().set_service(GoogleScholarService()).render()
