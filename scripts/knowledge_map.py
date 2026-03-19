#!/usr/bin/env python3
"""Generate an interactive knowledge map visualization.

Usage:
    python knowledge_map.py --concepts '[{"id":"c1","label":"React Hooks","retrievability":0.85,"stability":12.5},...]' --edges '[{"a":"c1","b":"c2","type":"prereq","weight":0.7},...]' --output /tmp/cognition-map.html
"""

import argparse
import json
import webbrowser
from pathlib import Path


def generate_map_html(concepts: list[dict], edges: list[dict]) -> str:
    concepts_json = json.dumps(concepts)
    edges_json = json.dumps(edges)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Knowledge Map — Cognition</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, sans-serif; background: #0f0f23; color: #e0e0e0; height: 100vh; overflow: hidden; }}
  svg {{ width: 100%; height: 100%; }}
  .node circle {{ stroke-width: 2px; cursor: pointer; }}
  .node text {{ font-size: 11px; fill: #ccc; pointer-events: none; }}
  .link {{ stroke-opacity: 0.4; }}
  .tooltip {{ position: absolute; background: #1a1a3e; border: 1px solid #3d3d6c; border-radius: 8px; padding: 12px 16px; font-size: 13px; pointer-events: none; display: none; max-width: 250px; }}
  .tooltip .label {{ font-weight: 600; color: #fff; margin-bottom: 4px; }}
  .tooltip .stat {{ color: #aaa; margin: 2px 0; }}
  .legend {{ position: absolute; bottom: 20px; left: 20px; background: #1a1a3e; border: 1px solid #3d3d6c; border-radius: 8px; padding: 16px; font-size: 12px; }}
  .legend-item {{ display: flex; align-items: center; gap: 8px; margin: 4px 0; }}
  .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
</style>
</head>
<body>
<svg id="graph"></svg>
<div class="tooltip" id="tooltip"></div>
<div class="legend">
  <div style="font-weight:600;margin-bottom:8px">Recall Strength</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div> Critical (&lt;40%)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div> At Risk (40-70%)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div> Strong (&gt;70%)</div>
</div>
<script>
const concepts = {concepts_json};
const edges = {edges_json};
const W = window.innerWidth, H = window.innerHeight;
const svg = document.getElementById('graph');
svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);
const tooltip = document.getElementById('tooltip');

function color(r) {{ return r < 0.4 ? '#ef4444' : r < 0.7 ? '#f59e0b' : '#22c55e'; }}
function radius(s) {{ return Math.max(8, Math.min(30, 6 + s * 0.8)); }}

const nodes = concepts.map((c, i) => ({{
  ...c, x: W/2 + (Math.random()-0.5)*400, y: H/2 + (Math.random()-0.5)*400,
  vx: 0, vy: 0, r: radius(c.stability || 5)
}}));
const idMap = Object.fromEntries(nodes.map((n,i) => [n.id, i]));
const links = edges.filter(e => idMap[e.a] !== undefined && idMap[e.b] !== undefined);

// Draw edges
links.forEach(e => {{
  const line = document.createElementNS('http://www.w3.org/2000/svg','line');
  line.classList.add('link');
  line.dataset.a = e.a; line.dataset.b = e.b;
  line.setAttribute('stroke', '#4a4a7a');
  line.setAttribute('stroke-width', Math.max(1, (e.weight||0.5)*3));
  svg.appendChild(line);
}});

// Draw nodes
nodes.forEach(n => {{
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.classList.add('node');
  const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
  c.setAttribute('r', n.r);
  c.setAttribute('fill', color(n.retrievability || 0.5));
  c.setAttribute('stroke', color(n.retrievability || 0.5));
  c.dataset.id = n.id;
  g.appendChild(c);
  const t = document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('dy', n.r + 14);
  t.setAttribute('text-anchor', 'middle');
  t.textContent = n.label;
  g.appendChild(t);
  g.addEventListener('mouseenter', ev => {{
    tooltip.style.display = 'block';
    tooltip.style.left = (ev.pageX+10)+'px';
    tooltip.style.top = (ev.pageY+10)+'px';
    tooltip.innerHTML = `<div class="label">${{n.label}}</div>
      <div class="stat">Recall: ${{Math.round((n.retrievability||0)*100)}}%</div>
      <div class="stat">Stability: ${{(n.stability||0).toFixed(1)}} days</div>
      <div class="stat">Difficulty: ${{(n.difficulty||0).toFixed(2)}}</div>
      <div class="stat">Reviews: ${{n.review_count||0}}</div>`;
  }});
  g.addEventListener('mouseleave', () => {{ tooltip.style.display = 'none'; }});
  svg.appendChild(g);
  n.el = g;
}});

// Simple force simulation
function tick() {{
  nodes.forEach((a,i) => {{
    nodes.forEach((b,j) => {{
      if (i >= j) return;
      let dx = a.x-b.x, dy = a.y-b.y;
      let d = Math.sqrt(dx*dx+dy*dy) || 1;
      let f = 800 / (d*d);
      a.vx += dx/d*f; a.vy += dy/d*f;
      b.vx -= dx/d*f; b.vy -= dy/d*f;
    }});
  }});
  links.forEach(e => {{
    const a = nodes[idMap[e.a]], b = nodes[idMap[e.b]];
    if (!a || !b) return;
    let dx = b.x-a.x, dy = b.y-a.y;
    let d = Math.sqrt(dx*dx+dy*dy) || 1;
    let f = (d - 120) * 0.02;
    a.vx += dx/d*f; a.vy += dy/d*f;
    b.vx -= dx/d*f; b.vy -= dy/d*f;
  }});
  nodes.forEach(n => {{
    n.vx += (W/2-n.x)*0.001; n.vy += (H/2-n.y)*0.001;
    n.vx *= 0.9; n.vy *= 0.9;
    n.x += n.vx; n.y += n.vy;
    n.x = Math.max(n.r, Math.min(W-n.r, n.x));
    n.y = Math.max(n.r, Math.min(H-n.r, n.y));
    n.el.setAttribute('transform', `translate(${{n.x}},${{n.y}})`);
  }});
  svg.querySelectorAll('.link').forEach(l => {{
    const a = nodes[idMap[l.dataset.a]], b = nodes[idMap[l.dataset.b]];
    if(a&&b){{ l.setAttribute('x1',a.x);l.setAttribute('y1',a.y);l.setAttribute('x2',b.x);l.setAttribute('y2',b.y); }}
  }});
  requestAnimationFrame(tick);
}}
tick();
</script>
</body>
</html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--concepts', required=True)
    parser.add_argument('--edges', default='[]')
    parser.add_argument('--output', default='/tmp/cognition-map.html')
    args = parser.parse_args()
    html = generate_map_html(json.loads(args.concepts), json.loads(args.edges))
    out = Path(args.output)
    out.write_text(html, encoding='utf-8')
    print(f'Knowledge map generated: {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
