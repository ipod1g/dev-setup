# dev-setup

Personal development setup for macOS and Windows, managed with [chezmoi](https://www.chezmoi.io/).
Homebrew and WinGet install applications; chezmoi restores the reviewed settings.
There is no custom package manager, Node runtime requirement for this repository, or background sync service.

This repository is separate from the [ipod1g GitHub profile](https://github.com/ipod1g/ipod1g).
The default editor is **VS Code**, matching the current preferred editor. Cursor remains an optional alternative.
The VS Code settings and 56-extension inventory now use the user-supplied MacBook configuration, with Mac-specific settings overrides. Cursor retains its separate Windows inventory. The MacBook's keyboard shortcuts are still awaiting capture.

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
Choosing VS Code also installs JetBrainsMono Nerd Font, Neovim, lazygit, and the `bat`, `fzf`, and `ripgrep` tools used by the supplied settings. Cursor retains its smaller baseline. Arc and iTerm2 are referenced by the Mac preferences but are not automatically installed.
Fish is part of the Mac development setup. The optional Mac app bundle installs Raycast, Scroll Reverser, OpenUsage, and the `mas` CLI, then attempts to install RunCat Neo from the Mac App Store. It is enabled by default; set `installMacApps = false` to skip the bundle. A pending App Store sign-in is reported and retried on the next apply while the rest of setup continues. Existing editor and utility apps in `/Applications` or `~/Applications` are retained. See [Fish and Mac app preferences](docs/mac-shell-and-apps.md).
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
editor = "vscode"          # "vscode", "cursor", or "none"
macFishPath = ""          # Optional custom Fish path; standard Homebrew path is automatic
installPackages = true    # Homebrew/WinGet apps and editor extensions
installMacApps = true     # Optional Raycast, Scroll Reverser, OpenUsage, and RunCat Neo bundle
installAgents = true      # Codex, Claude Code, and T3 Code
configureT3 = true        # Preferences and shortcuts, on the SERVER machine
configureCodex = false   # Optional native Windows model preferences; needs account access
legacyNeovim = false     # Optional historical VS Code Neovim integration
```

Set `installPackages` and `installAgents` to `false` for a configuration-only restore.
`installPackages` is the master package-install switch. Keep it `true` and set `installMacApps = false` for development tools without the personal Mac apps or App Store step. Existing configurations without `installMacApps` retain the enabled default. Changing the flag does not uninstall existing apps or remove their preferences.
Existing installations retain their editor choice. To switch an existing Cursor setup, run `chezmoi edit-config`, set `editor = "vscode"`, then review `chezmoi diff` and run `chezmoi apply`.
Set `configureT3 = false` on Windows if T3 runs exclusively in WSL.
Linux/WSL defaults to `editor = "none"`: no Windows editor configuration is written from Linux.
Run chezmoi separately inside WSL to restore the T3 server's preferences. This repo does not install a WSL distribution or provision Linux system packages; provide Git, curl, Bash, and Node/npm there before enabling agent installation.

Before changing any managed configuration, a script copies the existing individual files to
`~/.local/state/dev-setup/backups/<timestamp>-<id>/` (also on Windows). Restore a saved file to its corresponding home-relative path to roll back a setting. Backups are local and may contain private configuration; do not commit them.
Configuration files are restored as complete files, **not merged** with other local settings. In particular, leave `configureCodex` off unless you have reviewed the replacement of any existing hooks, MCP, and trust settings. Disabling a component later stops managing it; it does not uninstall its apps or delete its existing files.

## What is preserved

- The supplied MacBook VS Code settings: 160 shared preferences and six Mac-specific overrides, including Kimbie Dark, JetBrainsMono Nerd Font, relative line numbers, Prettier, custom UI styling, and FindItFaster preferences. See [the settings import notes](docs/macbook-settings.md).
- Fish as the Mac VS Code shell, with an explicit Apple Silicon/Intel Homebrew profile and one managed PATH file at `~/.config/fish/conf.d/10-dev-setup.fish`. Personal Fish configuration, prompt, plugins, and aliases are awaiting capture; the bootstrap does not replace `config.fish` or change the system login shell.
- The 56 VS Code extension IDs supplied from the MacBook, used for VS Code on macOS and Windows. Choosing Cursor restores its separate sixteen-extension inventory from the inspected Windows device. Extension packs may install additional dependencies; extension versions and enabled/disabled states are not captured by this ID-only list.
- T3 server preferences, model favorites, and the current complete keybinding baseline. `mod` maps to Command on macOS and Ctrl on Windows/Linux.
- An optional, allowlisted Codex model configuration from native Windows, disabled by default; WSL had no model defaults to export.
- The six original profile-repo configuration files under `legacy/`, retained as historical references and never installed by default.
- Optional Neovim configuration, adapted from the old snapshot to use `stdpath("config")` and the stable Ctrl+O jump command. The supplied VS Code inventory includes VS Code Neovim; the Mac's current Neovim init/keymaps are still awaiting capture.

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

The capture script defaults to VS Code. It reads only selected settings files and the extension manifest, updates only allowlisted preferences, and skips absent sources. Partial captures preserve the rest of the reviewed profile and its Mac overrides. It supports comments and trailing commas in editor JSON; newly supplied settings beyond the narrow automatic allowlist are reviewed and imported separately.
For a Windows/WSL split, run inside WSL with explicit Windows VS Code sources:

```sh
python3 scripts/capture.py \
  --editor-user-dir /mnt/c/Users/<user>/AppData/Roaming/Code/User \
  --extensions-file /mnt/c/Users/<user>/.vscode/extensions/extensions.json \
  --codex-config /mnt/c/Users/<user>/.codex/config.toml
```

Use `--editor cursor` and the corresponding Cursor paths to capture Cursor instead. On macOS, the default VS Code settings source is `~/Library/Application Support/Code/User/`; use `--editor-user-dir` for a named profile's actual directory.

Extension inventories are stored separately under `editorExtensions.vscode` and `editorExtensions.cursor` in `home/.chezmoidata/extensions.json`. Capturing one editor preserves the other editor's inventory, including its remote extensions. To capture the active VS Code profile's CLI list on macOS:

```sh
code --list-extensions > /tmp/dev-setup-vscode-extensions.txt
python3 scripts/capture.py --extensions-file /tmp/dev-setup-vscode-extensions.txt
```

Add `--profile "<profile-name>"` to the `code` command for a named profile. The capture accepts either an extension JSON manifest or a plain text list; UTF-8 and Windows PowerShell's UTF-16 text exports are supported.

Editor keybindings are deliberately reviewed manually because they can run arbitrary commands. Edit shared files under `home/.chezmoitemplates/` and package/extension lists under `home/.chezmoidata/`. Review `git diff`, then commit and push. Avoid broad `chezmoi add ~/.codex` or `chezmoi add ~/.t3` commands.

## Match the MacBook

The MacBook is user-confirmed as **Apple M1 (Apple Silicon), macOS 27.0.1**, using **Fish**. T3 runs locally on the Mac and also connects to the Windows/WSL environment. Keep `configureT3 = true` on both the Mac and the WSL host; each has its own T3 state and provider logins. See [the MacBook setup guide](docs/macbook-setup.md) for this arrangement.

The macOS path and installer support do not require access to the Mac. To match its actual setup, collect:

```sh
uname -m
sw_vers -productVersion
code --list-extensions
# Optional: compare the Mac's application and CLI selections.
brew leaves
brew list --cask
```

Also review the active VS Code profile's user settings and keyboard shortcuts through **Preferences: Open User Settings (JSON)** and **Preferences: Open Keyboard Shortcuts (JSON)**. If using a named profile, export its extensions with `code --profile "<profile-name>" --list-extensions`.
The current shell choice is Fish; the earlier settings snapshot's zsh default has been updated. iTerm2 remains the configured external terminal and JetBrainsMono Nerd Font is installed. The user settings, extension IDs, OS version, and Mac app list are recorded; the current VS Code keyboard shortcuts, personal Fish configuration, app preferences, and Mac-specific T3 preferences are still awaiting capture.
Review exports for credentials and private project paths before sharing or committing them to this public repository.

## Validation

With Python 3.11+ and chezmoi installed:

```sh
python3 scripts/test_setup.py
```

The suite renders Windows, Apple Silicon/Intel macOS, and WSL configurations; applies files to disposable destinations with installation disabled; checks backups, repeat application, optional components, platform-specific paths, allowlisted capture, and App Store retry behavior. Linux CI uses a checksum-verified portable Fish binary for syntax and PATH checks. CI also runs on native Windows and macOS. No test installs Mac apps, changes real home configuration or login shells, or performs a login.

## Upstream references

- [chezmoi setup and one-command initialization](https://www.chezmoi.io/user-guide/setup/)
- [Homebrew Bundle](https://docs.brew.sh/Brew-Bundle-and-Brewfile)
- [WinGet install](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)
- [VS Code CLI and extensions](https://code.visualstudio.com/docs/configure/command-line)
- [T3 installation](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md) and [keybindings](https://github.com/pingdotgg/t3code/blob/main/docs/user/keybindings.md)
- [Official OpenAI documentation: Codex setup](https://developers.openai.com/codex/quickstart) and [configuration](https://developers.openai.com/codex/config-basic)
- [Claude Code installation](https://code.claude.com/docs/en/setup)
