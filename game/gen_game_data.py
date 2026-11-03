#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从知识库生成游戏数据：data/nodes.json + data/edges.json + game/items.json → game/game_data.json
知识库更新后重跑本脚本，游戏数据随之更新；有节点没配题的会在输出里标 missing_items，提醒补题。
当前关卡链：数学七上第一章（qd-m7a-101…109），根节点为两个小学先修（P1、P2）。"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(BASE)
nodes = {n["id"]: n for n in json.load(open(os.path.join(KB, "data", "nodes.json")))}
edges = json.load(open(os.path.join(KB, "data", "edges.json")))
items = json.load(open(os.path.join(BASE, "items.json")))

CHAIN = ["qd-m7a-P1", "qd-m7a-P2", "qd-m7a-101", "qd-m7a-102", "qd-m7a-103", "qd-m7a-104",
         "qd-m7a-105", "qd-m7a-106", "qd-m7a-107", "qd-m7a-108", "qd-m7a-109"]
pre = {}
for e in edges:
    if e["to"] in CHAIN and e["from"] in CHAIN:
        pre.setdefault(e["to"], []).append({"id": e["from"], "strength": e["strength"]})

out, missing = [], []
for nid in CHAIN:
    n = nodes[nid]
    it = items.get(nid)
    if not it:
        missing.append(nid)
    out.append({
        "id": nid, "name": n["name"], "loc": n["loc"], "subject": n["subject"],
        "definition": n.get("definition", ""), "root_note": n.get("root_note", ""),
        "status": n["status"], "prereq": pre.get(nid, []), "items": it or {},
    })

data = {"title": "回溯大冒险 · 有理数岛", "chapter": "数学（青岛版）七上 第一章 有理数",
        "levels": out, "missing_items": missing,
        "kb_source": "knowledge-base/data/nodes.json + edges.json + game/items.json"}
json.dump(data, open(os.path.join(BASE, "game_data.json"), "w"), ensure_ascii=False, indent=1)
print("关卡数:", len(out), "| 缺题节点:", missing or "无")
