# MacBook and Windows/WSL setup

## Confirmed usage

The user confirmed an **Apple M1 MacBook**, **macOS 27.0.1**, **Fish**, and **VS Code** as the preferred editor. T3 runs locally on the Mac and also serves as the interface for the Windows/WSL environment. The Mac also uses RunCat Neo, Scroll Reverser, Raycast, and OpenUsage.
These are user-reported details; this session has inspected the Windows/WSL device, not the MacBook. Its VS Code user settings and 56-extension inventory have been supplied and imported; personal Fish configuration and the Mac app preferences have not been captured.

## MacBook

Use the normal macOS setup in the README. The installer detects Apple Silicon; the Intel-only T3 desktop fallback does not apply to a native ARM64 installation.

Keep these choices in the Mac's `chezmoi edit-config` configuration:

```toml
[data]
editor = "vscode"
macFishPath = ""
installPackages = true
installAgents = true
configureT3 = true
configureCodex = false
legacyNeovim = false
```

These are the defaults for a new macOS setup. They install the local development tools and T3 CLI, and manage the local T3 preferences under `~/.t3/userdata/`.
The optional Codex settings remain disabled so that the native Windows snapshot does not replace the Mac's preferences.
On an existing MacBook, review/export its current preferences before applying the repository's baseline.
The supplied VS Code settings are split into shared settings and Mac overrides; see [the import notes](macbook-settings.md) for the font/tool dependencies and extension inventory.
Fish is installed and selected in VS Code. One managed `conf.d` file loads Homebrew, the Node LTS bin directory, and `~/.local/bin`; it preserves the separate personal `config.fish`, functions, plugin files, and prompt. If Homebrew is in a custom location, set `macFishPath` to the actual Fish binary. System/terminal-app login-shell selection is a separate one-time setting. See [Fish and Mac app preferences](mac-shell-and-apps.md).

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

- VS Code's active profile keyboard shortcuts and any relevant enabled/disabled extension states. The user settings and 56 installed extension IDs are already imported.
- The Mac's Neovim init/keymaps if they should replace the historical opt-in configuration.
- Mac-local T3 preferences if they differ from the current WSL-derived baseline.
- Fish `config.fish`, custom `conf.d`/functions/completions, plugin manifest, abbreviations, and prompt/theme configuration.
- Raycast export kept privately, Scroll Reverser scrolling choices, RunCat Neo runner/metric preferences and assets, and OpenUsage display/provider preferences.
- Optional full Homebrew inventory. Fish and the four named apps are already in the installer plan; iTerm2 remains the configured external terminal, JetBrainsMono Nerd Font the editor font, and Arc the external browser.

Review exports before adding them to this public repository. The existing device audit remains the record of what was actually inspected.
