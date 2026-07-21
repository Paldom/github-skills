# README Templates: Library, CLI Tool, Web App

Three complete, copy-adapt README skeletons. Pick one, paste it, replace every
`<angle-bracket>` placeholder, then delete any section that does not apply —
never leave an empty stub heading in the final file.

## Contents

- [How to pick a template](#how-to-pick-a-template)
- [Rules that apply to every template](#rules-that-apply-to-every-template)
- [Template: library or package](#template-library-or-package)
- [Template: CLI tool](#template-cli-tool)
- [Template: web app](#template-web-app)
- [Hero and polish blocks](#hero-and-polish-blocks-copy-adapt)
- [Post-paste checklist](#post-paste-checklist)

## How to pick a template

| Project type | Pick when | Demo slot placement | Emphasize | De-emphasize |
|---|---|---|---|---|
| **Library / package** | Code others import (npm, PyPI, crate, gem, SDK) | Installation first; the demo is the smallest runnable code example right after it | Install one-liner, API surface, linked examples | Heavy visuals, roadmap prose |
| **CLI tool** | A binary or command users run in a terminal | Terminal GIF/screenshot near the top, before Installation | Copy-paste install, command table, exit codes | Web-app-style screenshots |
| **Web app** | A hosted or self-hosted application with a UI | Live demo link + screenshot at the top, before setup | Live demo, env-var setup, tech stack, deployment | Deep API reference (link out instead) |

## Rules that apply to every template

- **Top block is fixed**: H1 matching the repo name, a one-sentence value
  proposition, 3–4 badges, then the type-appropriate demo slot. A visitor must
  be able to answer "what is this, why should I care, how do I try it" within
  the first screen.
- **Badges**: cap at 3–5 trust signals (build, version, license, coverage).
  Use the GitHub Actions workflow badge pattern
  `https://github.com/<owner>/<repo>/actions/workflows/<workflow>.yml/badge.svg`
  and a static shields.io license badge. Skip decorative badges.
- **Headings are navigation**: GitHub auto-generates the README outline from
  headings, so keep them task-based ("Installation", "Usage", "API") — never
  vague ("More info"). Docs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- **Link out for depth**: full API reference, long guides, and process detail
  go to `docs/`, `examples/`, and community-health files (`CONTRIBUTING.md`,
  `SUPPORT.md`, `SECURITY.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE`). The
  README sections for these are one-to-two-line stubs that link to the file.
  GitHub truncates rendered READMEs beyond 500 KiB, and long single files scan
  poorly well before that limit.
- **Smallest success first**: every Usage/Quick-start section shows the
  minimal command or code that produces a visible result, plus one line
  stating the expected outcome.
- **Relative links**: use `../../discussions`, `../../issues`, `../../releases`
  so the README works in forks and clones without editing.
- **Tone**: second person, active voice, no hype adjectives. Prove claims with
  the demo, badges, and examples instead of asserting them.

## Template: library or package

````markdown
# <project-name>

<project-name> is a <category, e.g. "validation library"> for <audience> to <outcome> without <pain point>.

![CI](https://github.com/<owner>/<repo>/actions/workflows/<ci-workflow>.yml/badge.svg)
![Version](https://img.shields.io/badge/version-<x.y.z>-blue)
![License](https://img.shields.io/badge/license-<MIT>-green)

<!-- Optional demo slot: add ONE screenshot or GIF only if the library has visual output. Otherwise the Quick start below is the demo. -->

## Why <project-name>

- <benefit one — outcome, not feature, e.g. "Zero-config setup for <use case>">
- <benefit two>
- <benefit three — ecosystem fit, e.g. "Works with <framework/stack>">

## Installation

```bash
<package-manager install command, e.g. pip install <package>>
```

Other install methods: [docs/install.md](docs/install.md)

## Quick start

```<language>
<smallest useful example — must run as-is after the install above>
```

Expected result: <one line describing what the user sees>.

## API

Core entry points:

- `<primaryFunction(...)>` — <one-line purpose>
- `<secondaryFunction(...)>` — <one-line purpose>
- `<configObject>` — <one-line purpose>

Full reference: [docs/api.md](docs/api.md)

## Examples

- [Basic: <task>](examples/basic)
- [Advanced: <task>](examples/advanced)
- [Integration: <task>](examples/integration)

## Documentation

- [Getting started](docs/getting-started.md)
- [API reference](docs/api.md)
- [FAQ](docs/faq.md)

## Contributing

Contributions are welcome — read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## Support

Questions or ideas? Start a [Discussion](../../discussions) or see [SUPPORT.md](SUPPORT.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) or [Releases](../../releases).

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned work.

## License

Distributed under the <MIT> License. See [LICENSE](LICENSE).
````

## Template: CLI tool

````markdown
# <project-name>

A command-line tool for <audience> to <task> from the terminal.

![CI](https://github.com/<owner>/<repo>/actions/workflows/<ci-workflow>.yml/badge.svg)
![Version](https://img.shields.io/badge/version-<x.y.z>-blue)
![License](https://img.shields.io/badge/license-<MIT>-green)

![Terminal demo](docs/assets/<cli-demo>.gif)

## Installation

```bash
<recommended install command, e.g. brew install <tool>>
```

Other options:

- Prebuilt binaries: [Releases](../../releases)
- From source: [docs/install.md](docs/install.md)

## Usage

```bash
<tool> <most-common-subcommand> <typical-args>
```

Expected result: <one line describing the output>.

Run `<tool> --help` for all commands and flags.

## Quick examples

```bash
<tool> <example-1, e.g. init>
<tool> <example-2, e.g. sync ./data --remote prod>
<tool> <example-3, e.g. report --format json>
```

## Commands

| Command | What it does |
|---|---|
| `<init>` | <one-line purpose> |
| `<sync>` | <one-line purpose> |
| `<report>` | <one-line purpose> |
| `<config>` | <one-line purpose> |

Full command reference: [docs/commands.md](docs/commands.md)

## Configuration

- Config file: `<~/.config/tool/config>`
- Environment variables: `<TOOL_TOKEN>`, `<TOOL_ENV>`

Details: [docs/configuration.md](docs/configuration.md)

## Exit codes

- `0` — success
- `1` — <generic failure meaning>
- `2` — <invalid arguments / usage error>

## Documentation

- [Install guide](docs/install.md)
- [Command reference](docs/commands.md)
- [Examples](docs/examples.md)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Support

Questions? Start a [Discussion](../../discussions) or see [SUPPORT.md](SUPPORT.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) or [Releases](../../releases).

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned work.

## License

Distributed under the <MIT> License. See [LICENSE](LICENSE).
````

## Template: web app

````markdown
# <project-name>

<project-name> is a <category, e.g. "self-hosted dashboard"> for <audience> to <outcome>.

![CI](https://github.com/<owner>/<repo>/actions/workflows/<ci-workflow>.yml/badge.svg)
![License](https://img.shields.io/badge/license-<MIT>-green)
![Version](https://img.shields.io/badge/version-<x.y.z>-blue)

**Live demo:** [<app.example.com>](https://<app.example.com>) · **Docs:** [<docs.example.com>](https://<docs.example.com>)

![Screenshot of <main workflow>](docs/assets/<screenshot>.png)

## Features

- <feature one — user benefit phrasing>
- <feature two>
- <feature three>

## Tech stack

- Frontend: <framework>
- Backend: <framework / runtime>
- Data: <database / storage>
- Deployment: <platform / container>

## Getting started

### Prerequisites

- <runtime + version>
- <package manager>
- <database or external service>

### Installation

```bash
git clone https://github.com/<owner>/<repo>.git
cd <repo>
<install command>
```

### Environment

```bash
cp .env.example .env
```

Set the required variables (full list in [docs/configuration.md](docs/configuration.md)):

- `<APP_URL>`
- `<DATABASE_URL>`
- `<SECRET_KEY>`

### Run locally

```bash
<dev command>
```

Open `http://localhost:<port>` — you should see <expected first screen>.

## Usage

1. <step one, e.g. sign in or create an account>
2. <step two, e.g. create your first resource>
3. <step three, e.g. share or export the result>

## API

- [API reference](docs/api.md)
- [OpenAPI / interactive docs](https://<app.example.com>/docs)

## Deployment

See [docs/deployment.md](docs/deployment.md) for <platform> instructions.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Support

- Questions: [Discussions](../../discussions) or [SUPPORT.md](SUPPORT.md)
- Bugs: [Issues](../../issues)
- Vulnerabilities: [SECURITY.md](SECURITY.md)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) or [Releases](../../releases).

## Roadmap

See [ROADMAP.md](ROADMAP.md) or the [project board](<project-board-url>).

## License

Distributed under the <MIT> License. See [LICENSE](LICENSE).
````

## Hero and polish blocks (copy-adapt)

Markup patterns lifted from the best READMEs on GitHub (httpie, fiber,
thelounge, electron-markdownify, lobe-chat, size-limit, radioactive-state,
nerd-fonts, charmbracelet). All use GitHub's sanitized HTML subset — they
render on github.com, in forks, and in clones. Use them to upgrade a
template's top block; skip them for tiny utilities where a plain H1 reads
cleaner.

### The centered hero stack (the most-copied header on GitHub)

```html
<h1 align="center">
  <br>
  <a href="https://project-site"><img src="docs/assets/logo.png" alt="ProjectName" width="200"></a>
  <br>
  ProjectName
  <br>
</h1>

<h4 align="center">One-line value proposition, with one <a href="https://key-tech">key link</a>.</h4>

<p align="center">
  <a href="#quick-start">Quick start</a> •
  <a href="#features">Features</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#license">License</a>
</p>
```

Compact three-line variant (full app in a 95-line README):

```html
<h1 align="center"><img width="300" alt="ProjectName" src="docs/assets/logo.svg"></h1>
<h3 align="center">One-line value proposition</h3>
<p align="center"><strong>
  <a href="https://example.com/">Website</a> •
  <a href="https://example.com/docs">Docs</a> •
  <a href="https://demo.example.com/">Demo</a>
</strong></p>
```

### Dark/light adaptive images

The only reliable dark-mode mechanism — use it for the logo and any chart
whose colors break on one background:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
  <img height="125" alt="ProjectName" src="docs/assets/logo.svg">
</picture>
```

### Design-system badge strip

One shields style + one `labelColor` across every badge makes the row read as
brand. Keep the URL definitions in a link group at the file bottom:

```markdown
<p align="center">

[![][release-shield]][release-link] [![][ci-shield]][ci-link] [![][license-shield]][license-link]

</p>

<!-- LINK GROUP — keep at file bottom -->
[release-shield]: https://img.shields.io/github/v/release/OWNER/REPO?labelColor=black&style=flat-square&logo=github
[release-link]: ../../releases
[ci-shield]: https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?labelColor=black&style=flat-square
[ci-link]: ../../actions/workflows/ci.yml
[license-shield]: https://img.shields.io/badge/license-MIT-white?labelColor=black&style=flat-square
[license-link]: LICENSE
```

### Right-floated logo (zero-ceremony alternative)

```html
# ProjectName

<img src="docs/assets/logo.svg" align="right" alt="ProjectName logo" width="120">

ProjectName is a … (the intro paragraph wraps around the logo)
```

### Per-use-case collapsible recipes

The reader picks their scenario and sees ~15 lines instead of 200. The blank
line after `</summary>` is required for markdown to render inside:

```html
<details><summary><b>Using with Webpack</b></summary>

1. Install the plugin: `npm i -D tool-webpack`
2. Add it to `webpack.config.js`: …

</details>
```

### GIF-inside-summary example gallery

Collapsed examples that still show a moving preview:

```html
<details>
<summary><strong>Counter app</strong>
<p align="center"><img align="center" src="docs/assets/counter.gif" width="450" alt="Counter demo"></p>
</summary>

[Live demo](https://codesandbox.io/s/xxxx)

```jsx
const increment = () => state.count++;
```

</details>
```

### Persona router before multi-path sections

Route by the reader's situation before showing any path in full:

```markdown
_If you…_

- want the **quickest install**, run the one-liner below
- are on **macOS** with **Homebrew**, see [Homebrew](#homebrew)
- deploy with **Docker**, see [Docker](#docker)
```

### One-click deploy button (web apps)

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FOWNER%2FREPO&env=REQUIRED_KEY)
```

### Back-to-top links (long READMEs only)

```html
<a id="readme-top"></a>          <!-- first line of the README -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>   <!-- after long sections -->
```

Rules of use: pick the hero variant that matches the project's visual identity
(no logo → plain H1 or the emoji/text-only route); keep ONE style per README —
mixing centered-hero and floated-logo reads as patchwork; every nav-row link
must point at a section or site that exists.

## Post-paste checklist

Verify before committing:

- [ ] No `<angle-bracket>` placeholders remain (`grep -n '<[a-z]' README.md` and inspect hits)
- [ ] H1 matches the repository name; one-line value prop states audience + outcome
- [ ] 3–5 badges, all rendering (CI workflow file name in the badge URL exists)
- [ ] Demo slot filled per type: code example (library), terminal GIF (CLI), live link + screenshot (web app)
- [ ] Install commands verified on a clean environment; usage example produces the stated result
- [ ] Every linked file exists (`CONTRIBUTING.md`, `SUPPORT.md`, `CHANGELOG.md`, `LICENSE`, `docs/`, `examples/`) or the stub section is removed
- [ ] Stub sections stayed stubs — no process prose inlined into Contributing/Support/Changelog/Roadmap
- [ ] Sections that do not apply were deleted, not left empty
