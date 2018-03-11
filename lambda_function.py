import datetime
import json
import logging
import time
import boto3
import elastic


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

destination="https://search-amp-sight-24afp44dljnq5vgrp7grcdl5ei.us-east-1.es.amazonaws.com"
DOWNLOADED_SNAPSHOT_FILE_NAME = "/tmp/configsnapshot" + str(time.time()) + ".json.gz"


def lambda_handler(event, context):
    # TODO implement
    
    iso_now_time = datetime.datetime.now().isoformat()
    logger.info("lambda_function: Snapshot Time: " + str(iso_now_time))

    #event_str = unicode(json.dumps(event)).encode("utf-8")
    #logger.info("lambda_function: event_str: " + event_str)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    #logger.info("lambda_function: bucket: " + bucket)
    
    snapshot_file_path = event['Records'][0]['s3']['object']['key']
    logger.info("lambda_function: snapshot_file_path: " + snapshot_file_path)
    
    s3conn = boto3.resource('s3')
    s3conn.meta.client.download_file(bucket, snapshot_file_path, DOWNLOADED_SNAPSHOT_FILE_NAME)
    
    es=elastic.ElasticSearch(connections=destination, log=None)
    es.set_not_analyzed_template()
    
    data = None
    if "_ConfigSnapshot_" in snapshot_file_path:
        logger.info("lambda_function: ConfigSnapshot: " + snapshot_file_path)
        
        with open(DOWNLOADED_SNAPSHOT_FILE_NAME) as dataFile:
            try:
                data = json.load(dataFile)
                load_data_into_es(data, iso_now_time, es)
            except Exception as e:
                logger.info("lambda_function: json.load failed: " + e.message)

    else:
        logger.info("lambda_function: ConfigSnapshot: not a Config Snapshot file!")
    
    return
        
def load_data_into_es(data, iso_now_time, es):
    
    if data is not None:
        configuration_items = data.get("configurationItems", [])

        if len(configuration_items) > 0:
            for item in configuration_items:
                try:
                    #logger.info("lambda_function: storing in ES: " + str(item.get("resourceType")))
                    
                    indexname = item.get("resourceType").lower()
                    typename = item.get("awsRegion").lower()
                    item['snapshotTimeIso'] = iso_now_time
                    
                    item_str = unicode(json.dumps(item)).encode("utf-8")
                    #logger.info("lambda_function: item_str: " + item_str)
                    
                    response = es.add(index_name=indexname, doc_type=typename, json_message=item_str)
                    #logger.info("lambda_function: load_data_into_es: " + response)
                            
                except Exception as e:
                    logger.info("lambda_function: Couldn't add item: " + item_str + " because " + e.message)

    return


