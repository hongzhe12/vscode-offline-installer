# VS Code Offline Installer
可以解决 Remote-SSH 场景下 VS Code Server 的离线预部署问题，通过提前放置指定 commit 对应的server文件，让 VS Code Remote-SSH 跳过在线下载步骤

## Client

Download:

[Windows x64 User installer](https://update.code.visualstudio.com/fdb98833154679dbaa7af67a5a29fe19e55c2b73/win32-x64-user/stable)

## Setup
```bash
# clean
rm -rf ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
# create
mkdir -p ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
# extract
tar -xvzf /tmp/vscode-server-linux-x64.tar.gz --strip-components 1 -C ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
```
