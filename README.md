<img width="100%" alt="anime-manager-logo" src="https://user-images.githubusercontent.com/121255032/212677776-ec5aba1b-fab0-466c-b037-c30a116558a3.png">

[![Linux](https://img.shields.io/badge/os-Linux-blue)](https://img.shields.io/badge/os-Linux-blue)  [![macOS](https://img.shields.io/badge/os-macOS-blue)](https://img.shields.io/badge/os-macOS-blue)  [![CodeFactor](https://www.codefactor.io/repository/github/anma-dev/anime-manager/badge/master)](https://www.codefactor.io/repository/github/anma-dev/anime-manager/overview/master)

Anime Manager is a powerful open source script that lets you watch (streaming + torrenting) anime and synchronize (Trackma) your progress from your terminal.

<img src="https://user-images.githubusercontent.com/121255032/212490696-8464044e-3402-48cb-8844-2835d86d8f47.jpeg" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490703-5fe79ab2-347e-4ecc-bff5-8d021cd67fc8.jpeg" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490758-22e6191b-8eb7-4ef7-9a23-862a769b5af0.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490717-40b20df0-c3f0-479f-a313-b5ca31d52f43.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490721-4b9fb71d-7291-4f2e-9b3e-6ecfb4434bba.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490727-571414ad-6817-45c3-bd57-0afbcf183448.png" width="30%"></img>

You can use your existing anime list service (those [trackma supports](https://github.com/z411/trackma#currently-supported-websites)) to synchronize your progress as you watch, all from one utility for added convenience!

## Features

- 🔄 **Set anime as completed or (re)watching as you go.**
- ✅ **Set the current episode as watched and play the next one**
- ↔️ **Move anime between lists**
- 📣 **Filter anime by score or airing status**
- 🔀 **Play a random episode**
- 👁️ **Watch history for quick access**
- 👍 **Score your anime**

and even MORE...

- 💡 **Switch between torrenting and streaming as you play**
- 👉 **Select a new torrenting or streaming source as you play**
- 🗃️ **Pick from matching files for batch torrents**
- 🕵️ **Incognito Mode**

It integrates the following functionality and tools:

- List sync ([trackma](https://github.com/z411/trackma))
- Episode search and streaming ([animdl](https://github.com/justfoolingaround/animdl))
- Episode search and torrenting ([NyaaPy](https://github.com/JuanjoSalvador/NyaaPy/) + [(patched) webtorrent-cli](https://github.com/anma-dev/webtorrent-cli))
- Beautiful menus ([fzf](https://github.com/junegunn/fzf/))

AM starts empty by default, with no account configured. You will have to configure Trackma with an account separately for AM to work properly. The script will walk you through that.

## Usage

````text
Usage: anime-manager [options]...

Options:
      --minimal               Minimalistic interface. It does not print the logo, the menu
                              fills the screen and is reversed. Dimmer colors.
  -i, --incognito             Switch Incognito Mode on. Your activity will not be synced
                              with the remote anime list tracking service.
      --monochrome-logo       Print the monochromatic logo instead of the big orange one.
                              Suitable for terminals that do not support 24-bit colors.
  -d, --debug                 Start debug mode
  -h, --help
  -v, --version
````

The big orange logo requires that your terminal app supports 24-bit colors. You can check your terminal color support with a tool like [pastel colorcheck](https://github.com/sharkdp/pastel/blob/master/doc/colorcheck.md).

## Dependencies

Python 3+, NodeJS >=14

| Dependency | Description |
| - | - |
| [animdl](https://github.com/justfoolingaround/animdl) | Scraping and streaming video links. |
| [anitopy](https://github.com/igorcmoura/anitopy/) | Parsing filenames |
| [bat](https://github.com/sharkdp/bat) | Pretty print anime synopses |
| [fzf](https://github.com/junegunn/fzf/) | User menus.  Get a recent version that supports border label and border label coloring. <br/>Some repos provide older versions of fzf. |
| [jq](https://github.com/stedolan/jq) | Parse semi-structured data |
| [webtorrent-cli](https://github.com/anma-dev/webtorrent-cli) | Torrenting magnet links |
| [NyaaPy](https://github.com/JuanjoSalvador/NyaaPy/) | Scraping magnet links from nyaa.si |
| [Trackma](https://github.com/z411/trackma) | Anime list sync |

Other dependencies: awk, cat, curl, grep, iina (macOS), mpv, sed, wget.

Ensure all dependencies binaries are available through your `$PATH`.

## Installation

### Linux and macOS

The script has an automatic install mode for dependencies that supports Ubuntu, Debian, and macOS. Automatic install respects your existing installation.

Clone the repo and give executable permissions to `anime-manager` and everything under `utils/` folder, and put anime-manager in your `PATH`. Make sure the `lib` and `utils` folders are right next to the main script. We will provide more information once the first release is published.

### Windows

The script probably works with some versions of WSL but we haven't tested it yet. AM needs testers to expand to other platforms.

## Support
 
Issues and suggestions are welcome! For guaranteed serious discussion use the Github issues tracker.

| [Matrix room](https://matrix.to/#/!VhiFZVwXObXapcpbQD:matrix.org?via=matrix.org) | [Email](mailto:anime-manager@proton.me) | [Github issues](https://github.com/anma-dev/Anime-Manager/issues) | [Github Wiki](https://github.com/anma-dev/Anime-Manager/wiki) |

## Say thanks

 It's not expected but you can send a small thank you note to the dev to let them know this project was helpful to you by clicking the badge below.

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

---

> ALL BRAND OR PRODUCT NAMES USED HEREIN ARE TRADEMARKS OR REGISTERED TRADEMARKS OF THEIR RESPECTIVE COMPANIES OR ORGANIZATIONS.
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
