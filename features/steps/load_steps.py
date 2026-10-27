import requests
from behave import given
from compare import expect

@given('the following products')
def step_impl(context):
    rest_url = context.BASE_URL + "/products"
    
    resp = requests.get(rest_url)
    expect(resp.status_code).to_equal(200)
    for product in resp.json():
        delete_resp = requests.delete(f"{rest_url}/{product['id']}")
        expect(delete_resp.status_code).to_equal(204)

    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": float(row['price']),
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        resp = requests.post(rest_url, json=payload)
        expect(resp.status_code).to_equal(201)
