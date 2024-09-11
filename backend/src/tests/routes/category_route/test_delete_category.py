import pytest
from src.middleware.utils_environment import get_environment_config
from src.tests.utils.create_items import create_category, create_product
from src.tests.utils.https_methods import http_delete

config = get_environment_config()
BACKEND_URL = config.get('BACKEND_URL') + 'category/'

@pytest.mark.asyncio
async def test_delete_category_success(test_app, session, test_app_authentication):
    category1 = await create_category(session)
    
    response = await http_delete(test_app, test_app_authentication, f'{BACKEND_URL}?id_category={category1.id}')
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, type(None))
    assert response_data == None
    
@pytest.mark.asyncio
async def test_delete_category_not_found(test_app, session, test_app_authentication):
    response = await http_delete(test_app, test_app_authentication, f'{BACKEND_URL}?id_category=1')
    assert response.status_code == 404
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Category not found'
    
@pytest.mark.asyncio
async def test_delete_category_error_product_associated(test_app, session, test_app_authentication):
    product = await create_product(session)
    
    response = await http_delete(test_app, test_app_authentication, f'{BACKEND_URL}?id_category={product.id_category}')
    assert response.status_code == 409
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Category cannot be removed as there is a product associated with it.'
    