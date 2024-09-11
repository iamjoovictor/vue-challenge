import pytest
from src.middleware.utils_environment import get_environment_config
from src.tests.utils.https_methods import http_get

config = get_environment_config()
BACKEND_URL = config.get('BACKEND_URL') + 'category/'

@pytest.mark.asyncio
async def test_get_all_categories_sucess(test_app, session, test_app_authentication):
    response = await http_get(test_app, test_app_authentication, BACKEND_URL)
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, list)
    assert response_data == []

@pytest.mark.asyncio
async def test_get_all_categories_route_not_fount(test_app, session, test_app_authentication):
    response = await http_get(test_app, test_app_authentication, f'{BACKEND_URL}/route_not_found')
    assert response.status_code == 404
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Not Found'

    