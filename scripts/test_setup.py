#!/usr/bin/env python3
"""Exercise real chezmoi rendering and disposable restores without installers."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get("CHEZMOI_BIN") or shutil.which("chezmoi")
DEFAULTS = dict(editor="cursor", installPackages=False, installAgents=False,
                configureT3=True, configureCodex=False, legacyNeovim=False)
NATIVE_OS = {"win32": "windows", "darwin": "darwin"}.get(sys.platform, "linux")
spec = importlib.util.spec_from_file_location("capture", ROOT / "scripts/capture.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dev-setup-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.destination = self.base / "destination"
        self.destination.mkdir()
        self.config = self.base / "config.json"
        self.config.write_text(json.dumps({"data": DEFAULTS}), encoding="utf-8")

    def chez(self, *args, system=None, arch="arm64", data=None, check=True):
        override = dict(data or {})
        override["chezmoi"] = {"os": system or NATIVE_OS, "arch": arch}
        command = [CHEZMOI, "--source", str(ROOT), "--destination", str(self.destination),
                   "--config", str(self.config), "--persistent-state", str(self.base / "state.db"),
                   "--cache", str(self.base / "cache"), "--no-tty", "--no-pager",
                   "--override-data", json.dumps(override), *args]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=45)
        if check and result.returncode:
            self.fail(f"chezmoi {args}: {result.stdout}\n{result.stderr}")
        return result

    def dump(self, system, **data):
        return json.loads(self.chez("dump", "--format", "json", system=system, data=data).stdout)

    def test_platforms_and_editor_selection(self):
        for system, prefix in [("windows", "AppData/Roaming"), ("darwin", "Library/Application Support"), ("linux", None)]:
            for editor, app in [("cursor", "Cursor"), ("vscode", "Code"), ("none", None)]:
                with self.subTest(system=system, editor=editor):
                    result = self.dump(system, editor=editor)
                    files = [k for k, v in result.items() if v["type"] == "file"]
                    self.assertIn(".t3/userdata/settings.json", files)
                    self.assertNotIn(".codex/config.toml", files)
                    if prefix and app:
                        settings = f"{prefix}/{app}/User/settings.json"
                        self.assertIn(settings, files)
                        data = json.loads(result[settings]["contents"])
                        self.assertEqual(data["workbench.iconTheme"], "vscode-icons")
                        self.assertEqual(json.loads(result[f"{prefix}/{app}/User/keybindings.json"]["contents"]), [])
                    self.assertFalse(any(k.startswith("Library/") for k in files) if system != "darwin" else False)
                    self.assertFalse(any(k.startswith("AppData/") for k in files) if system != "windows" else False)
                    if not app:
                        self.assertFalse(any("/User/" in k for k in files))

    def test_optional_components(self):
        for system in ["windows", "darwin", "linux"]:
            with self.subTest(system=system):
                dump = self.dump(system, configureT3=False, configureCodex=True, legacyNeovim=True)
                self.assertNotIn(".t3/userdata/settings.json", dump)
                self.assertIn(".codex/config.toml", dump)
                codex = tomllib.loads(dump[".codex/config.toml"]["contents"])
                self.assertEqual(set(codex), {"model", "model_reasoning_effort", "service_tier", "features"})
                prefix = "AppData/Local/nvim" if system == "windows" else ".config/nvim"
                self.assertIn(f"{prefix}/init.lua", dump)
                keys = dump[f"{prefix}/lua/user/vscode_keymaps.lua"]["contents"]
                self.assertIn('stdpath("config")', keys)
                self.assertNotIn("<SNR>", keys)

    def test_invalid_editor_rejected(self):
        result = self.chez("managed", data={"editor": "typo"}, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("editor must be", result.stderr)

    def test_apply_backup_repeat_and_preserve_unmanaged_files(self):
        path = self.destination / ".t3/userdata/settings.json"
        path.parent.mkdir(parents=True)
        original = '{"existingLocalPreference":true}\n'
        path.write_text(original, encoding="utf-8")
        private = self.destination / ".codex/auth.json"
        private.parent.mkdir()
        private.write_text("unmanaged-auth-sentinel", encoding="utf-8")
        self.chez("apply", "--force")
        first = path.read_bytes()
        self.assertIn("favorites", json.loads(first))
        backups = list(self.destination.glob(".local/state/dev-setup/backups/*/.t3/userdata/settings.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), original)
        self.chez("apply", "--force")
        self.assertEqual(path.read_bytes(), first)
        self.assertEqual(private.read_text(encoding="utf-8"), "unmanaged-auth-sentinel")
        self.chez("verify", "--exclude", "scripts")

    def test_disabled_installers_are_empty(self):
        for system in ["windows", "darwin", "linux"]:
            dump = self.dump(system)
            for name, item in dump.items():
                if "install-" in name:
                    self.assertFalse(item.get("contents", "").strip())

    def test_rendered_installers_parse_without_executing(self):
        rendered = self.base / "rendered"
        rendered.mkdir()
        for system in ["windows", "darwin", "linux"]:
            for arch in ["amd64", "arm64"]:
                dump = json.loads(self.chez("dump", "--format", "json", system=system, arch=arch,
                                           data={"installPackages": True, "installAgents": True, "legacyNeovim": True}).stdout)
                for name, item in dump.items():
                    if item["type"] != "script" or not item.get("contents", "").strip():
                        continue
                    path = rendered / f"{system}-{arch}-{name}"
                    path.write_text(item["contents"], encoding="utf-8")
                    if name.endswith(".sh") and shutil.which("sh"):
                        result = subprocess.run(["sh", "-n", str(path)], capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0, result.stderr)
        if sys.platform == "win32":
            parser = self.base / "parse.ps1"
            parser.write_text("""param([string]$Directory)
