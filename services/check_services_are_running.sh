#!/bin/bash
running="$(docker-compose ps --services --filter "status=running")"
services="$(docker-compose ps --services)"
if [ "$running" != "$services" ]; then
    echo "Following services are not running:"
    # Bash specific
    comm -13 <(sort <<<"$running") <(sort <<<"$services")
    exit 1
else
    echo "All services are running"
    exit 0
fi

# docker-compose logs -f nginx published-apis capif-events api-invocation-logs logs service-apis api-invoker-management capif-security easy-rsa api-provider-management