#!/bin/bash

# 使用 lsof 找到监听端口 8080 的进程ID
PID=$(lsof -i:8080 -t)

# 检查是否找到进程
if [ -z "$PID" ]; then
  echo "No process is using port 8080."
else
  echo "Found process with PID: $PID. Killing the process..."
  # 终止该进程
  kill -9 $PID
  echo "Process $PID killed."
fi

# 使用 nohup 启动 app.py
echo "Starting app.py..."
nohup python3 app.py &
echo "app.py started."
