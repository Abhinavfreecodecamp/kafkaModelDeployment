from logging import Logger
from google.cloud import pubsub

class subscriber_module():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.subscriber = self.create_subscriber()

    def fetch_records(self):
        publisher = pubsub.PublisherClient()

        topic_path = publisher.topic_path(self.config['project'], self.config['topic'])

        with pubsub.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(self.config['project'], self.config['subscription'])
            response = subscriber.pull(
                request={
                    "subscription": self.config['subscription_path'],
                    "max_messages": self.config['max_messages'],
                }
            )
            consumedMessage, fetched = [], 0
            for msg in response.received_messages:
                consumedMessage.append(msg.message.data)
        return consumedMessage