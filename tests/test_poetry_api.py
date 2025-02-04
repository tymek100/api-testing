import pytest
from api_client.poetry_api_client import PoetryApiClient
from api_client.input_classes import Author, Title, LineCount, Random, PoemCount
from api_client.output_enum import Output

@pytest.fixture
def client():
    return PoetryApiClient()

def test_title(client):
    response = client.call_api(
        inputs = [Title("Ozymandias")],
        outputs = [Output.AUTHOR, Output.TITLE, Output.LINECOUNT])
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    expected = {
        "title": "Ozymandias",
        "author": "Percy Bysshe Shelley",
        "linecount": "14"
    }

    json = response.json()
    assert json[0] == expected
    assert len(json) == 1


def test_negative_abs_author(client):
    response = client.call_api(
        inputs = [Author("Shakespeare", absolute=True)],
        outputs = [Output.AUTHOR])
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    assert response.json()["status"] == 404
    assert response.json()["reason"] == "Not found"


def test_poemcount_with_linecount(client):
    response = client.call_api(
        inputs = [Title("Winter"), Author("William Shakespeare"), LineCount("14"), PoemCount("1")])
    
    expected = {
        "title": "Sonnet 2: When forty winters shall besiege thy brow",
        "author": "William Shakespeare",
        "lines": [
        "When forty winters shall besiege thy brow,",
        "And dig deep trenches in thy beauty's field,",
        "Thy youth's proud livery so gazed on now,",
        "Will be a tatter'd weed of small worth held:",
        "Then being asked, where all thy beauty lies,",
        "Where all the treasure of thy lusty days;",
        "To say, within thine own deep sunken eyes,",
        "Were an all-eating shame, and thriftless praise.",
        "How much more praise deserv'd thy beauty's use,",
        "If thou couldst answer 'This fair child of mine",
        "Shall sum my count, and make my old excuse,'",
        "Proving his beauty by succession thine!",
        "  This were to be new made when thou art old,",
        "  And see thy blood warm when thou feel'st it cold."
        ],
        "linecount": "14"
    }
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    json = response.json()
    assert json[0] == expected
    assert len(json) == 1


def test_negative_poemcount_with_random(client):
    response = client.call_api(
        inputs = [Title("Winter"), Author("William Shakespeare"), PoemCount("2"), Random("2")])
    
    assert response.json()["status"] == "405"
    assert response.json()["reason"] == "Use either poemcount or random as input fields, but not both."
    



