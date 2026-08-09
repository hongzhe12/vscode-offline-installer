from pathlib import Path
import tarfile
import shutil

import sys
from pathlib import Path


def resource_path(relative):
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative
    return Path(__file__).parent / relative


def install(commit, cli_tar, server_tar):
    base = Path.home() / ".vscode-server"

    # 1. 放置 CLI 标记文件
    cli_target = base / f"vscode-cli-{commit}.tar.gz.done"
    base.mkdir(parents=True, exist_ok=True)

    shutil.copy(cli_tar, cli_target)

    # 2. 解压 Server
    server_dir = base / "cli" / "servers" / f"Stable-{commit}" / "server"

    server_dir.mkdir(parents=True, exist_ok=True)

    with tarfile.open(server_tar) as tar:
        tar.extractall(path=server_dir, filter="data")

    # 3. 创建兼容软链接
    bin_dir = base / "bin"
    bin_dir.mkdir(exist_ok=True)

    link = bin_dir / commit

    if not link.exists():
        link.symlink_to(server_dir)


if __name__ == "__main__":
    cli_tar = resource_path("packages/vscode_cli_alpine_x64_cli.tar.gz")

    server_tar = resource_path("packages/vscode-server-linux-x64.tar.gz")

    install(
        commit="fdb98833154679dbaa7af67a5a29fe19e55c2b73",
        cli_tar=cli_tar,
        server_tar=server_tar,
    )