$ErrorActionPreference = 'Stop'
Get-ChildItem -LiteralPath $Directory -Filter '*.ps1' | ForEach-Object {
    $tokens = $null; $problems = $null
    [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$problems) | Out-Null
    if ($problems.Count -gt 0) { throw ($problems | Out-String) }
}
""", encoding="utf-8")
            result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-File", str(parser), str(rendered)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_installer_failure_propagates(self):
        if not shutil.which("sh") or sys.platform == "win32":
            self.skipTest("POSIX shell failure test")
        dump = self.dump("darwin", installPackages=True)
        script = self.base / "packages.sh"
        script.write_text(dump["10-install-packages.sh"]["contents"], encoding="utf-8")
        stub = self.base / "brew"
        stub.write_text("#!/bin/sh\nexit 37\n", encoding="utf-8")
        stub.chmod(0o755)
        env = dict(os.environ, PATH=str(self.base) + os.pathsep + os.environ["PATH"])
        result = subprocess.run(["sh", str(script)], env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 37)

    def test_intel_mac_has_desktop_fallback(self):
        result = self.chez("dump", "--format", "json", system="darwin", arch="amd64", data={"installAgents": True})
        script = json.loads(result.stdout)["30-install-agents.sh"]["contents"]
        self.assertIn("brew install --cask t3-code", script)
        self.assertNotIn("https://t3.codes/install.sh", script)


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dev-capture-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        old = capture.REPO
        capture.REPO = self.root
        self.addCleanup(setattr, capture, "REPO", old)
        (self.root / "home/.chezmoitemplates").mkdir(parents=True)

    def test_jsonc_keeps_urls_and_string_content(self):
        source = self.root / "settings.json"
        source.write_text('{ // comment\n"url":"https://example.com/a/*x*/", /* block */ "literal":"a,}", "array":[1,],}', encoding="utf-8")
        self.assertEqual(capture.read_jsonc(source), {"url": "https://example.com/a/*x*/", "literal": "a,}", "array": [1]})

    def test_capture_excludes_credentials_paths_and_trust(self):
        user = self.root / "user"
        user.mkdir()
        (user / "settings.json").write_text(json.dumps({"git.autofetch": True, "apiKey": "DO-NOT-COPY", "mcpServers": {"secret": "DO-NOT-COPY"}}), encoding="utf-8")
        codex = self.root / "config.toml"
        codex.write_text('model = "test-model"\n[projects."private-path"]\ntrust_level="trusted"\n[mcp_servers.private]\napi_key="DO-NOT-COPY"\n', encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            capture.capture_editor(user, self.root / "missing.json", "cursor")
            capture.capture_codex(codex)
        for path in (self.root / "home").rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("DO-NOT-COPY", text)
                self.assertNotIn("private-path", text)
                self.assertNotIn("trust_level", text)

    def test_missing_sources_preserve_existing_snapshot(self):
        target = self.root / "home/.chezmoitemplates/editor-settings.json"
        target.write_text('{"keep": true}', encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            capture.capture_editor(self.root / "absent", self.root / "absent.json", "cursor")
        self.assertEqual(target.read_text(encoding="utf-8"), '{"keep": true}')


if __name__ == "__main__":
    if not CHEZMOI:
        raise SystemExit("Install chezmoi or set CHEZMOI_BIN to its executable path.")
    unittest.main(verbosity=2)
