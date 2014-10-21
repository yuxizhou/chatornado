from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import time

kafka = KafkaClient("localhost:9092")

# To send messages asynchronously
producer = SimpleProducer(kafka, async=True)

while True:
    producer.send_messages('test-topic', "test")
    producer.send_messages('test-topic', "\xc2Hola, mundo!")

    time.sleep(1)





