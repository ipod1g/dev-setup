#!/usr/bin/env python3
"""Capture only allowlisted preferences; never copy an app's state directory."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import tomllib

REPO = Path(__file__).resolve().parents[1]
EDITOR_KEYS = {"window.autoDetectColorScheme", "git.autofetch", "workbench.iconTheme"}
T3_KEYS = {"favorites", "projectSettingsFolded", "idleCompaction", "removeAgentCreditsOnMerge"}


def read_jsonc(path):
    text = path.read_text(encoding="utf-8-sig")
    # Match strings first so URLs and comment characters inside them survive.
    text = re.sub(r'("(?:\\.|[^"\\])*")|//[^\r\n]*|/\*.*?\*/',
                  lambda m: m[1] or "", text, flags=re.S)
    text = re.sub(r'("(?:\\.|[^"\\])*")|,(\s*[}\]])',
                  lambda m: m[1] or m[2], text)
    return json.loads(text)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {path.relative_to(REPO)}")


def capture_editor(user_dir, extension_file, editor):
    templates = REPO / "home/.chezmoitemplates"
    settings_file = user_dir / "settings.json"
    if settings_file.is_file():
        data = read_jsonc(settings_file)
        shared = {k: v for k, v in data.items() if k in EDITOR_KEYS}
        write_json(templates / "editor-settings.json", shared)
        if editor == "cursor":
            cursor = dict(shared)
            if "window.commandCenter" in data:
                cursor["window.commandCenter"] = data["window.commandCenter"]
            write_json(templates / "cursor-settings.json", cursor)
        print("Other editor settings were omitted; review any additions individually.")
    else:
        print(f"Not found; retained existing snapshot: {settings_file}")
    # Keybindings can invoke arbitrary shell commands. Review changes manually.
    if extension_file.is_file():
        records = read_jsonc(extension_file)
        ids = sorted({x["identifier"]["id"] for x in records})
        if not all(re.fullmatch(r"[A-Za-z0-9_-]+\.[A-Za-z0-9_.-]+", x) for x in ids):
            raise ValueError("Unexpected extension identifier; no extension snapshot was written")
        ids = [x for x in ids if not x.startswith(("anysphere.remote-", "ms-vscode-remote."))]
        write_json(REPO / "home/.chezmoidata/extensions.json", {"extensions": ids})
    else:
        print(f"Not found; retained extension snapshot: {extension_file}")


def capture_t3(userdata):
    templates = REPO / "home/.chezmoitemplates"
    path = userdata / "settings.json"
    if path.is_file():
        data = read_jsonc(path)
        safe = {k: v for k, v in data.items() if k in T3_KEYS}
        if "favorites" in safe:
            safe["favorites"] = [{k: v for k, v in x.items() if k in {"provider", "model"}}
                                 for x in safe["favorites"]]
        write_json(templates / "t3-settings.json", safe)
    else:
        print(f"Not found; retained T3 settings snapshot: {path}")
    path = userdata / "keybindings.json"
    if path.is_file():
        rules = read_jsonc(path)
        if not isinstance(rules, list):
            raise ValueError("T3 keybindings must be an array")
        safe = []
        for rule in rules:
            if not isinstance(rule, dict) or not all(k in rule for k in ("key", "command")):
                raise ValueError("Unexpected T3 keybinding")
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", rule["command"]):
                raise ValueError("Unexpected T3 command; review the shortcut manually")
            safe.append({k: v for k, v in rule.items() if k in {"key", "command", "when"}})
        write_json(templates / "t3-keybindings.json", safe)


def capture_codex(path):
    if not path.is_file():
        print(f"Not found; retained Codex snapshot: {path}")
        return
    data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    lines = ["# Reviewed portable preferences. Authentication and project trust stay local."]
    for key in ("model", "model_reasoning_effort", "service_tier"):
        if isinstance(data.get(key), str):
            lines.append(f"{key} = {json.dumps(data[key])}")
    # Do not replace a useful native snapshot with a WSL trust-only configuration.
    if len(lines) == 1:
        print("No portable Codex preferences found; retained existing snapshot.")
        return
    flag = data.get("features", {}).get("js_repl")
    if isinstance(flag, bool):
        lines.extend(["", "[features]", f"js_repl = {str(flag).lower()}"])
    target = REPO / "home/.chezmoitemplates/codex-config.toml"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {target.relative_to(REPO)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", choices=("cursor", "vscode"), default="cursor")
    parser.add_argument("--editor-user-dir", type=Path)
    parser.add_argument("--extensions-file", type=Path)
    parser.add_argument("--t3-userdata", type=Path, default=Path.home() / ".t3/userdata")
    parser.add_argument("--codex-config", type=Path, default=Path.home() / ".codex/config.toml")
    args = parser.parse_args()
    app = "Cursor" if args.editor == "cursor" else "Code"
    if sys.platform == "win32":
        base = Path(os.environ["APPDATA"])
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    user_dir = args.editor_user_dir or base / app / "User"
    extension_file = args.extensions_file or Path.home() / (".cursor" if args.editor == "cursor" else ".vscode") / "extensions/extensions.json"
    capture_editor(user_dir, extension_file, args.editor)
    capture_t3(args.t3_userdata)
    capture_codex(args.codex_config)
    print("Review git diff before committing. No credentials or application databases were read.")


if __name__ == "__main__":
    main()
