import requests
from flask import Blueprint, abort, jsonify

from producer import publish
from .models import db, Product, ProductUser

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify(Product.query.all())


@api.route('<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        product_user = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'liked this product')

    return jsonify({
        'message': 'success'
    })
