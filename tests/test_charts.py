import pytest
import tempfile
import os
from io import BytesIO
from hchart.app import create_app

@pytest.fixture
def app():
    app = create_app(config_object="tests.settings")
    yield app
    

@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    """Verify we can reach the app"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Use this form to display a chart and a graph." in response.data
    

def test_submit_form_no_input(client):
    """User clicks the 'Submit' button without entering or uploading data"""
    response = client.post("/")
    assert b'Please either manually input data OR upload a file.' in response.data

    
def test_upload_non_csv(client):
    """User uploads a file that is not type csv"""
    data = { 'file': (BytesIO(b"abcdef"), 'test.jpg') }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b"csv files only!" in response.data

    
@pytest.mark.skip(reason="disabled redirect for this small application; form resubmission is okay because no persistent data is modified")
def test_form_submission_redirects(client):
    """Form submission should redirect back to main page to prevent multiple form submissions"""
    data = { 'file': (BytesIO(b""), 'test.csv') }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=False)
    assert response.status_code == 302


def test_upload_empty_file(client):
    """User uploads an empty csv file"""
    data = { 'file': (BytesIO(b""), 'test.csv') }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b"unable to read your file" in response.data
    
        
def test_upload_csv(client):
    """User uploads a valid csv file"""
    csv_data = """
a,b,c
1,3,10
3,20,12
-1,-5,-4
    """
    
    data = { 'file': (BytesIO(csv_data.encode('utf-8')), 'test.csv') }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b"Plotly.newPlot" in response.data


    
def test_valid_manual_input(client):
    """User manually enters data into the input field"""
    csv_data = """
a,b,c
1,3,10
3,20,12
-1,-5,-4
    """
    
    data = { 'data': csv_data }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b"Plotly.newPlot" in response.data


def test_manual_input_and_file_input(client):
    """If user enters data in the textarea field and uploads a file, the file upload takes precedence"""
    """User manually enters data into the input field"""
    csv_data = """
a,b,c
1,3,10
3,20,12
-1,-5,-4
    """
    
    data = { 'data': csv_data, 'file': (BytesIO(csv_data.encode('utf-8')), 'test.csv')  }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b"Displaying data from" in response.data


def test_invalid_manual_data(client):
    """User manually enters data into the input field"""    
    data = { 'data': "Not valid csv" }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b"There was a problem processing the input you entered." in response.data


@pytest.mark.skip(reason="Disabling as it is currently unclear how this app should handle non-numerical values; User should visually check that their data is correct;")
def test_invalid_file_data_extra_col(client):
    """User uploads improperly formatted file"""
    csv_data = """
a,b,c,d
1,3,10,2
3,20,12
-1,-5,-4
    """
    
    data = { 'file': (BytesIO(csv_data.encode('utf-8')), 'test.csv') }
    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b"unable to read your file" in response.data


@pytest.mark.skip(reason="This constraint works via the webapp, but this test has not yet implemented")
def test_error_page(client):
    pass


@pytest.mark.skip(reason="This constraint works via the webapp, but this test has not yet implemented")
def test_upload_large_file(client):
    """TODO - test that large files get rejected"""