#!/usr/bin/env python3
"""Hydrate template.html with a flow-graph spec -> a click-to-animate system-diagram artifact.

Usage: python3 generate.py spec.json out.html

The spec is authored by hand (see example-spec.json and SKILL.md for the method); this script is
purely mechanical: it renders the SVG nodes/paths/labels, injects the interaction tables into the
frozen behavior script, and LINTS the geometry — most importantly the "path routed through a box"
class of bug, which is invisible in code and glaring on screen. Stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

LANES = {"app", "broker", "worker", "target", "ok", "bad", "neutral"}
KINDS = {"flow", "ok", "bad", "warn"}
EDGE_TOLERANCE = 3  # px: a segment endpoint this close to a box edge counts as an attachment


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: generate.py spec.json out.html")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    template = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
    validate(spec)
    for warning in lint_geometry(spec):
        print(f"GEOMETRY: {warning}", file=sys.stderr)
    Path(sys.argv[2]).write_text(render(template, spec), encoding="utf-8")
    print(f"wrote {sys.argv[2]}")


def validate(spec: dict) -> None:
    node_ids = {node["id"] for node in spec["nodes"]}
    path_ids = {path["id"] for path in spec["paths"]}
    if len(node_ids) != len(spec["nodes"]) or len(path_ids) != len(spec["paths"]):
        sys.exit("duplicate node or path ids")
    for node in spec["nodes"]:
        if node.get("lane", "neutral") not in LANES:
            sys.exit(f"node {node['id']}: unknown lane {node.get('lane')!r} (use {sorted(LANES)})")
    for path in spec["paths"]:
        if path.get("kind", "flow") not in KINDS:
            sys.exit(f"path {path['id']}: unknown kind {path.get('kind')!r} (use {sorted(KINDS)})")
    for node_id, paths in spec["node_paths"].items():
        if node_id not in node_ids:
            sys.exit(f"node_paths references unknown node {node_id!r}")
        for path_id in paths:
            if path_id not in path_ids:
                sys.exit(f"node_paths[{node_id}] references unknown path {path_id!r}")
    for beat in spec.get("beats", []):
        if beat["node"] not in node_ids:
            sys.exit(f"beat references unknown node {beat['node']!r}")


def lint_geometry(spec: dict) -> list[str]:
    """Warn when a path segment crosses THROUGH a node box (attachment endpoints excluded)."""
    warnings = []
    boxes = {n["id"]: (n["x"], n["y"], n["x"] + n["w"], n["y"] + n["h"]) for n in spec["nodes"]}
    for path in spec["paths"]:
        for x1, y1, x2, y2 in segments_of(path["d"]):
            for node_id, (bx1, by1, bx2, by2) in boxes.items():
                if crosses_box(x1, y1, x2, y2, bx1, by1, bx2, by2):
                    warnings.append(
                        f"path {path['id']} segment ({x1},{y1})->({x2},{y2}) crosses node "
                        f"'{node_id}' — reroute through a clear lane"
                    )
    return warnings


def segments_of(d: str) -> list[tuple[float, float, float, float]]:
    """Parse an orthogonal path (absolute M/H/V only — the geometry style the skill mandates)."""
    tokens = re.findall(r"([MHV])\s*([-\d.,\s]+)", d)
    segments, x, y = [], 0.0, 0.0
    for command, args in tokens:
        values = [float(v) for v in re.split(r"[\s,]+", args.strip()) if v]
        if command == "M":
            x, y = values[0], values[1]
            extra = values[2:]
            while extra:  # implicit lineto pairs after M
                nx, ny = extra[0], extra[1]
                segments.append((x, y, nx, ny))
                x, y, extra = nx, ny, extra[2:]
        elif command == "H":
            for nx in values:
                segments.append((x, y, nx, y))
                x = nx
        elif command == "V":
            for ny in values:
                segments.append((x, y, x, ny))
                y = ny
    return segments


def crosses_box(x1, y1, x2, y2, bx1, by1, bx2, by2) -> bool:
    """True when an orthogonal segment passes through the box interior (not just touching an
    edge to attach): both endpoints outside-or-on-edge but the span overlaps the interior."""
    t = EDGE_TOLERANCE
    if x1 == x2:  # vertical
        if not (bx1 + t < x1 < bx2 - t):
            return False
        lo, hi = sorted((y1, y2))
        overlap_lo, overlap_hi = max(lo, by1 + t), min(hi, by2 - t)
        if overlap_lo >= overlap_hi:
            return False
        return not (abs(lo - by2) <= t or abs(hi - by1) <= t) or (lo < by1 - t and hi > by2 + t)
    if y1 == y2:  # horizontal
        if not (by1 + t < y1 < by2 - t):
            return False
        lo, hi = sorted((x1, x2))
        overlap_lo, overlap_hi = max(lo, bx1 + t), min(hi, bx2 - t)
        if overlap_lo >= overlap_hi:
            return False
        return not (abs(lo - bx2) <= t or abs(hi - bx1) <= t) or (lo < bx1 - t and hi > bx2 + t)
    return False


def render(template: str, spec: dict) -> str:
    defs = "\n".join(
        f'      <path id="{p["id"]}" d="{p["d"]}"/>' for p in spec["paths"]
    )
    uses = "\n".join(use_of(p) for p in spec["paths"])
    labels = "\n".join(label_of(p) for p in spec["paths"] if p.get("label"))
    groups = "\n".join(group_of(g) for g in spec.get("groups", []))
    nodes = "\n".join(node_of(n) for n in spec["nodes"])
    beats = beats_of(spec.get("beats", []))
    names = {n["id"]: n["name"] for n in spec["nodes"]}
    captions = {n["id"]: n.get("caption", "") for n in spec["nodes"] if n.get("caption")}
    dot_kind = {p["id"]: p["kind"] for p in spec["paths"] if p.get("kind", "flow") != "flow"}
    dot_kind = {k: ("warn" if v == "warn" else v) for k, v in dot_kind.items()}

    out = template
    for token, value in {
        "__TITLE__": escape(spec["title"]),
        "__EYEBROW__": spec["eyebrow"],
        "__HEADING__": spec["heading_html"],
        "__LEDE__": spec["lede_html"],
        "__ARIA__": escape(spec.get("aria", spec["title"])),
        "__CANVAS_W__": str(spec["canvas"]["width"]),
        "__CANVAS_H__": str(spec["canvas"]["height"]),
        "__DEFS_PATHS__": defs,
        "__USES__": uses,
        "__LABELS__": labels,
        "__GROUPS__": groups,
        "__NODES__": nodes,
        "__BEATS__": beats,
        "__EXTRAS__": spec.get("extras_html", ""),
        "__DEFAULT_CAPTION__": spec["default_caption"],
        "__JS_NODE_PATHS__": json.dumps(spec["node_paths"]),
        "__JS_DOT_KIND__": json.dumps(dot_kind),
        "__JS_NAMES__": json.dumps(names),
        "__JS_CAPTIONS__": json.dumps(captions),
        "__JS_PATH_IDS__": json.dumps([p["id"] for p in spec["paths"]]),
    }.items():
        out = out.replace(token, value)
    return out


def use_of(path: dict) -> str:
    kind = path.get("kind", "flow")
    classes = "flow" if kind == "flow" else f"flow {kind}"
    arrow = ' style="marker-end:url(#mFlow)"' if path.get("arrow", kind == "flow") else ""
    return f'    <use data-path="{path["id"]}" href="#{path["id"]}" class="{classes}"{arrow}/>'


def label_of(path: dict) -> str:
    label = path["label"]
    kind = path.get("kind", "flow")
    extra_class = {"ok": " okl", "bad": " badl"}.get(kind, "")
    rotate = label.get("rotate")
    transform = f' transform="rotate(90 {label["x"]} {label["y"]})"' if rotate else ""
    return (
        f'    <text class="plabel{extra_class}" data-path="{path["id"]}" '
        f'x="{label["x"]}" y="{label["y"]}"{transform}>{escape(label["text"])}</text>'
    )


def group_of(group: dict) -> str:
    return (
        f'    <g class="ghost"><rect x="{group["x"]}" y="{group["y"]}" width="{group["w"]}" '
        f'height="{group["h"]}" rx="10" stroke="var(--line)" fill="none" stroke-dasharray="4 4"/>'
        f'<text class="plabel" x="{group["label_x"]}" y="{group["label_y"]}">'
        f'{escape(group["label"])}</text></g>'
    )


def node_of(node: dict) -> str:
    lane = node.get("lane", "neutral")
    ghost = " ghost" if node.get("ghost") else ""
    small = " small" if node.get("small") else ""
    cx = node["x"] + node["w"] / 2
    name_y = node["y"] + (21 if node.get("small") else 23)
    ref_y = name_y + (16 if node.get("small") else 18)
    ref_line = (
        f'\n      <text class="ref" x="{cx:g}" y="{ref_y}" text-anchor="middle">'
        f'{escape(node["ref"])}</text>'
        if node.get("ref")
        else ""
    )
    return (
        f'    <g class="nodebox lane-{lane}{ghost}" data-node="{node["id"]}" tabindex="0" role="button">\n'
        f'      <rect x="{node["x"]}" y="{node["y"]}" width="{node["w"]}" height="{node["h"]}" rx="9"/>\n'
        f'      <text class="name{small}" x="{cx:g}" y="{name_y}" text-anchor="middle">'
        f'{escape(node["name"])}</text>{ref_line}</g>'
    )


def beats_of(beats: list) -> str:
    if not beats:
        return ""
    items = []
    for beat in beats:
        ok_class = ' class="okb"' if beat.get("ok") else ""
        items.append(f'    <li data-node="{beat["node"]}"{ok_class}>{beat["html"]}</li>')
    joined = "\n".join(items)
    return f'  <ol class="beats" id="beats">\n{joined}\n  </ol>'


if __name__ == "__main__":
    main()
