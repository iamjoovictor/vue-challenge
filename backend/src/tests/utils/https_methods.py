async def http_get(test_app, test_app_authentication, url):
    login_response_data = test_app_authentication.json()
    headers = { 'Authorization': f"Bearer {login_response_data['access_token']}" }
    
    return await test_app.get(url, headers=headers)

async def http_post(test_app, test_app_authentication, url, body = {}, is_url_encoded = False):
    content_type = 'application/x-www-form-urlencoded' if is_url_encoded else 'application/json'
    
    login_response_data = test_app_authentication.json()
    headers = {
        'Authorization': f"Bearer {login_response_data['access_token']}",
        'Content-Type': content_type
    }
    
    return await test_app.post(url, headers=headers, json=body)

async def http_put(test_app, test_app_authentication, url, body):
    login_response_data = test_app_authentication.json()
    headers = { 'Authorization': f"Bearer {login_response_data['access_token']}" }
    
    return await test_app.put(url, headers=headers, json=body)

async def http_delete(test_app, test_app_authentication, url):
    login_response_data = test_app_authentication.json()
    headers = { 'Authorization': f"Bearer {login_response_data['access_token']}" }
    
    return await test_app.delete(url, headers=headers)
