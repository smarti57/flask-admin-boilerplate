from pymongo import MongoClient
import configuration

connection_params = configuration.connection_params

#connect to mongodb
mongoconnection = MongoClient(
    'mongodb+srv://{user}:{password}@{host}:{port}'
    '/{namespace}?retryWrites=true&w=majority'.format(**connection_params)
)

#ORIGINAL STUFF
    #'mongodb+srv://{user}:{password}@{host}:'
    #'{port}/{namespace}?retryWrites=false'.format(**connection_params)
#pymongo.MongoClient("mongodb+srv://flaskdb_user:<password>@cluster0.xrgdk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
