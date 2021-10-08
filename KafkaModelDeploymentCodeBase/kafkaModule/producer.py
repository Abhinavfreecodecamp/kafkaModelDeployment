from kafka import kafkaProducer

class kafka_producer():
    def __init__(self, config, logger):
        self.kafkaConfig = config
        self.logger = logger
        self.producer  = self.createProducer()

    def create_producer(self):
        return kafkaProducer(**config)

    def push_records(self, requestId, labelnames):
        if len(requestId) == 0:
            return False
        try:
            for reqId, clsLabel in zip(requestId, labelnames):
                producer.send('test-topic-send', {reqId:clsLabel})
            logger.info(f'successfully pushed records....')
            return True
        except Exception as e:
            logger.error(f'failed to push records {e}')
            return False
