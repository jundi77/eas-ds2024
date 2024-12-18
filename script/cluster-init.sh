#!/bin/sh

# Loop until this container responds with PONG
while true; do
    if redis-cli ping | grep -q "PONG"; then
        echo "Redis server is ready!"
        # redis-cli --cluster create redis-node-1:6379 redis-node-2:6379 redis-node-3:6379 redis-node-4:6379 redis-node-5:6379 redis-node-6:6379 --cluster-replicas 1 --cluster-yes 
        redis-cli --cluster create eas-ds2024-redis-joiner-1:6379 eas-ds2024-redis-1:6379 eas-ds2024-redis-2:6379 eas-ds2024-redis-3:6379 eas-ds2024-redis-4:6379 eas-ds2024-redis-5:6379 --cluster-replicas 1 --cluster-yes 
        break
    else
        echo "Waiting for Redis server..."
        sleep 1 # SECONDS
    fi
done
