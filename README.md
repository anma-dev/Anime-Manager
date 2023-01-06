# ~ anime-manager

anime-manager is a powerful open source script that lets you watch (stream + torrenting) and synchronize your anime lists from your terminal.

You can use your existing anime list service (those [trackma supports](https://github.com/z411/trackma#currently-supported-websites)) to synchronize your lists as you watch anime by streaming or torrenting, all from one utility for added convenience!

- 🔄 Set series as completed or (re)watching as you go.
- ✅ Set the current episode as watched and play the next one
- ↔️ Move series between lists
- 📣 Filter series by score or airing status
- 🔀 Play a random episode
- 👁️ Watch history for quick access
- 👍 Rate your series

and even more...
- 💡 Switch between torrenting and streaming as you play
- 👉 Select a new torrenting or streaming source as you play
- 🗃️ Pick from matching files for batch torrents

It integrates the following functionality and tools:
- List sync ([trackma](https://github.com/z411/trackma))
- Episode search and streaming ([animdl](https://github.com/justfoolingaround/animdl))
- Episode search and torrenting ([NyaaPy](https://github.com/JuanjoSalvador/NyaaPy/) + [(patched) webtorrent-cli](https://github.com/anma-dev/webtorrent-cli))
- Beautiful menus ([fzf](https://github.com/junegunn/fzf/))

AM starts empty by default, with no account configured. You will have to configure Trackma with a acocunt separately for AM to work properly. The script will walk you through that.

### Dependencies
Python 3+ and modern bash or zsh.

| Dependency | Description |
| - | - |
| [animdl](https://github.com/justfoolingaround/animdl) | Scrapping and streaming video links. |
| [bat](https://github.com/sharkdp/bat) | Pretty print anime synopses |
| [fzf](https://github.com/junegunn/fzf/) | User menus |
| [jq](https://github.com/stedolan/jq) | Parse semi-structured data |
| [Node.js](https://nodejs.org/en/) | Runs the Webtorrent process |
| [NyaaPy](https://github.com/JuanjoSalvador/NyaaPy/) | Scrapping magnet links from nyaa.si |
| [pastel](https://github.com/sharkdp/pastel) | Text with pretty colors |
| [Trackma](https://github.com/z411/trackma) | Anime list sync |

Ensure all dependencies binaries are available through your `$PATH`.

### Installation

The script has an automatic install mode for dependencies that supports macOS and Ubuntu. Automatic install respects your existing installation. AM needs testers to extend to other platforms.
````
sudo curl -sL https://github.com/anma-dev/anime-manager/raw/main/anime-manager -o /usr/local/bin/anime-manager
sudo chmod +x /usr/local/bin/anime-manager
````
Run the script to accept the terms and begin automatic installation of dependencies if your platform is supported.

### Usage
Run with

`$ anime-manager <arguments>`

We offer few options because the script is meant to be interacted with through the menus for most of the functionality.

#### Arguments

#### `-d`, `--debug`
Don't print the logo and enable debug mode.
#### `--small-logo`
Don't print the big, orange logo, print the small yellow one instead.
The default big logo includes some fun greetings for holiday seasons. Recommended!
#### `-v`, `--version`
Print the version number and exit.

### Support
Issues and suggestions are welcome! I give free support and development for issues and features that personally interest me so I don't promise that I will implement "X" feature.
| [Matrix room](https://matrix.to/#/!VhiFZVwXObXapcpbQD:matrix.org?via=matrix.org) | [Discord](https://discord.gg/hqt7WSDP8J) | [Email](email:anime-manager@proton.me) | [Github issues](https://github.com) | [Github Wiki](https://github.com/anma-dev/Anime-Manager/wiki) |

The Discord server is more of a fun chill place than technical support but use whatever floats your boat. For guaranteed serious discussion use the Github issues tracker.
