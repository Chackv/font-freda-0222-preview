#!/usr/bin/env python3
"""Prueba determinista de distancias de edificios OSM a la ruta Sa Calobra.

La proyección equirectangular es suficiente para los primeros kilómetros y solo
sirve como prueba de regresión geométrica; no sustituye el motor 3D de Three.js.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAT0, LON0 = 39.85, 2.8
KX = 111195 * math.cos(math.radians(LAT0))
KY = 111195


def project(lon, lat):
    return (lon - LON0) * KX, (lat - LAT0) * KY


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_segment(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    den = dx * dx + dy * dy
    t = 0 if den < 1e-14 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / den))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def segment_gap(a, b, c, d):
    if cross(a, b, c) * cross(a, b, d) <= 0 and cross(c, d, a) * cross(c, d, b) <= 0:
        return 0.0
    return min(point_segment(a, c, d), point_segment(b, c, d), point_segment(c, a, b), point_segment(d, a, b))


def main():
    route = json.loads((ROOT / 'routes/sa-calobra.json').read_text())
    assert route['coords'][0][:2] == [2.7999, 39.850409], 'Se modificó el origen GPS de la ruta'
    pts = [project(lon, lat) for lon, lat, *_ in route['coords']]
    segments = [(a, b) for a, b in zip(pts, pts[1:]) if math.dist(a, b) > .05]
    osm = json.loads((ROOT / 'osm/sa-calobra.json').read_text())
    buildings = [p for p in osm if p['type'] == 'way' and p.get('tags', {}).get('building') not in (None, 'no') and len(p.get('geometry', [])) >= 4]
    distances = []
    for bld in buildings:
        poly = [project(point['lon'], point['lat']) for point in bld['geometry']]
        if poly[0] == poly[-1]:
            poly.pop()
        gap = math.inf
        for a, b in segments:
            for c, d in zip(poly, poly[1:] + poly[:1]):
                if max(a[0], b[0]) + 50 < min(c[0], d[0]) or min(a[0], b[0]) - 50 > max(c[0], d[0]):
                    continue
                if max(a[1], b[1]) + 50 < min(c[1], d[1]) or min(a[1], b[1]) - 50 > max(c[1], d[1]):
                    continue
                gap = min(gap, segment_gap(a, b, c, d))
        distances.append(gap)
    before = sum(d < 3.5 for d in distances)
    after = sum(d < 8.1 for d in distances)
    assert len(buildings) == 40, len(buildings)
    assert before == 1, f'Se esperaba 1 OSM footprint < 3,5 m: {before}'
    assert after == 9, f'Se esperaban 9 OSM footprints < 8,1 m: {after}'
    assert after < len(buildings) // 2, 'Filtro demasiado agresivo: afectaría al núcleo de edificios'
    patch = (ROOT / 'assets/index-fontfreda-0223-qa.js').read_text()
    assert 'e.id===`sa-calobra`?r+5:r+.4' in patch
    assert 'a>=8||t.nearest(c,l,120).index>=0' in patch
    print(f'OK: {len(buildings)} edificios OSM; perímetros cercanos <3,5m={before}, <8,1m={after}; resto preservado')


if __name__ == '__main__':
    main()
