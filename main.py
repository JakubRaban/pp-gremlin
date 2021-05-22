from gremlin_python.driver import client, serializer
from password import password

client = client.Client('wss://zuz.gremlin.cosmosdb.azure.com:443/', 'g',
                       username="/dbs/graphdb/colls/Persons",
                       password=password,
                       message_serializer=serializer.GraphSONSerializersV2d0()
                       )
callback = client.submit("g.addV('person').property('id', 'thomas.1').property('firstName', 'Thomas').property('lastName', 'Andersen').property('age', 44)")
print(callback)
client.close()
