#!/bin/bash
docker compose up --scale redis=5 redis-joiner -d