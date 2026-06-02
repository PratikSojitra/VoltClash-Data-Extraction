# Graph Report - coc-data  (2026-06-02)

## Corpus Check
- 13 files · ~114,820 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 351 nodes · 497 edges · 46 communities (42 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `deb8380f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 50|Community 50]]

## God Nodes (most connected - your core abstractions)
1. `levels` - 23 edges
2. `levels` - 22 edges
3. `levels` - 22 edges
4. `levels` - 22 edges
5. `levels` - 19 edges
6. `levels` - 19 edges
7. `levels` - 17 edges
8. `levels` - 17 edges
9. `main()` - 12 edges
10. `1` - 10 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `scrape_defense()`  [EXTRACTED]
  run.py → scrapers/update_defenses.py
- `main()` --calls--> `detect_changes()`  [EXTRACTED]
  run.py → utils/compare.py
- `main()` --calls--> `load_json()`  [EXTRACTED]
  run.py → utils/file_handler.py
- `main()` --calls--> `save_json()`  [EXTRACTED]
  run.py → utils/file_handler.py

## Import Cycles
- None detected.

## Communities (46 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (5): id, levels, defenses, Air Defense, last_updated

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 19

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (28): decompress_sc_csv(), extract_buildings(), extract_characters(), extract_heroes(), extract_pets(), extract_traps(), main(), make_time_str() (+20 more)

### Community 3 - "Community 3"
Cohesion: 0.22
Nodes (9): cost, dps, hitpoints, required_th, time, id, levels, Archer Tower (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 14

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 10

### Community 6 - "Community 6"
Cohesion: 0.22
Nodes (9): cost, dps, hitpoints, required_th, time, Mortar, 12, id (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 15

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 16

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 17

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (19): decompress_sc_csv(), extract_buildings(), extract_characters(), extract_equipment(), extract_heroes(), extract_pets(), extract_traps(), main() (+11 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (27): cost, dps, hitpoints, required_th, time, cost, dps, hitpoints (+19 more)

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 20

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 4

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 8

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 7

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 8

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (9): cost, dps, hitpoints, required_th, time, id, levels, Cannon (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 14

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 2

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 7

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 10

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 11

### Community 28 - "Community 28"
Cohesion: 0.40
Nodes (5): cost, dps, hitpoints, time, 0

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 13

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 18

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 5

### Community 33 - "Community 33"
Cohesion: 0.29
Nodes (7): cost, dps, hitpoints, required_th, time, levels, 12

### Community 34 - "Community 34"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 13

### Community 35 - "Community 35"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 15

### Community 36 - "Community 36"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 16

### Community 37 - "Community 37"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 17

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (7): cost, dps, hitpoints, required_th, time, 18, levels

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (7): cost, dps, hitpoints, required_th, time, levels, 19

### Community 40 - "Community 40"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 1

### Community 41 - "Community 41"
Cohesion: 0.29
Nodes (7): cost, dps, hitpoints, required_th, time, levels, 20

### Community 42 - "Community 42"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 21

### Community 43 - "Community 43"
Cohesion: 0.06
Nodes (31): cost, dps, hitpoints, required_th, time, cost, dps, hitpoints (+23 more)

### Community 47 - "Community 47"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 21

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (6): cost, dps, hitpoints, required_th, time, 9

## Knowledge Gaps
- **223 isolated node(s):** `BeforeTool`, `hitpoints`, `dps`, `cost`, `time` (+218 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `levels` connect `Community 3` to `Community 1`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 13`, `Community 47`, `Community 15`, `Community 16`, `Community 17`, `Community 28`, `Community 29`, `Community 30`, `Community 31`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `levels` connect `Community 17` to `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 13`, `Community 47`, `Community 15`, `Community 16`, `Community 29`, `Community 30`, `Community 31`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `levels` connect `Community 41` to `Community 33`, `Community 34`, `Community 35`, `Community 36`, `Community 37`, `Community 38`, `Community 39`, `Community 40`, `Community 42`, `Community 43`, `Community 14`, `Community 50`, `Community 23`, `Community 24`, `Community 25`, `Community 26`, `Community 27`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **What connects `BeforeTool`, `Decompresses a Supercell signed LZMA file.     - Strips the 68-byte cryptographi`, `Formats upgrade days, hours, minutes, and seconds into a clean human string.` to the rest of the system?**
  _246 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.10685483870967742 - nodes in this community are weakly interconnected._
- **Should `Community 11` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._
- **Should `Community 43` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._