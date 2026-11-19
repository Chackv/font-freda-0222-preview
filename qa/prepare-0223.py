#!/usr/bin/env python3
"""Genera una QA no publicada a partir de la r4, sin modificar sus activos."""
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'assets/index-fontfreda-0222-beta-r4.js'
dst=ROOT/'assets/index-fontfreda-0223-qa.js'
s=src.read_text()
changes={
  # En Mediterráneo no siempre existen mallas de vallas. Un add(...[]) llamaba add(undefined).
  'if(o&&a.add(...o.build()),u.length){': 'if(o){const built=o.build();if(built.length)a.add(...built)}if(u.length){',
  # Encuadre del ciclista en Seguimiento.
  'case`chase`:{let e=u(-6.5);f.set(e.x,e.y+2.25,e.z),p.set(d.x+d.fx*4,d.y+1.05,d.z+d.fz*4);break}':
  'case`chase`:{let e=u(-8.8);f.set(e.x,e.y+3.25,e.z),p.set(d.x+d.fx*1.4,d.y+1.22,d.z+d.fz*1.4);break}',
  # Dron menos alejado, conservando una altura suficiente respecto de los árboles.
  'case`drone`:{let e=u(-42,a+6);f.set(e.x,e.y+30,e.z);let t=u(22);p.set(t.x,t.y,t.z),m=1.4,h=2.5;break}':
  'case`drone`:{let e=u(-12,a);f.set(e.x,e.y+18,e.z);let t=u(3,a);p.set(t.x,t.y+1.0,t.z),m=2.0,h=3.5;break}',
  # Traducción de la descripción de salida.
  '`${t(e.length)} km with ${Math.round(e.gain)} m of climbing`':
  '`${t(e.length)} km · ${Math.round(e.gain)} m de desnivel positivo`',
  # No mostrar arco KOM de salida encima de la cámara durante los primeros metros.
  ',_(t.start,a,t.name.toUpperCase(),`START`),_(t.end':
  ',t.start>=30&&_(t.start,a,t.name.toUpperCase(),`START`),_(t.end',
  # Terminología de puertos en español.
  '${e.name} climb':'Subida a ${e.name}',
  # Banner de aproximación en rutas de montaña.
  '`${t(e.leadIn)} km easy lead-in from ${e.leadInFrom}, then ${t(e.length-e.leadIn)} km and ${Math.round(e.maxEle-vv(e,e.leadIn).ele)} m up`':
  '`${t(e.leadIn)} km de aproximación desde ${e.leadInFrom} · ascenso de ${t(e.length-e.leadIn)} km · ${Math.round(e.maxEle-vv(e,e.leadIn).ele)} m de subida`',
  # Marca inequívoca de la QA para no confundirla con la r4 estable.
  '02.2.2 BETA r4':'02.2.3 QA',
}
for a,b in changes.items():
    num=s.count(a)
    assert num== (2 if a=='02.2.2 BETA r4' else 1), f'Patrón ambiguo o ausente: {a[:60]} ({num})'
    s=s.replace(a,b)
dst.write_text(s)
for filename in ('index.html','404.html'):
    p=ROOT/filename
    html=p.read_text().replace('02.2.2 BETA r4 (audio + visual)','02.2.3 QA (no publicada)').replace('index-fontfreda-0222-beta-r4.js','index-fontfreda-0223-qa.js')
    assert '0223-qa.js' in html
    p.write_text(html)
# El motor de audio se conserva byte a byte en la QA.
base=src.read_text()
def engine(t):
  start=t.index('pw=class{')+3
  end=t.index('},mw=',start)+1
  return t[start:end]
assert engine(base)==engine(s), 'Se ha cambiado accidentalmente el motor de audio'
assert sha256(src.read_bytes()).hexdigest()==sha256(base.encode()).hexdigest()
print('QA preparada',dst, 'bytes=',dst.stat().st_size,'audio sin cambios')
