import pandas as pd
from time import time
from pyelasticsearch import ElasticSearch

CHUNKSIZE = 100


def index_data(data_path, chunksize, index_name, doc_type):
    f = open(data_path)
    csvfile = pd.read_csv(f, iterator=True, chunksize=chunksize)
    es = ElasticSearch(urls='http://localhost', port=9200)
    try:
        es.delete_index(index_name)
    except:
        pass
    es.create_index(index_name)
    for i, df in enumerate(csvfile):
        records = df.where(pd.notnull(df), None).T.to_dict()
        records_list = [records[i] for i in records]
        try:
            es.bulk_index(index_name, doc_type, records_list)
        except:
            print("Error! Skipping chunk...!")
            pass


# read and insert data into elastic
train_data_path = "c:\\data\\train_loan.csv"
test_data_path = "c:\\data\\test_loan.csv"
train = pd.read_csv(train_data_path)
test = pd.read_csv(test_data_path)
# train.shape
# train.head(5)

# insert data into elastic search
index_name_train = "loan_prediction_train"
doc_type_train = "av-lp_train"
index_name_test = "loan_prediction_test"
doc_type_test = "av-lp_test"

# indexing train data
index_data(train_data_path, CHUNKSIZE, index_name_train, doc_type_train)
# indexing test data
index_data(test_data_path, CHUNKSIZE, index_name_test, doc_type_test)