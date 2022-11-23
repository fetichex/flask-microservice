import pika
import json

from main import create_app
from main.models import Product, db

app = create_app()

params = pika.URLParameters(
    'amqps://zbrsberv:vYxG0wUrodhtbQTdoYyH62KX-vG3O4qz@jackal.rmq.cloudamqp.com/zbrsberv')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    data = json.loads(body)

    if properties.content_type == 'product_created':
        with app.app_context():
            product = Product(
                id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
        print('product created')

    elif properties.content_type == 'product_updated':
        with app.app_context():
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
        print('product updated')

    elif properties.content_type == 'product_deleted':
        with app.app_context():
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
        print('product deleted')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('CONSUMING')

channel.start_consuming()

channel.close()
