from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer, KeyedProducer
import logging

logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.DEBUG
        )


kafka = KafkaClient("localhost:9092")
kafka.send_offset_fetch_request('test-group')

# To consume messages
consumer = SimpleConsumer(kafka, "test-group", "test-topic", auto_commit_every_n=1, iter_timeout=10)

# while True:
#     for message in consumer:
#         print(message)
#         consumer.commit()

print consumer.get_message()
# consumer.commit(partitions=[0])

kafka.close()