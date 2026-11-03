#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自家版初中知识库 · 查询脚本（纯标准库）
用法：
  python3 kb.py stats              全库统计
  python3 kb.py list [科目]        列节点（科目：数学/语文/英语，可省略）
  python3 kb.py show <节点id>      看单个节点全字段
  python3 kb.py back <节点id>      回溯链：这个点错了，往回查哪些先修（默认只走硬边；加 --all 含软边）
  python3 kb.py search <关键词>    按名字/落点搜节点
"""
import json, os, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
NODES = json.load(open(os.path.join(BASE, "nodes.json")))
EDGES = json.load(open(os.path.join(BASE, "edges.json")))
BYID = {n["id"]: n for n in NODES}
PRE = {}
for e in EDGES:
    PRE.setdefault(e["to"], []).append(e)

def stats():
    import collections
    print("节点总数:", len(NODES), dict(collections.Counter(n["subject"] for n in NODES)))
    print("状态:", dict(collections.Counter(n["status"] for n in NODES)))
    print("先修边:", len(EDGES), "（硬", sum(1 for e in EDGES if e["strength"] == "硬"),
          "／软", sum(1 for e in EDGES if e["strength"] == "软"), "）")

def lst(subj=None):
    for n in NODES:
        if subj and n["subject"] != subj:
            continue
        print(f'{n["id"]:<16} {n["subject"]} {n["name"]}  [{n["loc"]}] <{n["status"]}>')

def show(nid):
    n = BYID.get(nid)
    if not n:
        print("没有这个节点:", nid); return
    for k in ("id", "subject", "name", "loc", "type", "level", "status", "source",
              "definition", "mastery", "diagnostic", "root_note", "tier", "part_of"):
        if n.get(k):
            print(f"{k}: {n[k]}")
    pre = PRE.get(nid, [])
    if pre:
        print("先修:", "；".join(f'{p["from"]}({BYID.get(p["from"], {}).get("name", "?")},{p["strength"]})' for p in pre))

def back(nid, hard_only=True, depth=0, seen=None):
    seen = seen or set()
    n = BYID.get(nid)
    if not n:
        print("没有这个节点:", nid); return
    print("  " * depth + f'{nid} {n["name"]}')
    if nid in seen:
        return
    seen.add(nid)
    for e in PRE.get(nid, []):
        if hard_only and e["strength"] != "硬":
            continue
        back(e["from"], hard_only, depth + 1, seen)

def search(kw):
    hits = [n for n in NODES if kw in n["name"] or kw in n.get("loc", "") or kw in n.get("definition", "")]
    for n in hits:
        print(f'{n["id"]:<16} {n["subject"]} {n["name"]}  [{n["loc"]}]')
    print("共", len(hits), "条")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "stats":
        stats()
    elif a[0] == "list":
        lst(a[1] if len(a) > 1 else None)
    elif a[0] == "show":
        show(a[1])
    elif a[0] == "back":
        back(a[1], hard_only="--all" not in a)
    elif a[0] == "search":
        search(a[1])
    else:
        print(__doc__)
