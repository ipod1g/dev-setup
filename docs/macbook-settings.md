# MacBook VS Code settings import

Source: the user supplied the current VS Code user `settings.json` in this conversation. This import is based on that text, not direct access to the MacBook.
All 170 active top-level preferences are accounted for. Disabled settings and comments were omitted, and the active values were normalized to valid JSON.

## Portable settings

The 160 shared settings live in [`editor-settings.json`](../home/.chezmoitemplates/editor-settings.json). They are used by VS Code on both Windows and macOS, including:

- Prettier formatters and formatting behavior for CSS, HTML, JavaScript, TypeScript, JSX/TSX, JSON, and JSONC.
- Kimbie Dark, color customizations, JetBrainsMono Nerd Font, size 13, relative line numbers, sidebar/tab/terminal layout, and custom CSS.
- GitLens, Error Lens, YAML tags, editor behavior, and the supplied FindItFaster preview command.

The six Mac overrides live in [`editor-settings.macos.json`](../home/.chezmoitemplates/editor-settings.macos.json):

- `terminal.integrated.defaultProfile.osx`: zsh.
- `terminal.external.osxExec`: iTerm2.
- `terminal.integrated.env.osx`: the supplied `FIG_NEW_SESSION` flag.
- `workbench.externalBrowser`: Arc.
- `find-it-faster.general.shellPathForTerminal`: `/bin/bash`.
- `custom-ui-style.electron`: the supplied Electron window and vibrancy options.

Those six preferences are not emitted into Windows VS Code settings. Cursor keeps the previously inspected minimal profile; it does not inherit the VS Code Custom UI Style configuration.

## Portability adjustments

The Bitbucket Pipelines YAML schema originally pointed into a specific user's versioned Cursor extension directory. That file reference was replaced with [Atlassian's public schema](https://api.bitbucket.org/schemas/pipelines-configuration), keeping its `bitbucket-pipelines.yml` association.
The exported settings contain no user-specific schema file path or versioned Cursor extension path.

Four leftover `cursor.*` settings are preserved as a reference in [`legacy/macbook-cursor-only-settings.json`](../legacy/macbook-cursor-only-settings.json), and are not emitted into VS Code settings:

- `cursor.cpp.disabledLanguages`
- `cursor.composer.collapsePaneInputBoxPills`
- `cursor.composer.renderPillsInsteadOfBlocks`
- `cursor.composer.usageSummaryDisplay`

The rest of the active preferences retain the supplied values, including `$message` templates, CSS declarations, array ordering, and FindItFaster's `{1}`/`{2}` placeholders. No credential or project configuration was added.

## Tools and extensions

When VS Code is selected and `installPackages = true`, the package scripts also install:

- JetBrainsMono Nerd Font: Homebrew's `font-jetbrains-mono-nerd-font`, or WinGet's `DEVCOM.JetBrainsMonoNerdFont`.
- `fzf`, `ripgrep` (`rg`), and `bat` for [FindItFaster](https://github.com/tomrijndorp/vscode-finditfaster#requirements). Its upstream requirements also include `sed`, which is available in macOS; native Windows support is experimental, so validate the extension's Windows shell behavior after installation.
- `lazygit` and Neovim for the configured integrations. Neovim's historical init/keymaps remain separately opt-in through `legacyNeovim`; the current Mac init/keymaps have not been supplied.

The Mac's external browser and external terminal preferences are retained. Arc and iTerm2 application installation is not added to the bootstrap at this stage.
An extension's settings do not prove that it is currently installed. The installer still uses the earlier reviewed extension inventory; the user needs to supply `code --list-extensions` to confirm the complete Mac profile. In particular, VS Code Neovim, FindItFaster, lazygit, Custom UI Style, YAML, and other settings-referenced extensions should be checked against that inventory before declaring the editor fully reproduced.

[Custom UI Style](https://github.com/subframe7536/vscode-custom-ui-style#usage) applies CSS/Electron changes through its own backup and `Custom UI Style: Reload` commands. This bootstrap stores the preferences; it does not run those patching commands. Extension installation and editor startup on the actual Mac still need validation.

## Future captures

The automatic capture script still updates only its narrow allowlist. It now merges those captured preferences into the reviewed profile, preserving the full imported configuration and separate Mac overrides. Review additional settings manually before publishing them.

The remaining inputs are the macOS version, current keyboard shortcuts, actual extension list, and any Mac-local T3 preferences that differ from the WSL-derived baseline.
