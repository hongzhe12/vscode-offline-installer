#!/usr/bin/env bash

VERSION="fdb98833154679dbaa7af67a5a29fe19e55c2b73"
PACKAGE="/tmp/vscode-server-linux-x64.tar.gz"

# 安装宿主机 VS Code Server
install_host() {
    local target="$HOME/.vscode-server/bin/$VERSION"

    echo "[host] installing..."

    rm -rf "$target"
    mkdir -p "$target"

    tar -xzf "$PACKAGE" \
        --strip-components 1 \
        -C "$target"

    echo "[host] success"
}

# 获取符合条件的容器
get_target_containers() {
    docker ps --format '{{.ID}} {{.Names}}'
}

# 检查容器是否满足条件
check_container() {
    local container="$1"

    docker exec "$container" test -d /root >/dev/null 2>&1
}

# 安装容器内 VS Code Server
install_vscode_server() {
    local container="$1"

    echo "[$container] installing..."

    docker cp "$PACKAGE" \
        "$container:/tmp/vscode-server-linux-x64.tar.gz" || return 1

    docker exec "$container" bash -c "
        rm -rf ~/.vscode-server/bin/$VERSION &&
        mkdir -p ~/.vscode-server/bin/$VERSION &&
        tar -xzf /tmp/vscode-server-linux-x64.tar.gz \
            --strip-components 1 \
            -C ~/.vscode-server/bin/$VERSION
    " || return 1

    echo "[$container] success"
}

# 批量安装
main() {
    local container name

    # 先安装宿主机
    install_host || exit 1

    # 再安装所有符合条件的容器
    while read -r container name; do
        if check_container "$container"; then
            install_vscode_server "$container"
        else
            echo "[$name] skipped"
        fi
    done < <(get_target_containers)
}

main "$@"