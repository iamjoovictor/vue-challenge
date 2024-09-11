import pytest
from src.middleware.utils_environment import get_environment_config
from src.tests.utils.create_items import create_product
from src.tests.utils.https_methods import http_delete

config = get_environment_config()
BACKEND_URL = config.get('BACKEND_URL') + 'product/'

@pytest.mark.asyncio
async def test_delete_product_success(test_app, session, test_app_authentication):
    product1 = await create_product(session)
    
    response = await http_delete(test_app, test_app_authentication, f'{BACKEND_URL}?id_product={product1.id}')
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, type(None))
    assert response_data == None
    
@pytest.mark.asyncio
async def test_delete_product_not_found(test_app, session, test_app_authentication):
    response = await http_delete(test_app, test_app_authentication, f'{BACKEND_URL}?id_product=1')
    assert response.status_code == 404
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data['detail'] == 'Product not found'
    