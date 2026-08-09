安装依赖
```bash
uv venv
uv sync
```

编译打包
```bash
source .venv/bin/activate
bash build.sh
```

清理
```bash
rm -rf ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
```

开发
```bash
source .venv/bin/activate && bash build.sh
rm -rf ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73

/root/vscode-offline-installer/dist/vscode-installer
```
