#!/usr/bin/env python3
"""Install a checksum-verified chezmoi release into the CI temporary directory."""
import hashlib
import io
import os
from pathlib import Path
import platform
import tarfile
import tempfile
import urllib.request
import zipfile

VERSION = "2.73.3"
system = {"Darwin": "darwin", "Linux": "linux", "Windows": "windows"}[platform.system()]
arch = {"x86_64": "amd64", "AMD64": "amd64", "arm64": "arm64", "aarch64": "arm64"}[platform.machine()]
suffix = "zip" if system == "windows" else "tar.gz"
archive = f"chezmoi_{VERSION}_{system}_{arch}.{suffix}"
base = f"https://github.com/twpayne/chezmoi/releases/download/v{VERSION}"


def download(name):
    with urllib.request.urlopen(f"{base}/{name}", timeout=90) as response:
        return response.read()


checksums = download(f"chezmoi_{VERSION}_checksums.txt").decode().splitlines()
expected = next(line.split()[0] for line in checksums if line.endswith(f"  {archive}"))
payload = download(archive)
if hashlib.sha256(payload).hexdigest() != expected:
    raise SystemExit("Downloaded chezmoi archive failed SHA256 verification")
destination = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "dev-setup-test-tools"
destination.mkdir(parents=True, exist_ok=True)
name = "chezmoi.exe" if system == "windows" else "chezmoi"
if suffix == "zip":
    with zipfile.ZipFile(io.BytesIO(payload)) as data:
        executable = data.read(name)
else:
    with tarfile.open(fileobj=io.BytesIO(payload)) as data:
        executable = data.extractfile(name).read()
target = destination / name
target.write_bytes(executable)
target.chmod(0o755)
if "GITHUB_ENV" in os.environ:
    with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as env:
        env.write(f"CHEZMOI_BIN={target}\n")
print(f"Verified chezmoi {VERSION}: {target}")
