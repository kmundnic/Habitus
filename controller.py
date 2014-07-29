from data_retriever import DataRetriever
from data_handler import DataHandler

# TODO: Erase files that have been sent
# If the files that have been sent are erased, it is quite easy to keep track
# of the information that has not been sent, and this can be saved into a list
# that can be easily put into a file and therefore, read to create a queue.
#
# TODO: Keep log with logger

RETRIEVE_DATA_INTERVAL = 1
SEND_DATA_INTERVAL = 15

retriever = DataRetriever(RETRIEVE_DATA_INTERVAL)
handler = DataHandler(retriever)