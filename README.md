# Anime Manager
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)  [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)

AM is a powerful open source (POSIX-compliant) script that lets you watch (stream + torrenting) and synchronize your anime lists from your terminal.

<img src="https://user-images.githubusercontent.com/121255032/212490696-8464044e-3402-48cb-8844-2835d86d8f47.jpeg" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490703-5fe79ab2-347e-4ecc-bff5-8d021cd67fc8.jpeg" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490758-22e6191b-8eb7-4ef7-9a23-862a769b5af0.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490717-40b20df0-c3f0-479f-a313-b5ca31d52f43.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490721-4b9fb71d-7291-4f2e-9b3e-6ecfb4434bba.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/121255032/212490727-571414ad-6817-45c3-bd57-0afbcf183448.png" width="30%"></img>

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

AM starts empty by default, with no account configured. You will have to configure Trackma with an account separately for AM to work properly. The script will walk you through that.

### Dependencies
Python 3+

| Dependency | Description |
| - | - |
| [animdl](https://github.com/justfoolingaround/animdl) | Scraping and streaming video links. |
| [bat](https://github.com/sharkdp/bat) | Pretty print anime synopses |
| [fzf](https://github.com/junegunn/fzf/) | User menus.  Get a recent version that supports border label and border label coloring. <br/>Some repos provide older versions of fzf. |
| [jq](https://github.com/stedolan/jq) | Parse semi-structured data |
| [Node.js](https://nodejs.org/en/) | Runs the Webtorrent process |
| [NyaaPy](https://github.com/JuanjoSalvador/NyaaPy/) | Scrapping magnet links from nyaa.si |
| [anitopy](https://github.com/igorcmoura/anitopy/) | Parsing filenames |
| [pastel](https://github.com/sharkdp/pastel) | Text with pretty colors |
| [Trackma](https://github.com/z411/trackma) | Anime list sync |

Ensure all dependencies binaries are available through your `$PATH`.

### Installation

The script has an automatic install mode for dependencies that supports macOS and Ubuntu. Automatic install respects your existing installation. AM needs testers to extend to other platforms.

Just clone the repo and give exec permissions to anime-manager and put anime-manager in path. Make sure the lib and utils folders are next to the main script.

### Usage
Run with

`$ anime-manager <arguments>`

We offer few options because the script is meant to be interacted with through the menus for most of the functionality.

#### Arguments

#### `--minimal`
Minimalistic interface. It doesn't print the logo, the menu fills the screen and is reversed. Dimmer colors.
#### `--monochrome-logo`
Print the monochromatic logo instead of the orange one, for terminals that do not support 24-bit colors. You can check your terminal color support with a tool like [pastel colorcheck](https://github.com/sharkdp/pastel/blob/master/doc/colorcheck.md), for example.

Currently, there is no holiday seasonal greeting for the monochromatic logo.

#### `-v`, `--version`
Print the version number and exit.

#### `-d`, `--debug`
Enable debug mode.

### Windows
The script probably works with some versions of WSL but no thorough testing was done to this date.

### Support
 
Issues and suggestions are welcome! I give free support and development for issues and features that personally interest me so I don't promise that I will implement "X" feature.

| [Matrix room](https://matrix.to/#/!VhiFZVwXObXapcpbQD:matrix.org?via=matrix.org) | [Discord](https://discord.gg/hqt7WSDP8J) | [Email](mailto:anime-manager@proton.me) | [Github issues](https://github.com) | [Github Wiki](https://github.com/anma-dev/Anime-Manager/wiki) |

For guaranteed serious discussion use the Github issues tracker.

### Say thanks
 It's not expected but you can send a small thank you note to the dev to let them know this project was helpful to you by clicking the badge below.

  [![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/anma-dev)

### Similar projects
You should also check these projects:
- [adl](https://github.com/RaitaroH/adl)
- [animdl](https://github.com/justfoolingaround/animdl)
- [ani-cli](https://github.com/pystardust/ani-cli)
- [trackma](https://github.com/z411/trackma)
- [MALSync](https://github.com/MALSync/MALSync)
- [jerry](https://github.com/justchokingaround/jerry)
- [eztrackma](https://github.com/justchokingaround/trackma-wrapper)

---

> ALL BRAND OR PRODUCT NAMES USED HEREIN ARE TRADEMARKS OR REGISTERED TRADEMARKS OF THEIR RESPECTIVE COMPANIES OR ORGANIZATIONS.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
