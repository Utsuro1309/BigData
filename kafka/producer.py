import time
import json
import random
from datetime import datetime
from data_generator import generate_order
from kafka import KafkaProducer


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:19092', 'localhost:29092', 'localhost:39092'],
    value_serializer=serializer,
    api_version=(2, 0, 2)
)

if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    while True:
        # Generate a message
        dummy_message = generate_order()

        # Send it to our 'messages' topic0
        print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
        producer.send('Order', dummy_message)
        producer.flush()

        # Sleep for a random number of seconds
        time_to_sleep = random.randint(1, 3)
        time.sleep(time_to_sleep)