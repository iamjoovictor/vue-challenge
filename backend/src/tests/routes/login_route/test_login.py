import pytest
from src.middleware.utils_environment import get_environment_config

config = get_environment_config()
BACKEND_URL = config.get('BACKEND_URL') + 'login/'


@pytest.mark.asyncio
async def test_login_success(test_app, session):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = "username=admin&password=admin"
        
    response = await test_app.post(BACKEND_URL, content = body, headers = headers)
    
    response_data = response.json()
    
    assert response.status_code == 200
    assert isinstance(response_data, dict)
    assert response_data['token_type'] == "bearer"
    
@pytest.mark.asyncio
async def test_login_invalid_credentials(test_app, session):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = "username=admin&password=wrong_password"
        
    response = await test_app.post(BACKEND_URL, content = body, headers = headers)
    response_data = response.json()
    
    assert response.status_code == 401
    assert isinstance(response_data, dict)
    assert response_data['detail'] == "Invalid credentials"