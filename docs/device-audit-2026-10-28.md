# Device audit — 2026-10-28

Read-only inspection of the connected Windows machine and its WSL2 environment.
This is a snapshot of the accessible device, not a claim about other Macs or PCs.
No real-device configuration was applied as part of creating this repository.

## Observed

- Windows user profile and installed Cursor files were accessible from WSL.
- WSL: Ubuntu 26.04.1 LTS, x86-64, Microsoft WSL2 kernel. Node 22.23.3 and Python 3.14.4 were available.
- Cursor had a user settings file and an empty user keybinding array. Sixteen extension IDs were present in its installed-extension manifest. Installed does not imply enabled or recently used.
- No VS Code user directory or extension directory was found in the inspected Windows user profile. No native Neovim config or PowerShell profile was found at the standard inspected locations.
- T3 Code server 0.1.2 was running in WSL. Its server preferences and keybindings were in `~/.t3/userdata/`. No custom themes were present there.
- T3 preferences: `idleCompaction = "onReturn"`, project settings folded, and agent credits removed on merge. Favorites: Claude Opus 5.5, GPT-6.1 Sol, and GPT-6 Luna.
- T3 environment preferences (separate from the captured JSON): balanced background activity, provider update checks enabled, and new worktrees starting from origin. These are documented here; the repository does not edit T3's environment database.
- Native Windows Codex preferences selected `gpt-6.1-sol`, medium effort, default service tier, and `features.js_repl = false`. Only those values were exported to an optional template.
- WSL Codex configuration contained UI onboarding state and a single local project trust entry; neither belongs in a portable bootstrap.
- The accessible WSL shell startup files appeared to be the distribution defaults; no custom shell configuration was copied.

## Differences from the profile repo

The inspected `ipod1g/ipod1g` checkout was at commit `6ac6567`.
Its VS Code files describe a substantially larger configuration with customized Vim mappings, fonts, and mixed macOS/Windows shortcuts. Those files were not present as the active editor configuration on this device.
They are preserved verbatim under `legacy/` instead of being presented as the currently verified setup. The original GitHub profile repository was not edited.

The Neovim opt-in uses portable config-directory discovery instead of `~/.config/nvim`, and replaces a fragile hardcoded Vim script-number jump with Ctrl+O.
Historical font and theme settings remain reference material. The default current editor configuration requires no custom font installation.

## Capture boundaries

The source paths were the Windows `AppData/Roaming/Cursor/User/` files, Windows `.cursor/extensions/extensions.json`, the WSL `.t3/userdata/{settings,keybindings}.json` files, and an allowlist of native Windows Codex preferences.
App authentication files, environment secrets, shell history, application databases, and work-project source files were not read for export or copied into this repository.

Only the connected device was inspected. A Mac migration still needs a real first installation to validate installer privileges, account entitlements, editor downloads, and app startup. Automated template and filesystem checks cannot establish those outcomes.

## Workspaces and providers

The T3 project list confirmed one registered work repository in WSL with no saved setup scripts. Its source, local path, Git credentials, threads, and database are not included here. Register or clone work projects after authenticating on a new device.
T3 model favorites are portable preferences, not account access grants. Install and authenticate providers locally. Connected plugins and MCP servers need their own authorization; copying the entire application state would mix configuration with credentials and device-specific records.
