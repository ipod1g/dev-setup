# dev-setup

Personal development setup for macOS and Windows, managed with [chezmoi](https://www.chezmoi.io/).
Homebrew and WinGet install applications; chezmoi restores the reviewed settings.
There is no custom package manager, Node runtime requirement for this repository, or background sync service.

This repository is separate from the [ipod1g GitHub profile](https://github.com/ipod1g/ipod1g).
The default editor is **Cursor**, matching the device inspected on 2026-10-28. VS Code is an optional alternative.

## New device

This repository is public. Install the prerequisites below; downloading the setup does not require a GitHub login.

macOS, with [Homebrew](https://brew.sh) installed:

```sh
brew install chezmoi git
```

Windows, in PowerShell, with [WinGet](https://aka.ms/getwinget) installed:

```powershell
winget install --id twpayne.chezmoi --exact --source winget
winget install --id Git.Git --exact --source winget
# Open a new PowerShell window so PATH includes the installed commands.
```

Then **the same command on either OS** restores the setup:

```sh
chezmoi init --apply https://github.com/ipod1g/dev-setup.git
```

It installs Git, GitHub CLI, Node LTS, the selected editor and extensions, Codex, Claude Code, and T3 Code.
On macOS Node 24 LTS is selected; WinGet uses its current Node LTS package. This is a reproducible selection of tools and settings, not a lock of every application version.
Existing applications are retained without a requested upgrade. Agent installs are skipped when their command is already available.

The first apply can request OS administrator approval or acceptance of installer requirements.
Sign in to **Codex**, **Claude Code**, and any editor services separately. For private projects or authenticated GitHub operations, run `gh auth login`; use `gh auth setup-git` if Git should use that login. Tokens, SSH keys, cookies, and subscriptions are never copied.
Add `~/.local/bin` to PATH if the upstream agent installers request it. On Intel Macs, T3's desktop app is installed through Homebrew; install its `t3` command from the app's Settings → General → About. Upstream has no standalone Intel Mac server binary.

## Preview or customize

On an existing device, close the apps whose configuration will change, then review first:

```sh
chezmoi init https://github.com/ipod1g/dev-setup.git
chezmoi edit-config
chezmoi diff
chezmoi apply --dry-run --verbose
chezmoi apply
```

The machine's `chezmoi.toml` has these choices under `[data]`:

```toml
editor = "cursor"          # "cursor", "vscode", or "none"
installPackages = true    # Homebrew/WinGet apps and editor extensions
installAgents = true      # Codex, Claude Code, and T3 Code
configureT3 = true        # Preferences and shortcuts, on the SERVER machine
configureCodex = false   # Optional native Windows model preferences; needs account access
legacyNeovim = false     # Optional historical VS Code Neovim integration
```

Set both installation flags to `false` for a configuration-only restore.
Set `configureT3 = false` on Windows if T3 runs exclusively in WSL.
Linux/WSL defaults to `editor = "none"`: no Windows editor configuration is written from Linux.
Run chezmoi separately inside WSL to restore the T3 server's preferences. This repo does not install a WSL distribution or provision Linux system packages; provide Git, curl, Bash, and Node/npm there before enabling agent installation.

Before changing any managed configuration, a script copies the existing individual files to
`~/.local/state/dev-setup/backups/<timestamp>-<id>/` (also on Windows). Restore a saved file to its corresponding home-relative path to roll back a setting. Backups are local and may contain private configuration; do not commit them.
Configuration files are restored as complete files, **not merged** with other local settings. In particular, leave `configureCodex` off unless you have reviewed the replacement of any existing hooks, MCP, and trust settings. Disabling a component later stops managing it; it does not uninstall its apps or delete its existing files.

## What is preserved

- Cursor's inspected settings and 16 installed extension IDs. The VS Code alternative uses the three shared settings and the corresponding Microsoft remote extensions.
- T3 server preferences, model favorites, and the current complete keybinding baseline. `mod` maps to Command on macOS and Ctrl on Windows/Linux.
- An optional, allowlisted Codex model configuration from native Windows, disabled by default; WSL had no model defaults to export.
- The six original profile-repo configuration files under `legacy/`, retained as historical references and never installed by default.
- Optional Neovim configuration, adapted from the old snapshot to use `stdpath("config")` and the stable Ctrl+O jump command. Enable the VS Code Neovim extension separately if using it.

The historical PowerShell profile is archived only: no equivalent active profile was found on the inspected device. Its Windows-specific `ls` alias and self-editing startup behavior are not applied automatically.
No company repositories, project registrations, workspace databases, agent conversations, MCP credentials, or authenticated plugin installations are copied.
See [the device audit](docs/device-audit-2026-10-28.md) for evidence and coverage limits.

## Keep the setup current

```sh
chezmoi update                     # Pull and apply reviewed upstream changes
chezmoi doctor
```

To capture updated preferences, use Python 3.11+ from a checkout:

```sh
python scripts/capture.py          # On Windows; use python3 on macOS/Linux
git diff
```

The capture script reads only selected settings files and the extension manifest, writes only allowlisted preferences, and skips absent sources. It supports comments and trailing commas in editor JSON.
For this Windows/WSL split, run inside WSL with explicit Windows editor sources:

```sh
python3 scripts/capture.py \
  --editor-user-dir /mnt/c/Users/<user>/AppData/Roaming/Cursor/User \
  --extensions-file /mnt/c/Users/<user>/.cursor/extensions/extensions.json \
  --codex-config /mnt/c/Users/<user>/.codex/config.toml
```

Editor keybindings are deliberately reviewed manually because they can run arbitrary commands. Edit shared files under `home/.chezmoitemplates/` and package/extension lists under `home/.chezmoidata/`. Review `git diff`, then commit and push. Avoid broad `chezmoi add ~/.codex` or `chezmoi add ~/.t3` commands.

## Validation

With Python 3.11+ and chezmoi installed:

```sh
python3 scripts/test_setup.py
```

The suite renders Windows, Apple Silicon/Intel macOS, and WSL configurations; applies files to disposable destinations with installation disabled; checks backups, repeat application, optional components, platform-specific paths, and allowlisted capture. CI also runs on native Windows and macOS. No test installs applications, changes real home configuration, or performs a login.

## Upstream references

- [chezmoi setup and one-command initialization](https://www.chezmoi.io/user-guide/setup/)
- [Homebrew Bundle](https://docs.brew.sh/Brew-Bundle-and-Brewfile)
- [WinGet install](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)
- [VS Code CLI and extensions](https://code.visualstudio.com/docs/configure/command-line)
- [T3 installation](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md) and [keybindings](https://github.com/pingdotgg/t3code/blob/main/docs/user/keybindings.md)
- [Official OpenAI documentation: Codex setup](https://developers.openai.com/codex/quickstart) and [configuration](https://developers.openai.com/codex/config-basic)
- [Claude Code installation](https://code.claude.com/docs/en/setup)
