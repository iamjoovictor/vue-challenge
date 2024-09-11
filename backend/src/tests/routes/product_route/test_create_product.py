import pytest
from src.middleware.utils_environment import get_environment_config
from src.tests.utils.https_methods import http_post
from src.tests.utils.create_items import create_category, create_product

config = get_environment_config()
BACKEND_URL = config.get('BACKEND_URL') + 'product/'

@pytest.mark.asyncio
async def test_create_product_sucess(test_app, session, test_app_authentication):
    await create_category(session)
    
    body = {
        "name": "Product 1",
        "price": 0,
        "expiration_date": '2024-09-11',
        "image": None,
        "id_category": 1
    }
    
    response = await http_post(test_app, test_app_authentication, BACKEND_URL, body)
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    
@pytest.mark.asyncio
async def test_create_category_already_exists_product_with_same_name(test_app, session, test_app_authentication):
    await create_product(session)
    
    body = {
        "name": "test_product",
        "price": 0,
        "expiration_date": '2024-09-11',
        "image": None,
        "id_category": 1
    }
    
    response = await http_post(test_app, test_app_authentication, BACKEND_URL, body)
    assert response.status_code == 409
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Already exists product with name test_product'

    