

import requests


_requests_session = None


def requests_session(session=None):
    """
    Set/get the requests library session used by all API functions.
    :param session: Optional requests Session object to replace the default one
    :return: requests.session()
    """

    global _requests_session

    # change to given session object
    if session is not None:
        _requests_session = session

    # create session if not exist already
    if _requests_session is None:
        _requests_session = requests.Session()

    return _requests_session
