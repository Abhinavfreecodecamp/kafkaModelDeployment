from pubSubModule.subcriber import subscriber_module
from pubSubModule.publisher import publisher_module
from kafkaModule.consumer import kafka_consumer
from kafkaModule.producer import kafka_producer
from NNModule.modelHelper import model_helper
from config.loggingConfig import get_logger
from config.runTimeConf import *
from json import loads, dumps
from datetime import datetime
import numpy as np
import aerospike



### get aerospike connection
def create_aerospike_connection(host, port, namespace=None):
    try:
        hosts = host.split(',')
        aerospike_config_dict = {'hosts':list(tuple([host,int(port)]) for host in hosts)}
        aerospike_client = aerospike.client(aerospike_config_dict).connect()
        return aerospike_client
    except:
        return None


### producer func and aerospike upload

def pushRecords(aerospikeClient, requestId, labelnames, namespace, logger):
    logger.info(f'pushing records to kafka producer & nosql backup db....')
    try:
        for reqId, clsLabel in zip(requestId, labelnames):
            key = (namespace, 'test-table-name', str(reqId))
            if aerospikeClient is not None or aerospikeClient.closed() is not True:
                aerospikeClient.put(key, clsLabel)
            logger.info(f'successfully pushed records....')
            return True
    except Exception as e:
        logger.error(f'failed to push records {e}')
        return False


#### start main program

if __name__ == "__main__":
    logger = get_logger(logger_name=__name__)
    logger.info('application started....')
    logger.info('getting configs....')
    
    appConfig = getAppConfig()
    aerospikeConfig = getAerospikeConfig()
    kafkaConfig = getKafkaConfig()
    pubSubConfig = getPubSubConfig()

    consumerConfig = kafkaConfig['kafka_consumer_config']
    producerConfig = kafkaConfig['kafka_producer_config']
    pubSubScriberConfig = pubSubConfig['pub_sub_subscriber_config']
    pubSubPublisherConfig = pubSubConfig['pub_sub_publisher_config']

    logger.info('creating kafka clients....')
    kafkaConsumer = kafka_consumer(topics='test-topics',config=consumerConfig, logger=logger)
    kafkaProducer = kafka_producer(producerConfig,logger=logger)

    logger.info('creating google pub/sub cients')
    publisherModule = publisher_module(logger=logger, config=pubSubPublisherConfig)
    subscriberModule = subscriber_module(logger=logger, config=pubSubScriberConfig)

    logger.info('creating model helper class')
    modelHelperModule = model_helper(logger=logger)

    logger.info('creating aerospike client')
    aerospikeClient = create_aerospike_connection(**aerospikeConfig)

    usePubSub = appConfig['usePubSub']
    bufferSize = appConfig['client.buffer.size']
    logger.info(f'using pubsub {usePubSub}')
    while True:

        if usePubSub:
            ### fetch from pubsub and push to pubsub
            consumedMessage = subscriberModule.fetch_records()
            requestId, classLabels = modelHelperModule.getInference(consumedMessage=consumedMessage)
            pushFlag = publisherModule.push_records(requestId=requestId, labelnames=classLabels)
        
        else:
            ### fetch from kafka and push to kafka
            consumedMessage = kafkaConsumer.fetch_records()
            #### getting model prediction 
            requestId, classLabels = modelHelperModule.getInference(consumedMessage=consumedMessage)
            ##### pushing records 
            pushFlag = kafkaProducer.push_records(requestId=requestId, labelnames=classLabels)

        
        pushFlagAerospike = pushRecords(aerospikeClient, requestId, labelnames, namespace, logger)     
        logger.info(f'push flag status {pushFlag}, aerospike push status {pushFlagAerospike}')








    