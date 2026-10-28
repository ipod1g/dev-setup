# PATH support only; personal config.fish, functions, and plugins stay separate.
if test (uname) != Darwin
    return
end

set -l dev_setup_brew
if command -q brew
    set dev_setup_brew (command -s brew)
else if test -x /opt/homebrew/bin/brew
    set dev_setup_brew /opt/homebrew/bin/brew
else if test -x /usr/local/bin/brew
    set dev_setup_brew /usr/local/bin/brew
end

if test -n "$dev_setup_brew"
    $dev_setup_brew shellenv fish | source
    set -l dev_setup_prefix
    if set -q HOMEBREW_PREFIX
        set dev_setup_prefix $HOMEBREW_PREFIX
    else
        set dev_setup_prefix ($dev_setup_brew --prefix)
    end
    if test -n "$dev_setup_prefix"
        fish_add_path --path "$dev_setup_prefix/opt/node@24/bin"
    end
end
fish_add_path --path "$HOME/.local/bin"
