from pathlib import Path
import shutil
import sys
import tarfile


def resource_path(relative):
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative

    return Path(__file__).parent / relative


def extract_strip_components(tar_path, target_dir, strip_components=1):
    """解压 tar.gz，去掉第一层目录"""
    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar.getmembers():
            parts = Path(member.name).parts

            if len(parts) <= strip_components:
                continue

            member.name = str(Path(*parts[strip_components:]))

            tar.extract(
                member,
                target_dir,
                filter="data",
            )

def install(commit, cli_tar, server_tar):
    base = Path.home() / ".vscode-server"

    # 1. CLI 标记文件
    base.mkdir(parents=True, exist_ok=True)

    cli_target = base / f"vscode-cli-{commit}.tar.gz.done"
    shutil.copy(cli_tar, cli_target)

    # 2. 解压 Server
    server_dir = base / "cli" / "servers" / f"Stable-{commit}" / "server"

    server_dir.mkdir(parents=True, exist_ok=True)

    extract_strip_components(
        server_tar,
        server_dir,
        strip_components=1,
    )

    # 3. 创建兼容旧版路径软链接
    bin_dir = base / "bin"
    bin_dir.mkdir(exist_ok=True)

    link = bin_dir / commit

    if not link.exists():
        link.symlink_to(server_dir)


if __name__ == "__main__":
    commit = "fdb98833154679dbaa7af67a5a29fe19e55c2b73"

    cli_tar = resource_path("packages/vscode_cli_alpine_x64_cli.tar.gz")

    server_tar = resource_path("packages/vscode-server-linux-x64.tar.gz")

    install(
        commit=commit,
        cli_tar=cli_tar,
        server_tar=server_tar,
    )
