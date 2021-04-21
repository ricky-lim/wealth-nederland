import pytest
import voila.app
from pyprojroot import here


class VoilaTest(voila.app.Voila):
    def listen(self):
        pass


@pytest.fixture
def nb_app():
    nb = here() / "notebooks" / "wealth_of_nederland.ipynb"
    voila_args = [str(nb), "--no-browser"]
    voila_app = VoilaTest.instance()
    voila_app.initialize(voila_args)
    voila_app.start()
    yield voila_app
    voila_app.stop()
    voila_app.clear_instance()


@pytest.fixture
def app(nb_app):
    return nb_app.app


@pytest.mark.gen_test
def test_app(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200
