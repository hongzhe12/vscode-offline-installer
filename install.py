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
    print(f"[extract] 开始解压: {tar_path}")

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()
        total = sum(1 for m in members if len(Path(m.name).parts) > strip_components)
        print(f"[extract] 共 {len(members)} 个条目，将解压 {total} 个文件")

        count = 0
        for member in members:
            parts = Path(member.name).parts

            if len(parts) <= strip_components:
                continue

            member.name = str(Path(*parts[strip_components:]))

            tar.extract(
                member,
                target_dir,
                filter="data",
            )
            count += 1

        print(f"[extract] 解压完成，共 {count} 个文件 -> {target_dir}")

def install(commit, cli_tar, server_tar):
    '''
    兼容：
    Remote-SSH 新版 CLI 流程
    Remote-SSH 旧版 server.tar.gz 流程
    Attach Container
    '''
    base = Path.home() / ".vscode-server"

    print(f"[install] commit     = {commit}")
    print(f"[install] cli_tar    = {cli_tar}")
    print(f"[install] server_tar = {server_tar}")

    # 检查资源文件
    if not cli_tar.exists():
        raise FileNotFoundError(f"CLI 文件不存在: {cli_tar}")

    if cli_tar.stat().st_size == 0:
        raise RuntimeError(f"CLI 文件为空: {cli_tar}")

    if not server_tar.exists():
        raise FileNotFoundError(f"Server 文件不存在: {server_tar}")

    # 1. 安装 CLI
    base.mkdir(parents=True, exist_ok=True)
    print(f"[install] 创建目录: {base}")

    cli_target = base / f"vscode-cli-{commit}.tar.gz"
    shutil.copy(cli_tar, cli_target)

    print(f"[install] CLI 文件已复制: {cli_target}")

    cli_done = base / f"vscode-cli-{commit}.tar.gz.done"
    cli_done.touch()

    print(f"[install] CLI 标记创建: {cli_done}")

    # 2. 创建旧版 Remote-SSH 兼容文件
    server_archive = base / "vscode-server.tar.gz"

    shutil.copy(server_tar, server_archive)

    print(f"[install] Server 兼容文件已复制: {server_archive}")

    # 3. 安装新版 Server 布局
    server_dir = (
        base /
        "cli" /
        "servers" /
        f"Stable-{commit}" /
        "server"
    )

    if server_dir.exists():
        print(f"[install] 删除旧 Server: {server_dir}")
        shutil.rmtree(server_dir)

    server_dir.mkdir(parents=True, exist_ok=True)

    print(f"[install] 创建 Server 目录: {server_dir}")

    extract_strip_components(
        server_tar,
        server_dir,
        strip_components=1,
    )

    # 4. 创建兼容旧版 bin 路径
    bin_dir = base / "bin"
    bin_dir.mkdir(exist_ok=True)

    link = bin_dir / commit

    if link.exists() or link.is_symlink():
        link.unlink()

    link.symlink_to(server_dir)

    print(f"[install] 已创建软链接: {link} -> {server_dir}")

    print("[install] 安装完成！")


if __name__ == "__main__":
    commit = "fdb98833154679dbaa7af67a5a29fe19e55c2b73"

    cli_tar = resource_path("packages/vscode_cli_alpine_x64_cli.tar.gz")

    server_tar = resource_path("packages/vscode-server-linux-x64.tar.gz")

    install(
        commit=commit,
        cli_tar=cli_tar,
        server_tar=server_tar,
    )
