---
name: flow-diagram-artifact
description: Build an interactive click-to-animate system/flow diagram artifact (SVG boxes + orthogonal flows, node selection with Ctrl multi-select, light/dark theming). Use when the user asks for a system design diagram, architecture walkthrough, animated code-flow page, or a visual "how does X flow through the system" artifact.
---

# Flow-diagram artifact

Produces the interactive system-diagram artifact style: a **calm, static, readable diagram** of
process boxes and orthogonal flow lines where **selecting a node animates that node's flows**
(marching dashes + traveling dots), Ctrl/⌘-click builds multi-node selections showing the union,
and a caption bar explains the selected step. Behavior, theming, and accessibility live in a
frozen template — you author only a JSON graph spec and hydrate it.

Files here: `template.html` (frozen behavior — do not fork lightly), `generate.py` (hydrator +
geometry linter), `example-spec.json` (a full worked example: a queue-worker RPA write path).

## The behavior contract (what the template guarantees — preserve it)

- **Calm default**: no motion until a node is selected. Solid neutral connectors; semantic paths
  (`ok` green, `bad` red, `warn` amber) colored but static.
- **Click a node** (or its beat card): that node's paths animate, everything else dims, the
  caption bar shows the node's caption. Click again or click empty space to release.
- **Ctrl/⌘-click** toggles nodes in/out of a multi-selection; the union of flows animates; the
  caption lists the selection. Ctrl-clicking empty space does NOT clear.
- Keyboard: nodes are tabbable, Enter/Space selects, Ctrl+Enter adds.
- **Theming**: light-first tokens, dark via `prefers-color-scheme`, the artifact viewer's
  `data-theme` toggle overrides both. NEVER hardcode palette hex in markup — node borders go
  through lane classes, path colors through kind classes.
- `prefers-reduced-motion`: selection still highlights, but no dashes march and no dots run.

## How to build the graph (the method)

**1. Content before geometry.** From the system you're documenting, write down: the process
boxes (≤ ~16 — merge internals rather than exceeding this), the edges with their SEMANTIC kind
(`flow` = normal, `ok` = success/commit, `bad` = failure/dead-letter, `warn` = retry/loop), the
happy-path order (becomes the numbered beats, ≤ 8), and for every node a one-sentence caption
a reader sees when they select it. Captions are where the text lives — the diagram itself stays
terse (name + one small mono ref line per box).

**2. Plan geometry on a grid.** Canvas ~1200×800. Assign each process/service a COLUMN and give
every column an explicit x-range; shared infrastructure (a database band) goes in a bottom strip
as a dashed `group` with small boxes inside. Rules that keep it clean:

- Orthogonal paths only — absolute `M`/`H`/`V` commands (`"M400,262 H480"`). The linter and the
  travel dots depend on this.
- Attach paths at box-edge midpoints; when several paths share an edge, offset them 8–14px.
- Reserve **clear vertical lanes** in the gaps between columns for long runs; NEVER route a
  segment through a box — `generate.py` lints this, take its warnings seriously (this is the #1
  recurring bug and it is invisible until rendered).
- Path labels are positioned manually (`label.x/y`, `rotate` for vertical runs): keep them off
  boxes, off other labels, and off group captions.
- Lanes color node borders: `app`, `broker`, `worker`, `target`, `ok`, `bad`, `neutral`
  (+ `ghost: true` for dashed secondary boxes, `small: true` for compact chip boxes).

**3. Write the spec** (shape = `example-spec.json`): `nodes` (id, x/y/w/h, lane, name, ref,
caption), `paths` (id, d, kind, optional label/arrow), `node_paths` (node id → the path ids that
animate when it's selected — include every edge that touches the node, both directions),
`groups`, `beats` (ordered happy path, `ok: true` for the final beat), `default_caption`,
header strings, and optional `extras_html` (e.g. a `.policy` call-out; `details` blocks for
code anchors).

**4. Hydrate**: `python3 <skill-dir>/generate.py spec.json out.html` — fix every GEOMETRY
warning it prints before proceeding.

**5. Verify with screenshots — never ship unrendered.** Wrap the output in
`<!doctype html><html><head><meta charset=utf-8></head><body>…</body></html>` as a preview file
and screenshot it with headless chromium (Playwright), then LOOK at every image:

- calm state, **light** color scheme (`emulate_media(color_scheme="light")`) — this is the
  artifact viewer's common default; near-white-on-white text means the theming broke;
- calm state, dark;
- a selected node (click one with the most edges) — check dimming, label legibility, dots;
- a Ctrl-click multi-selection.

Hunt specifically for: paths through boxes, labels colliding with badges/captions/boxes,
arrowheads ending inside text, truncated labels at box edges. Fix coordinates in the SPEC and
regenerate — don't hand-edit the output.

**6. Publish** via the Artifact tool (the file needs no doctype/head wrapper for publishing —
only the local preview does). Keep the same file path when updating so the URL is stable.

## Customizing beyond the spec

Small palette shifts (swap the token hex sets, keeping ALL FOUR blocks in sync: base, media-dark,
data-theme-light, data-theme-dark) and copy changes are fine. Changing the interaction script
means re-testing the whole behavior contract above — prefer not to.
