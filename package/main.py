__author__ = 'fla'

from Redis import Redis
from mylist import mylist

#{'serverId': 'serverId', 'cpu': 80, 'mem': 80, 'time': '2014-03-24 16:21:29.384631'}
if __name__ == "__main__":
    p1 = [[1,2,3]]
    p2 = ['[1, 2, 3]']

    print p1
    print p2

    print isinstance(p1[0], list)
    print isinstance(p2[0], list)
    print isinstance(p2[0], str)

    p3 = p2[0].lstrip().replace('[','').replace(']','').split(',')

    p3 = [int(i) for i in p3]

    print p3


    p1 = [[1,2,3], [1,2,3], [1,2,3]]
    p2 = ['[1, 2, 3]', '[4, 5, 6]', '[7, 8, 9]']
    p4 = []

    for i in range(0, len(p2)):
        p3 = p2[i].lstrip().replace('[','').replace(']','').split(',')

        p3 = [int(j) for j in p3]

        p4.append(p3)

    print p4





    '''
    r = Redis()

    r.insert(1)
    r.insert(2)
    r.insert(3)
    r.insert(4)
    r.insert(5)
    r.insert(6)

    lista = r.range()

    print lista

    #print r.media(lista)

    prueba = ['1', '2', '3', '4']

    #message="{serverId: {}, cpu: {}, mem: {}, time: {}}".format("333",0.3,0.4,"hoy")
    message = 'Hello World, tenantId: {}     serverId: {}    json: {}!!!'.format(1, 2, 3)

    print(message)

    message1 = "serverId: {}, cpu: {}, mem: {}, time: {}".format(1, 2, 3, 4)

    print message1

    print "Prueba con listas \n"

    list = [1, 2, 3, 4]

    r.delete()

    r.insert(list)
    r.insert(list)
    r.insert(list)
    r.insert(list)
    r.insert(list)
    r.insert(list)

    list = r.range()

    print list
    print list[0]
    print list[1:]
    '''