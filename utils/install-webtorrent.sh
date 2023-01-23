#!/bin/sh
# shellcheck disable=SC2016,SC2034

# enable node before checks
if [ -d "$HOME/.config/nvm" ]; then
    export NVM_DIR="$HOME/.config/nvm"
    # shellcheck disable=SC1091
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
    # shellcheck disable=SC1091
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion
    export NVM_DIR="$HOME/.nvm"
    nvm use node
fi
if ! command -v nvm; then
    if ! command -v node; then
        # neither nvm nor node are installed at this point
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
        export NVM_DIR="$HOME/.config/nvm"
        # shellcheck disable=SC1091
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
        # shellcheck disable=SC1091
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion
        export NVM_DIR="$HOME/.nvm"
        if ! grep 'export NVM_DIR="$HOME/.nvm"' "$HOME/.bash_profile"; then
            printf "%b" '
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"                   # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion
' >>"$HOME/.bash_profile"
        fi
        # ensure we are using the latest version
        nvm install node
        nvm use node
    else
        # respect the user installation
        node_v="$(node -v | awk -F"." '{print $1}' | sed 's,v,,g')"
        if [ "$node_v" -lt 14 ]; then
            # tell the user to upgrade manually
            printf "%s\n" "Please manually update your Node.js version to node>=14."
        fi
    fi
else
    # ensure we are using the latest version
    nvm install node
    nvm use node
fi
if [ ! -s lib/webtorrent-cli/bin/cmd.js ]; then
    git clone https://github.com/anma-dev/webtorrent-cli.git lib/webtorrent-cli
    cd lib/webtorrent-cli || exit
    npm i
    npm i --package-lock-only
    npm audit fix
    cd ../../
fi
