# Paper Grid Generator

A free, web-based generator for **printable grid paper** — like [gridzzly.com](https://gridzzly.com), but with exact millimetre sizing, multiple paper sizes, configurable margins, and cut-tile support.

Everything is a single self-contained `index.html` — no build step, no dependencies, no server. Open the file in any browser.

## Features

- **Grid types:** dot grid, square, ruled lines, graph (major/minor), isometric, hexagonal, cross/plus, blank.
- **True-to-size printing:** grids are SVG dimensioned in real millimetres with a matching `@page` size, so a 2.5 mm dot grid prints as an actual 2.5 mm grid.
- **Crisp vector output:** dots are drawn as explicit vector circles (not pattern fills), so they stay razor-sharp in print/PDF instead of rasterizing to blocky squares.
- **Paper sizes:** A3, A4, A5, A6, A7, Letter, Legal, or custom W×H — portrait or landscape.
- **Configurable margins:** uniform or per-side (top/right/bottom/left), with an optional margin outline.
- **Cut tiles:** print one sheet and cut it into smaller pages. Pick a target size (e.g. A4 → 2× A6) or a custom rows×cols grid, with corner crop marks and optional per-tile margins.
- **Export:** print / save as PDF, or download the raw SVG (vector).

## Usage

Open `index.html` in a browser. Adjust the controls in the sidebar; the preview updates live.

When printing, for accurate physical sizes:

1. Set **Scale: 100%** (not "Fit to page").
2. Set **Margins: None**.

> The browser's on-screen *print preview* downsamples fine grids and can look noisy — the actual printed page and saved PDF are sharp vector.

## Deployment

Hosted as a static site on Dokku behind Cloudflare. See [DEPLOY.md](DEPLOY.md) for the full setup and deploy steps.

## License

MIT
