import pytest
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'User Management' in response.data

def test_add_user(client):
    """Test adding a user."""
    response = client.post('/add_user', data={'name': 'John Doe'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'John Doe' in response.data

def test_add_empty_user(client):
    """Test that empty user names are handled."""
    response = client.post('/add_user', data={'name': ''}, follow_redirects=True)
    assert response.status_code == 200

def test_multiple_users(client):
    """Test adding multiple users."""
    client.post('/add_user', data={'name': 'Alice'}, follow_redirects=True)
    client.post('/add_user', data={'name': 'Bob'}, follow_redirects=True)
    response = client.get('/')
    assert b'Alice' in response.data
    assert b'Bob' in response.data
