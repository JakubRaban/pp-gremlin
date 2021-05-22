from gremlin_python.driver import client, serializer, resultset
from password import password


def print_results(callback):
    for result in callback.results():
        print(result)
    print()


vertex_queries = [
    "g.addV('person').property('id', 'thomas').property('firstName', 'Thomas').property('age', 44).property('pk', 'pk')",
    "g.addV('person').property('id', 'mary').property('firstName', 'Mary').property('lastName', 'Andersen').property('age', 39).property('pk', 'pk')",
    "g.addV('person').property('id', 'ben').property('firstName', 'Ben').property('lastName', 'Miller').property('pk', 'pk')",
    "g.addV('person').property('id', 'robin').property('firstName', 'Robin').property('lastName', 'Wakefield').property('pk', 'pk')",
    "g.addV('device').property('id', 'device1').property('type', 'pc').property('cores', 8).property('pk', 'pk')",
    "g.addV('device').property('id', 'device2').property('type', 'pc').property('cores', 4).property('pk', 'pk')",
    "g.addV('device').property('id', 'device3').property('type', 'smartphone').property('cores', 4).property('pk', 'pk')",
    "g.addV('device').property('id', 'device4').property('type', 'smartphone').property('cores', 4).property('pk', 'pk')",
    "g.addV('device').property('id', 'device5').property('type', 'smartphone').property('cores', 2).property('pk', 'pk')",
    "g.addV('device').property('id', 'device6').property('type', 'tablet').property('cores', 2).property('pk', 'pk')",
    "g.addV('os').property('id', 'win10').property('name', 'windows').property('version', '10').property('pk', 'pk')",
    "g.addV('os').property('id', 'ubuntu20').property('name', 'ubuntu').property('version', '20').property('pk', 'pk')",
    "g.addV('os').property('id', 'android').property('name', 'android').property('pk', 'pk')",
]

edge_queries = [
    "g.V('device1').addE('hasOs').to(g.V('win10'))",
    "g.V('device1').addE('hasOs').to(g.V('ubuntu20'))",
    "g.V('device2').addE('hasOs').to(g.V('win10'))",
    "g.V('device3').addE('hasOs').to(g.V('android'))",
    "g.V('device4').addE('hasOs').to(g.V('android'))",
    "g.V('device5').addE('hasOs').to(g.V('android'))",
    "g.V('device6').addE('hasOs').to(g.V('android'))",
    "g.V('thomas').addE('hasDevice').to(g.V('device1'))",
    "g.V('thomas').addE('hasDevice').to(g.V('device3'))",
    "g.V('mary').addE('hasDevice').to(g.V('device2'))",
    "g.V('ben').addE('hasDevice').to(g.V('device4'))",
    "g.V('robin').addE('hasDevice').to(g.V('device5'))",
    "g.V('robin').addE('hasDevice').to(g.V('device6'))",
    "g.V('mary').addE('knows').to(g.V('thomas'))",
    "g.V('mary').addE('knows').to(g.V('robin'))",
    "g.V('robin').addE('knows').to(g.V('ben'))",
]


def cleanup_db():
    cosmos_client.submit('g.V().drop()')


def setup_db():
    for query in vertex_queries + edge_queries:
        cosmos_client.submit(query)


def find_people_with_more_than_one_device():
    return cosmos_client.submit("g.V().hasLabel('person').where(__.out('hasDevice').count().is(gt(1)))")


def find_devices_with_4_cores_or_less():
    return cosmos_client.submit("g.V().hasLabel('device').has('cores', lte(4))")


def find_people_who_know_someone_with_windows_device():
    return cosmos_client.submit("g.V().hasLabel('person').where(__.out('knows').out('hasDevice').out('hasOs').has('name', 'windows'))")


def update_ubuntu_to_21():
    return cosmos_client.submit("g.V().hasLabel('os').has('name', 'ubuntu').property('version', '21')")


def kill_people_who_know_no_one():
    return cosmos_client.submit("g.V().hasLabel('person').where(__.out('knows').count().is(eq(0))).drop()")


cosmos_client = client.Client('wss://zuz.gremlin.cosmosdb.azure.com:443/', 'g',
                              username="/dbs/graphdb/colls/Persons",
                              password=password,
                              message_serializer=serializer.GraphSONSerializersV2d0()
                              )

cleanup_db()
setup_db()

print('People with more than one device')
print_results(find_people_with_more_than_one_device())
print('Devices with no more than 4 cores')
print_results(find_devices_with_4_cores_or_less())
print('People who know somebody with windows device')
print_results(find_people_who_know_someone_with_windows_device())
update_ubuntu_to_21()
print('Ubuntu updated to v21')
kill_people_who_know_no_one()
print('People with no friends killed')

cosmos_client.close()
