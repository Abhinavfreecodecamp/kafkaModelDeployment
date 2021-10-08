from kafka import kafkaConsumer
from json import loads


class kafka_consumer():
    def __init__(self, topics, logger, config):
        self.kafkaTopics = topics
        self.kafkaConfig = topics
        self.logger = logger
        self.consumer = self.createConsumer()

    def createConsumer(self):
        return KafkaConsumer(self.kafkaTopics, **self.kafkaConfig)

    def fetch_records(self, bufferSize):
        # Consuming message batch
        consumedMessage, fetched = [], 0
        for message in self.consumer:
            try:
                consumedMessage.append(loads(message.value.decode('utf-8')))
                fetched +=1
                if fetched > bufferSize:
                    break
            except Exception as e:
                self.logger.warning(f'failed to consume message {e}')

        return consumedMessage