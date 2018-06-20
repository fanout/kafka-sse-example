from django.conf import settings
from django.core.management.base import BaseCommand
from gripcontrol import HttpStreamFormat
from django_grip import publish
from confluent_kafka import Consumer, KafkaException, KafkaError

def sse_encode(data):
	out = 'event: message\n'
	for line in data.split('\n'):
		out += 'data: %s\n' % line
	out += '\n'
	return out

class Command(BaseCommand):
	help = 'Relay events from Kafka to GRIP proxy.'

	def handle(self, *args, **options):
		c = Consumer(settings.KAFKA_CONSUMER_CONFIG)

		c.subscribe(['^.*'])

		self.stdout.write('subscribed')

		try:
			while True:
				msg = c.poll(timeout=1)

				if msg is None:
					continue

				if msg.error():
					if msg.error().code() == KafkaError._PARTITION_EOF:
						continue
					else:
						raise KafkaException(msg.error())

				# skip internal channels
				if msg.topic().startswith('__'):
					continue

				try:
					data = msg.value().decode('utf-8')
				except Exception:
					self.stdout.write('%s: message is not valid utf-8: %s' %
						(msg.topic(), repr(msg.value())))
					continue

				publish(msg.topic(), HttpStreamFormat(sse_encode(data)))

		except KeyboardInterrupt:
			pass

		c.close()
