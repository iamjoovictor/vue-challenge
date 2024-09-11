import pytest
from src.middleware.utils_environment import get_environment_config
from src.tests.utils.https_methods import http_post, http_put
from src.tests.utils.create_items import create_category

config = get_environment_config()
BACKEND_URL = config.get('BACKEND_URL') + 'category/'

@pytest.mark.asyncio
async def test_update_category_sucess(test_app, session, test_app_authentication):
    await create_category(session)
    
    body = {
        "id": 1,
        "name": "Category 1 Update",
    }
    
    response = await http_put(test_app, test_app_authentication, BACKEND_URL, body)
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, type(None))
    
@pytest.mark.asyncio
async def test_update_category_not_fount(test_app, session, test_app_authentication):
    body = {
        "id": 1,
        "name": "Category Update",
    }
    
    response = await http_put(test_app, test_app_authentication, BACKEND_URL, body)
    assert response.status_code == 404
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Category not found'
    
@pytest.mark.asyncio
async def test_update_category_already_exists_category_with_same_name(test_app, session, test_app_authentication):
    await create_category(session)
    
    # Create new category
    body_create = {
        "name": "Category 1",
    }
    
    response = await http_post(test_app, test_app_authentication, BACKEND_URL, body_create)
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    
    # Update Category
    body_update = {
        "id": 2,
        "name": "test_category",
    }
    
    response = await http_put(test_app, test_app_authentication, BACKEND_URL, body_update)
    assert response.status_code == 409
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Already exists category with name test_category'