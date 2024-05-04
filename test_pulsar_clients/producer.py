import pulsar

topic = 'persistent://babblebox/audio_processing/test'

client = pulsar.Client('pulsar://ace1576244a014b69bf12b37caa0adc0-448406877.us-east-1.elb.amazonaws.com:6650')
producer = client.create_producer(topic)

for i in range(1000):
    producer.send(('hello-pulsar-%d' % i).encode('utf-8'))
    print('Sent message: hello-pulsar-%d' % i)
client.close()