# MacBook VS Code settings import

Source: the user supplied the current VS Code user `settings.json` in this conversation. This import is based on that text, not direct access to the MacBook.
All 170 active top-level preferences are accounted for. Disabled settings and comments were omitted, and the active values were normalized to valid JSON.

## Portable settings

The 160 shared settings live in [`editor-settings.json`](../home/.chezmoitemplates/editor-settings.json). They are used by VS Code on both Windows and macOS, including:

- Prettier formatters and formatting behavior for CSS, HTML, JavaScript, TypeScript, JSX/TSX, JSON, and JSONC.
- Kimbie Dark, color customizations, JetBrainsMono Nerd Font, size 13, relative line numbers, sidebar/tab/terminal layout, and custom CSS.
- GitLens, Error Lens, YAML tags, editor behavior, and the supplied FindItFaster preview command.

The six Mac overrides live in [`editor-settings.macos.json`](../home/.chezmoitemplates/editor-settings.macos.json):

- `terminal.integrated.defaultProfile.osx`: Fish, updated after the user clarified the current shell.
- `terminal.external.osxExec`: iTerm2.
- `terminal.integrated.env.osx`: the supplied `FIG_NEW_SESSION` flag.
- `workbench.externalBrowser`: Arc.
- `find-it-faster.general.shellPathForTerminal`: `/bin/bash`.
- `custom-ui-style.electron`: the supplied Electron window and vibrancy options.

Those six preferences are not emitted into Windows VS Code settings. Cursor keeps the previously inspected minimal profile; it does not inherit the VS Code Custom UI Style configuration.
The Mac renderer also adds an explicit Fish terminal profile: `/opt/homebrew/bin/fish` on Apple Silicon, `/usr/local/bin/fish` on Intel, or `macFishPath` for a custom prefix. FindItFaster keeps `/bin/bash` as its helper shell. The Fish change deliberately supersedes the older zsh value in the supplied snapshot.

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
The user has now supplied the MacBook's `code --list-extensions` output: **56 installed extension IDs**. That exact inventory is stored under `editorExtensions.vscode` in [`extensions.json`](../home/.chezmoidata/extensions.json), and is requested by both macOS and Windows VS Code installers. Cursor keeps its earlier 16-extension inventory under `editorExtensions.cursor`. Capture updates preserve the other editor's inventory and do not remove listed remote extensions.

The supplied inventory confirms VS Code Neovim, FindItFaster, lazygit, Custom UI Style, YAML, GitLens, Prettier, language support, and the other listed extensions. It includes Remote WSL but does not include Remote SSH; the installer requests the supplied IDs without adding Remote SSH. Extension packs can install additional dependencies.

The list records installed IDs, without versions or enabled/disabled states. Both `asvetliakov.vscode-neovim` and `vscodevim.vim` are present, as are APC, Vibrancy Continued, and Custom UI Style. Preserve any intentional disabling or enablement choices from the Mac when validating a fresh installation. No extension was disabled or removed based on its name or on an inferred conflict.
The settings also reference Copilot, Project Manager, Quickgrep, VS Code Pets, and AI Chat commands that are not present as explicit IDs in this export. Those settings remain preserved; extension installation is based on the supplied inventory.
Language and container extensions do not provision their external SDKs or a Docker runtime. Add those tools from a reviewed application/project inventory when needed.

[Custom UI Style](https://github.com/subframe7536/vscode-custom-ui-style#usage) applies CSS/Electron changes through its own backup and `Custom UI Style: Reload` commands. This bootstrap stores the preferences; it does not run those patching commands. Extension installation and editor startup on the actual Mac still need validation.

## Future captures

The automatic capture script still updates only its narrow allowlist. It now merges those captured preferences into the reviewed profile, preserving the full imported configuration and separate Mac overrides. Review additional settings manually before publishing them.

The remaining inputs are current keyboard shortcuts, any intended extension enablement states, the Mac's Neovim init/keymaps, personal Fish and app preferences, and any Mac-local T3 preferences that differ from the WSL-derived baseline. The user has confirmed macOS 27.0.1.
