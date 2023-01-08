#!/bin/sh

if ! which nvm; then
    if ! which node; then
        # neither nvm nor node are installed at this point
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"                   # This loads nvm
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion

        if ! grep 'export NVM_DIR="$HOME/.nvm"' "$HOME/.bash_profile"; then
            printf "%b" '
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"                   # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion
' >>"$HOME/.bash_profile"
        fi
        # install node with nvm
        # ensure we are using the latest version
        nvm install node
        nvm use node
    else
        # respect the user installation
        node_v="$(node -v | awk -F"." '{print $1}' | sed 's,v,,g')"
        if [ "$node_v" -lt 14 ]; then
            # tell the user to upgrade manually
            install_dep_msg="🎉 Finished the autoinstall!\nNEXT STEPS: manually update your Node.js version to node>=14 and restart your Terminal to start using Anime Manager."
        fi
    fi
else
    # ensure we are using the latest version
    nvm install node
    nvm use node
fi
if [ ! -d lib/webtorrent-cli ]; then
    git clone https://github.com/anma-dev/webtorrent-cli.git lib/webtorrent-cli
    cd lib/webtorrent-cli || exit
    npm i
    npm i --package-lock-only
    npm audit fix
    cd ../../
fi
