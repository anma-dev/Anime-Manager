<img width="100%" alt="anime-manager-logo" src="https://user-images.githubusercontent.com/121255032/215242574-7ce5953f-38eb-4431-b716-db343a2cf401.png">

[![Linux](https://img.shields.io/badge/platform-Linux-blue)](https://img.shields.io/badge/platform-Linux-blue)  [![macOS](https://img.shields.io/badge/platform-macOS-blue)](https://img.shields.io/badge/platform-macOS-blue)  [![CodeFactor](https://www.codefactor.io/repository/github/anma-dev/anime-manager/badge/master)](https://www.codefactor.io/repository/github/anma-dev/anime-manager/overview/master)

Anime Manager is a powerful open source script that allows you to watch anime and synchronize your watch progress from your terminal.

<img src="https://user-images.githubusercontent.com/121255032/223771157-af6e2d04-e19b-4f0a-9fb5-54c0ca69ff89.jpeg" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/223768842-7ccab03e-0263-4474-8b7a-e4ef3ac3ae8e.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/223768860-54851be7-ebf2-40b7-9917-e66f4d5d4360.png" width="30%"></img> 

Anime Manager can synchronize your watch progress with your [anime cataloguing service](https://github.com/anma-dev/Anime-Manager/wiki#currently-supported-websites).

## Features ✨

- Integrated torrent client
- Integrated streaming client
- Integrated feed reader
- Integrated anime list sync
- Operations supported on lists: update anime status, add new anime, update episode count, set and update the score, delete anime from lists
- Quickly search your lists with fuzzy and literal match.
- Watch anime via streaming and torrenting
- Automatic update mode for updating your lists as you watch
- Play the next episode manually from the playback menu
- Playlist mode: automatically play the next episode when the video ends
- Playlist mode: watch multiple episodes in a row from the same or mixed anime
- Filter anime by score or airing status
- Play a random anime
- Watch history for quick access
- Select a new torrenting or streaming search result as you play
- Pick from matching files for batch torrents
- Bookmark magnet links for quickly resuming watch progress
- Incognito Mode

You need to configure Trackma with an account separately for using the Account mode, or you can use Incognito mode without an account.

> Note: Anime Manager is still unfinished software. Unexpected behavior and bugs will be encountered. We are actively working towards a stable release.

## Usage 🖥️

````text
Usage: anime-manager [options]...

Options:
  -a, --auto-update           Automatically update the lists when the playback time reaches
                              the threshold (80% of video duration).
  -m, --minimal               Minimalistic interface. It does not print the logo, the menu
                              fills the screen and is reversed. Dimmer colors.
  -i, --incognito             Switch Incognito Mode on. Your activity will not be synced
                              with the remote anime cataloguing service.
      --monochrome-logo       Print the monochromatic logo instead of the big orange one.
                              Suitable for terminals that do not support 24-bit colors.
  -t, --torrent-only          Always torrent the anime selection. Always load bookmark if
                              possible or automatically search the torrent tracker.
  -f, --downloads-folder TORRENT_DOWNLOADS_DIR
                              Full path for a persistent downloads folder for torrenting.
                              It is created if it does not exist.
  -p, --player MEDIA_PLAYER_APP
                              Select the media player. Defaults to mpv or iina (macOS)
                              Available players: iina, mpv, vlc.
  -d, --debug                 Start debug mode.
  -h, --help
  -v, --version
````

Some colored text requires that your terminal app supports 24-bit colors. You can check your terminal color support with a tool like [pastel colorcheck](https://github.com/sharkdp/pastel/blob/master/doc/colorcheck.md).

## Dependencies ✅

Python 3+, NodeJS >=14

| Dependency | Description |
| - | - |
| [animdl](https://github.com/justfoolingaround/animdl) | Scraping and streaming video links. |
| [anitopy](https://github.com/igorcmoura/anitopy/) | Parsing filenames |
| Compatible media player | The media player is automatically installed if necessary. Defaults: [mpv](https://mpv.io/) (Linux), [iina](https://iina.io/) (macOS). [VLC media player](https://www.videolan.org/) is also an option.|
| [fzf](https://github.com/junegunn/fzf/) | Terminal menus.  Get a recent version that supports border label and border label coloring. Some repos provide older versions of fzf. |
| [html2text](https://github.com/grobian/html2text) | "*HTML to text rendering aimed for E-mail*", but we use it for rendering the feed summaries that contain markdown. Make sure to install version 2.1.1 or later for link references support. |
| [jq](https://github.com/stedolan/jq) | Parse semi-structured data |
| [NyaaPy](https://github.com/JuanjoSalvador/NyaaPy/) | Scraping magnet links from the torrent tracker. |
| [Trackma](https://github.com/z411/trackma) | Anime list sync |
| [webtorrent-cli](https://github.com/anma-dev/webtorrent-cli) | Torrenting magnet links. We are using a fork that adds support for file selection, so it will only download what is being played. Included as a git submodule. |

Other dependencies assumed to be already installed and well known but listed here nonetheless: awk, cat, curl, grep, gunzip, netcat, ps, sed, timeout, wget.

Ensure all dependencies are available through your `$PATH`.

## Installation 🔨

### Linux and macOS

The script has an automatic install mode for dependencies that supports Ubuntu, Debian, and macOS. Automatic install respects your existing installation.

Clone the repo, initialize submodules, and then run the main script:

````text
$ git clone --recurse-submodules https://github.com/anma-dev/Anime-Manager.git Anime-Manager
$ cd Anime-Manager/
$ ./anime-manager
Anime Manager can automatically install its dependencies.
Some dependencies were not found!
### Anime Manager autoinstall ###
...
🎉 Finished the autoinstall!
Restart your shell to start using Anime Manager.
````

Then restart your terminal and run the main script again. You can also download compressed code for a version [here](https://github.com/anma-dev/Anime-Manager/tags). Tagged versions are more stable than master.

### Windows

The script probably works with some versions of WSL but we haven't tested it yet. Any help is welcome to add support for other platforms.

Once the installation is done it is recommended that you read the Wiki:

### [📖 Getting Started](https://github.com/anma-dev/Anime-Manager/wiki#getting-started)

## Support 💬

Suggestions are welcome. For guaranteed serious discussion use the Github issues tracker.

| [Matrix room](https://matrix.to/#/!VhiFZVwXObXapcpbQD:matrix.org?via=matrix.org) | [Email](mailto:anime-manager@proton.me) | [Github issues](https://github.com/anma-dev/Anime-Manager/issues) | [Github Wiki](https://github.com/anma-dev/Anime-Manager/wiki) |

## Say thanks

 It is not expected but you can send a short thank you note to the dev to let them know this project was helpful to you by clicking the badge below.

  [![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/anma-dev)

## Similar projects

You should also check these projects:

- [adl](https://github.com/RaitaroH/adl)
- [ani-cli](https://github.com/pystardust/ani-cli)
- [animdl](https://github.com/justfoolingaround/animdl)
- [eztrackma](https://github.com/justchokingaround/trackma-wrapper)
- [jerry](https://github.com/justchokingaround/jerry)
- [MALSync](https://github.com/MALSync/MALSync)
- [trackma](https://github.com/z411/trackma)

There's so many good projects to list them all here. [Check my starred repos](https://github.com/anma-dev?tab=stars).

---

> ALL BRAND OR PRODUCT NAMES USED HEREIN ARE TRADEMARKS OR REGISTERED TRADEMARKS OF THEIR RESPECTIVE COMPANIES OR ORGANIZATIONS.
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
