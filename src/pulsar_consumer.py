import io
import time
import traceback

import pulsar
from pulsar.schema import *
from avro.io import DatumReader, BinaryDecoder, DatumWriter, BinaryEncoder
from avro.schema import parse
from chat_message_processor import update_transcription_using_whisper
from pulsar.schema import BytesSchema, JsonSchema
from env_variables import PULSAR_URL
import os

# Get the current working directory
current_directory = os.getcwd()

print("Current Directory:", current_directory)

topic = 'persistent://babblebox/messages/new_audio_message'
send_message_topic = 'persistent://babblebox/audio_processing/new_transcription'

print(PULSAR_URL)
client = pulsar.Client(PULSAR_URL)
print("Pulsar Python client version:", pulsar.__version__)


class ChatMessage(Record):
    id = String()
    chat_id = String()
    audio_message_id = String()
    image_id = String()
    timestamp = String()


consumer = client.subscribe(topic, subscription_name='my-sub')
producer = client.create_producer(send_message_topic, schema=JsonSchema(ChatMessage))

# Define your Avro schema
schema_path = current_directory + '/src/audiofile_schema.avsc'
with open(schema_path, 'r') as file:
    schema = parse(file.read())

print(schema)


def deserialize_from_avro(data, avro_schema):
    bytes_reader = io.BytesIO(data)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(avro_schema)
    return reader.read(decoder)


def serialize_to_avro(data, avro_schema):
    writer = DatumWriter(avro_schema)
    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder)
    return bytes_writer.getvalue()


def send_pulsar_message(serialized_data):
    producer.send(serialized_data)
    print("Message sent to pulsar successfully")

while True:
    msg = consumer.receive()
    try:
        print("Received message: '%s'" % msg.data())
        deserialize_msg = deserialize_from_avro(msg.data(), schema)
        print(deserialize_msg)
        update_transcription_using_whisper(deserialize_msg["audio_message_id"])
        data = ChatMessage(
            id=deserialize_msg["id"],
            chat_id=deserialize_msg["chat_id"],
            audio_message_id=deserialize_msg["audio_message_id"],
            image_id=deserialize_msg["image_id"],
            timestamp=deserialize_msg["timestamp"]
        )
        send_pulsar_message(data)
        consumer.acknowledge(msg)
    except Exception as e:
        print("Error message:", e)
        traceback.print_exc()

client.close()
