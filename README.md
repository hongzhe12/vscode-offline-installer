# VS Code Offline Installer

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
source .venv/bin/activate
bash build.sh
rm -rf ~/.vscode-server/bin/fdb98833154679dbaa7af67a5a29fe19e55c2b73
/root/vscode-offline-installer/dist/vscode-installer
```
