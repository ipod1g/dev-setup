# Fish and Mac app preferences

The user reports an M1 MacBook running macOS 27.0.1, with Fish, RunCat Neo, Scroll Reverser, Raycast, and [OpenUsage](https://github.com/robinebers/openusage). The package selection is recorded; the exact personal shell and app preferences have not yet been exported.

## What the bootstrap handles

Homebrew installs `fish`, `mas`, `raycast`, `scroll-reverser`, and `openusage` on the Mac, alongside the existing development tools. Existing editor and utility apps in `/Applications` or `~/Applications` are retained without an attempted cask replacement.
VS Code uses Fish with the standard Apple Silicon or Intel Homebrew binary path. For a custom prefix, set `macFishPath` in `chezmoi edit-config`. Windows and WSL shell choices are unchanged. FindItFaster retains its separate Bash helper setting.

The single managed file `~/.config/fish/conf.d/10-dev-setup.fish` loads Homebrew's Fish environment and adds Node 24 LTS and `~/.local/bin` to the session PATH. Repeated sourcing does not duplicate those paths, and it does not write universal variables. An existing copy is backed up before replacement. The personal `config.fish`, other `conf.d` files, functions, and plugins are not replaced.

RunCat **Neo** is the [App Store application](https://apps.apple.com/app/id6757801838), not the original RunCat. Its upstream [installation instructions](https://github.com/runcat-dev/RunCatNeo#installation) require macOS 26 or later. The bootstrap uses `mas install 6757801838`, skips an already installed copy, and reports a pending App Store sign-in if installation cannot complete. The remaining setup continues, and the next `chezmoi apply` retries the App Store step. Paid in-app runner purchases are not performed by this script.

Current OpenUsage requires [macOS 15 or later](https://github.com/robinebers/openusage#requirements). The reported macOS 27.0.1 meets both app requirements. The repository installs the current cask versions; it does not export, downgrade, or force an upgrade of the installed app versions.

## Fish settings to preserve

Keep reviewed personal files from `~/.config/fish/`:

- `config.fish` and custom `conf.d/*.fish` startup snippets.
- Custom `functions/*.fish`, including `fish_prompt.fish`, `fish_right_prompt.fish`, and `fish_user_key_bindings.fish` if present.
- Custom `completions/*.fish` and `themes/*.theme` files.
- `fish_plugins` if Fisher is used, or the equivalent plugin list for another manager.
- A separate prompt configuration, such as `~/.config/starship.toml`, if used.

`abbr --show` lists the abbreviation definitions that may need to be moved into reviewed configuration. Also preserve the terminal app's profile that launches Fish, its font choice, and custom terminal keybindings.
Universal preferences should be converted into explicit, reviewed Fish configuration. Do not publish or blindly restore all of `fish_variables`: it can hold machine-specific paths and private environment values, and Fish manages it itself. Shell history is not part of the portable setup. The repository ignores `fish_variables`, `fish_history`, and old `fishd.*` state files.

Selecting Fish as the system login shell or as the terminal app's launch command is a separate one-time Mac setting. The bootstrap selects it in VS Code but does not edit `/etc/shells`, run `chsh`, or rewrite an unknown terminal app profile. See [Fish configuration](https://fishshell.com/docs/current/language.html#configuration-files), [universal variables](https://fishshell.com/docs/current/language.html#universal-variables), and [Fish PATH management](https://fishshell.com/docs/current/cmds/fish_add_path.html).

## Raycast

Use Raycast's **Export Settings & Data** command for a private backup of the setup, including extensions, aliases, hotkeys, snippets, quicklinks, and layouts. Restore it with **Import Settings & Data** on the new device.
The [current export format](https://manual.raycast.com/import-export) can also include clipboard history, notes, chats, and MCP settings. Keep the encrypted `.rayconfig` backup and its passphrase privately; do not add the complete export to this public repository. The repository ignores `.rayconfig` and older `.raycastconfig` exports. Non-sensitive hotkey and extension selections can be documented separately after review.

## Scroll Reverser

Preserve the chosen vertical and horizontal scrolling behavior for each mouse/trackpad, step size, and launch-at-login choice. Newer versions store per-device rules, so check them with the new machine's actual devices rather than assuming hardware identifiers carry over.
A private backup can be made outside the checkout:

```sh
mkdir -p "$HOME/.local/state/dev-setup/private-backups"
defaults export com.pilotmoon.scroll-reverser "$HOME/.local/state/dev-setup/private-backups/scroll-reverser.plist"
```

Review and reapply the settings with the app closed. New-device Accessibility permission still needs to be granted through macOS; it is not a portable preference. See the [official app guide](https://pilotmoon.com/scrollreverser/).

## RunCat Neo

Preserve the selected runner, animation/metric preferences, menu bar choices, launch-at-login choice, and any custom runner assets or custom-metric JSON/generator scripts. Custom metric paths may need to change on the new device. Restore purchased content through the App Store account and the app's supported restore flow; purchase entitlements are not dotfiles. See [the upstream custom metrics and runner documentation](https://github.com/runcat-dev/RunCatNeo#custom-metrics).

## OpenUsage

Preserve enabled providers, provider/metric order and pins, icon style, theme/density, used-versus-left display, reset-time display, global shortcut, launch-at-login choice, and notification preferences. See [OpenUsage settings](https://github.com/robinebers/openusage/blob/main/docs/settings.md).
Provider logins and API keys stay local. OpenUsage can reuse credentials already present on that Mac; authenticate the relevant tools again after migration. Do not copy Keychain data, provider auth files, usage caches, or application databases into the repo. The optional `~/.openusage/config.json` proxy file may contain credentials inside a proxy URL, so review it before exporting any part of it. See [OpenUsage proxy configuration](https://github.com/robinebers/openusage/blob/main/docs/proxy.md).

## Remaining exports

The next useful input is the reviewed Fish configuration and plugin/prompt list. App preferences can follow as selected settings or screenshots without tokens; keep full Raycast and application-data backups in private storage. Accessibility permissions, App Store sign-in, and any app login-item confirmations are completed on each new Mac.
