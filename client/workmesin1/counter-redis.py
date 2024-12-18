import redis
import time
import random
import socket

first_available_server_list=[
    'eas-ds2024-redis-joiner-1',
    'eas-ds2024-redis-1',
    'eas-ds2024-redis-2',
    'eas-ds2024-redis-3',
    'eas-ds2024-redis-4',
    'eas-ds2024-redis-5',
]

while True:
    try:
        host = first_available_server_list[random.randint(0, len(first_available_server_list) - 1)]
        print(f'Trying first host {host}...')
        cluster = redis.RedisCluster(
            host=host,
            port= 6379,
            decode_responses=True
        )
        nodes = [node.host for node in cluster.get_nodes()]
    except Exception:
        print(f'Exception with host {host}.')
        continue
    break

def find_key_owner(key, cluster):
    keyslot = cluster.cluster_keyslot(counter_key)
    for node_id, node_info in cluster.cluster_nodes().items():
        if 'master' in node_info['flags']:
            for slot_range in node_info['slots']:
                if isinstance(slot_range, list):
                    if int(slot_range[0]) <= keyslot <= int(slot_range[1]):
                        node_host = node_id.split(':')[0]
                        if node_host == '':
                            continue # host may be dead or something, the host value just gone lol
                        name = socket.gethostbyaddr(node_host)[0]
                        if name.find('eas-ds2024-') != -1:
                            node_host = socket.gethostbyaddr(node_host)[0].split('.')[0]

                        print(f'Key {key} with keyslot {keyslot} is stored on node {node_host}')
                        return
                elif keyslot == slot_range:
                    node_host = node_id.split(':')[0]
                    if node_host == '':
                        continue # host may be dead or something, the host value just gone lol
                    name = socket.gethostbyaddr(node_host)[0]
                    if name.find('eas-ds2024-') != -1:
                        node_host = socket.gethostbyaddr(node_host)[0].split('.')[0]
                    print(f'Key {key} with keyslot {keyslot} is stored on node {node_host}')
                    return

def print_simplified_nodes(cluster):
    node_host_id = {}
    nodes = cluster.cluster_nodes()
    for node_id, node_info in nodes.items():
        node_host = node_id.split(':')[0]
        if node_host == '':
            continue # host may be dead or something, the host value just gone lol
        name = socket.gethostbyaddr(node_host)[0]
        if name.find('eas-ds2024-') != -1:
            node_host = socket.gethostbyaddr(node_host)[0].split('.')[0]
        node_host_id[node_info['node_id']] = node_host

    for node_id, node_info in nodes.items():
        node_host = node_id.split(':')[0]
        if node_host == '':
            continue # host may be dead or something, the host value just gone lol
        name = socket.gethostbyaddr(node_host)[0]
        if name.find('eas-ds2024-') != -1:
            node_host = socket.gethostbyaddr(node_host)[0].split('.')[0]
        if 'slave' in node_info['flags']:
            print(f'{node_host}: {node_info["flags"]}, master: {node_host_id[node_info["master_id"]]}')
        else:
            print(f'{node_host}: {node_info["flags"]}')

print_simplified_nodes(cluster)
counter_key = "global_counter"
find_key_owner(counter_key, cluster)

while True:
    try:
        print('-' * 15)
        new_value = cluster.incr(counter_key)
        print(f"INCR: '{counter_key}' = {new_value}")
        nodes = [node.host for node in cluster.get_nodes()]
        print_simplified_nodes(cluster)
        find_key_owner(counter_key, cluster)
    except Exception:
        while True:
            try:
                host = nodes[random.randint(0, len(nodes) - 1)]
                print(f'Trying first host {host}...')
                cluster = redis.RedisCluster(
                    host=host,
                    port= 6379,
                    decode_responses=True
                )
                nodes = [node.host for node in cluster.get_nodes()]
            except Exception:
                print(f'Exception with host {host}.')
                continue
            break

    time.sleep(random.uniform(0.75, 1.3))
