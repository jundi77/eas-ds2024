```
This will focus on redis, not the use case implementation of redis. The implementation instead will be a simple counter app. For the case, we will create 2 python script as a client that connect to a redis node. This two will do an increment operation to a key that's set in a redis. We should see an info about the cluster info/topology, hash slot and info on where the key resides, and other things. Other than python script that prints changes, we also will use Wireshark to see what is happening inside the network.

To run the infrastructure required for the task, please run start.sh
To stop the infrastructure required for the task, please run stop.sh --> Be warned that any data in redis nodes will be lost.

https://redis.io/docs/latest/operate/rs/release-notes/: 7.8.2 releases --> no version on docker, 7.4.1 will be used instead
```
