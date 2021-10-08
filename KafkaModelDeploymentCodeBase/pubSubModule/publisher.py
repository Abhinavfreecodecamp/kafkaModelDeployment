from logging import Logger
from google.cloud import pubsub_v1
from json import dumps


class publisher_module():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.publisher, self.topic_path = self.create_publisher()

    def create_publisher(self):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(**self.config)
        return publisher, topic_path
    
    def push_records(self, requestId, labelnames):
        if len(requestId) == 0:
            return False
        try:
            for reqId, clsLabel in zip(requestId, labelnames):
                data = dumps({reqId:clsLabel})
                message_publish_status = self.publisher.publish(self.topic_path, data)
                self.logger.info(f'pushed record {message_publish_status}')
            self.logger.info('successfully pushed records....')
            return True
        except Exception as e:
            self.logger.error(f'failed to push records {e}')
            return False
