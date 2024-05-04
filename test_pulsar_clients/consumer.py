import pulsar

topic = 'persistent://babblebox/audio_processing/test'

client = pulsar.Client('pulsar://ace1576244a014b69bf12b37caa0adc0-448406877.us-east-1.elb.amazonaws.com:6650')
print("Pulsar Python client version:", pulsar.__version__)

consumer = client.subscribe(topic, subscription_name='my-sub')

while True:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)

client.close()