#!/usr/bin/env bash

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

if [[ ! -d lib/webtorrent-cli ]]; then
    git clone https://github.com/anma-dev/webtorrent-cli.git lib/webtorrent-cli
    cd lib/webtorrent-cli || exit
    npm i
    npm i --package-lock-only
    npm audit fix
    cd ../../
fi
