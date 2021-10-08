from jproperties import Properties
from constants import *
import pathlib
import os

path = pathlib.Path(__file__).resolve().parent.parent

def getKafkaConfig():
    kafka_consumer_config = Properties()
    with open(os.path.join(path,kafka_consumer_conf), "rb") as f:
        kafka_consumer_config.load(f, "utf-8")

    kafka_producer_config = Properties()
    with open(os.path.join(path,kafka_producer_conf), "rb") as f:
        kafka_producer_config.load(f, "utf-8")
    
    return {'kafka_consumer_config': kafka_consumer_config,
            'kafka_producer_config': kafka_producer_config}


def getPubSubConfig():
    pub_sub_subscriber_config = Properties()
    with open(os.path.join(path,pub_sub_subscriber_conf), "rb") as f:
        pub_sub_subscriber_config.load(f, "utf-8")

    pub_sub_producer_config = Properties()
    with open(os.path.join(path,pub_sub_producer_conf), "rb") as f:
        pub_sub_producer_config.load(f, "utf-8")
    
    return {'pub_sub_subscriber_config': pub_sub_subscriber_config,
            'pub_sub_producer_config': pub_sub_producer_config}

def getAerospikeConfig():
    aerospike_config = Properties()
    with open(os.path.join(path,aerospike_conf), "rb") as f:
        aerospike_config.load(f, "utf-8")
    return aerospike_config

def getAppConfig():
    app_config = Properties()
    with open(os.path.join(path,app_conf), "rb") as f:
        app_config.load(f, "utf-8")
    return app_config

