from flask import jsonify, request, url_for, abort, make_response
from service.models import Product, Category
from service.common import status
from service import app

@app.route("/")
def index():
    """Base URL for the application"""
    return app.send_static_file("index.html")

def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(status.HTTP_400_BAD_REQUEST, f"Content-Type must be {content_type}")
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(status.HTTP_400_BAD_REQUEST, f"Content-Type must be {content_type}")

@app.route("/products", methods=["POST"])
def create_products():
    """Create a Product"""
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    return make_response(
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": url_for("get_products", product_id=product.id, _external=True)},
    )

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Retrieve a single Product"""
    app.logger.info("Request to retrieve product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return product.serialize(), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Update a Product"""
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Delete a Product"""
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

@app.route("/products", methods=["GET"])
def list_products():
    """List all Products or query by parameters"""
    app.logger.info("Request to list products...")
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Find by category: %s", category)
        category_value = getattr(Category, category.upper(), None)
        products = Product.find_by_category(category_value)
    elif available:
        app.logger.info("Find by available: %s", available)
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        app.logger.info("Find all")
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK
