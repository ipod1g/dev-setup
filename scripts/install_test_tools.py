#!/usr/bin/env python3
"""Place verified chezmoi and Linux Fish test binaries in a temporary directory."""
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

# Linux provides a portable Fish binary for syntax/startup checks. This does not
# install a shell into the runner's system or change its login shell.
if system == "linux":
    fish_version = "4.9.3"
    fish_arch, fish_digest = {
        "amd64": ("x86_64", "8f643d10ad1abb0ef7072764c01ceb5cf61b2d373fda400cf60f0bad69b7e095"),
        "arm64": ("aarch64", "57349f0111728c64b703a84e611aa97ff4d1fa8466385d64e67bd5bc3ffa49fc"),
    }[arch]
    fish_url = f"https://github.com/fish-shell/fish-shell/releases/download/{fish_version}/fish-{fish_version}-linux-{fish_arch}.tar.xz"
    with urllib.request.urlopen(fish_url, timeout=90) as response:
        fish_payload = response.read()
    if hashlib.sha256(fish_payload).hexdigest() != fish_digest:
        raise SystemExit("Portable Fish archive failed SHA256 verification")
    with tarfile.open(fileobj=io.BytesIO(fish_payload)) as data:
        fish_executable = data.extractfile("fish").read()
    fish_target = destination / "fish"
    fish_target.write_bytes(fish_executable)
    fish_target.chmod(0o755)
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as env:
            env.write(f"FISH_BIN={fish_target}\n")
    print(f"Verified portable Fish {fish_version}: {fish_target}")
