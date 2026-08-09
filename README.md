# VS Code Offline Installer
可以解决 Remote-SSH 场景下 VS Code Server 的离线预部署问题，通过提前放置指定 commit 对应的 vscode-cli 和 server 文件，让 VS Code Remote-SSH 跳过在线下载步骤



## Client

Download:

[Windows x64 User installer](https://update.code.visualstudio.com/fdb98833154679dbaa7af67a5a29fe19e55c2b73/win32-x64-user/stable)

## Setup

```bash
uv venv
uv sync
```

## Build
```bash
source .venv/bin/activate
bash build.sh
```

## Clean
```bash
rm -rf ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
```

## Run
```bash
/root/vscode-offline-installer/dist/vscode-installer
```

## Dev
```bash
# 编译
source .venv/bin/activate && bash build.sh

# 复制到容器内
docker cp /root/vscode-offline-installer/dist/vscode-installer django-app:/tmp

# 清理
docker exec -it django-app rm -rf ~/.vscode-server

# 执行
docker exec -it django-app /tmp/vscode-installer




# 宿主机
rm -rf ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
rm -f ~/.vscode-server/vscode-cli-fdb98833154679dbaa7af67a5a29fe19e55c2b73.tar.gz
/root/vscode-offline-installer/dist/vscode-installer
```



Remote-SSH 已连接 Linux 宿主机，并且宿主机上的任意 Docker 容器都能 Attach to Running Container

```bash
docker run -d --name hello-world-container busybox sh -c "while true; do echo 'Hello World'; sleep 5; done"
```

批量复制到容器
```bash
for c in $(docker ps -q); do
    echo "install $c"
    docker cp ~/vscode-installer $c:/tmp/
    docker exec $c sh -c "
        chmod +x /tmp/vscode-installer &&
        /tmp/vscode-installer
    "
done


# 检查
find ~/.vscode-server/ -name vscode-cli-fdb98833154679dbaa7af67a5a29fe19e55c2b73.tar.gz
```
