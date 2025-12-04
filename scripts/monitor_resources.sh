#!/bin/bash

OUTPUT_FILE="resource_usage.log"
DURATION=300   # 5 minutes

echo "Monitoring system resources for $DURATION seconds..."
echo "Timestamp,CPU%,Memory%,NetworkRx,NetworkTx" > $OUTPUT_FILE

for i in $(seq 1 $DURATION); do
    TIMESTAMP=$(date +%s)
    CPU=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    MEM=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
    
    NET_RX=$(cat /sys/class/net/tun0/statistics/rx_bytes 2>/dev/null || echo 0)
    NET_TX=$(cat /sys/class/net/tun0/statistics/tx_bytes 2>/dev/null || echo 0)

    echo "$TIMESTAMP,$CPU,$MEM,$NET_RX,$NET_TX" >> $OUTPUT_FILE
    sleep 1
done

echo "Monitoring complete. Results saved to $OUTPUT_FILE"

