from .database import Session


class AlchemySessionMiddleware(object):

    def process_request(self, request):
        request.db_session = Session()

    def process_response(self, request, response):
        try:
            request.db_session.commit()
            request.db_session.close()
        except AttributeError:
            pass
        return response

    def process_exception(self, request, exception):
        try:
            request.db_session.rollback()
            request.db_session.close()
        except AttributeError:
            pass