# MacBook and Windows/WSL setup

## Confirmed usage

The user confirmed an **Apple M1 MacBook** with **VS Code** as the preferred editor. T3 runs locally on the Mac and also serves as the interface for the Windows/WSL environment.
These are user-reported details; this session has inspected the Windows/WSL device, not the MacBook. Its macOS version and current local configuration have not been captured.

## MacBook

Use the normal macOS setup in the README. The installer detects Apple Silicon; the Intel-only T3 desktop fallback does not apply to a native ARM64 installation.

Keep these choices in the Mac's `chezmoi edit-config` configuration:

```toml
[data]
editor = "vscode"
installPackages = true
installAgents = true
configureT3 = true
configureCodex = false
legacyNeovim = false
```

These are the defaults for a new macOS setup. They install the local development tools and T3 CLI, and manage the local T3 preferences under `~/.t3/userdata/`.
The optional Codex settings remain disabled so that the native Windows snapshot does not replace the Mac's preferences.
On an existing MacBook, review/export its current preferences before applying the repository's baseline.

For the native desktop interface, the upstream installation command is `brew install --cask t3-code`; the Apple Silicon CLI branch itself installs the CLI, not the desktop app. Existing desktop installations can be retained. See [T3 installation](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md).

## Windows/WSL host

Run chezmoi inside the WSL distribution that hosts the agents, independently of the Mac's installation:

```toml
[data]
editor = "none"
installPackages = false
installAgents = true
configureT3 = true
configureCodex = false
legacyNeovim = false
```

Provide Git, curl, Bash, and Node/npm in WSL first. The repository's system-package installation covers macOS and native Windows; it does not provision a Linux distribution.
If native Windows is used only for VS Code and all agents run in WSL, set `installAgents = false` and `configureT3 = false` in the native Windows chezmoi config. Leave its editor as `vscode`.

## Connect the two environments

Keep the Mac's local environment and the Windows/WSL environment available in T3. Choose the environment that should run each project or thread.
Install and authenticate providers on each machine where agents actually run. Provider credentials, project paths, and thread databases remain specific to that host; a connection from the Mac does not move them onto the Mac. See [T3's provider setup](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md#providers).

After replacing a device, restore its reviewed configuration, then reconnect to the Windows/WSL host using the existing connection method. T3 Connect or a fresh pairing link can authorize a new client; the repository does not store pairing links, tokens, host addresses, or connection credentials. See [T3 remote access](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md).

## Remaining capture

- macOS version: `sw_vers -productVersion`.
- VS Code's active profile settings and keyboard shortcuts, plus `code --list-extensions` (add `--profile "<profile-name>"` for a named profile).
- Mac-local T3 preferences if they differ from the current WSL-derived baseline.
- Optional shell, terminal, fonts, and Homebrew package choices.

Review exports before adding them to this public repository. The existing device audit remains the record of what was actually inspected.
