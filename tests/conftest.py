import pytest

from src.app import create_app

@pytest.fixture(scope="module")
def test_app():
    application = create_app()

    application.config["TESTING"] = True
    application.config["DEBUG"] = True

    client = application.test_client()

    context = application.test_request_context()
    context.push()

    yield client

    context.pop()

    # with application.test_client() as testing_client:
    #     with application.app_context():
    #         yield testing_client