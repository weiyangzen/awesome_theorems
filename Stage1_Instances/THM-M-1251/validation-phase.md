# THM-M-1251 validation-phase evidence

Item: `S56-M-1251-VALIDATION`. Base revision:
`3175b20b2d6ae989a526ad94ae0ff0d20df1bc58`.

The local validator ran the structured recipe in `validation-spec.json`. It copied no dependency
artifacts, made no network requests, and did not mutate `.lake`. It elaborated the exact statement,
frozen child-to-parent composition, proof root, and an independently written local reconstruction
from temporary source paths using the existing pinned Lake environment. The checked declarations
reported only `propext`, `Classical.choice`, and `Quot.sound`; source scanning found no `sorry`,
`admit`, `sorryAx`, `axiom`, or `unsafe` declaration.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1251` | 0 | rank 171; planned; theorem_complete false |
| `python3 Stage1_Instances/THM-M-1251/check_validation.py` | 0 | exact root/composition/reconstruction elaborated; axiom, placeholder, input-hash, recipe, pin, and anchor checks passed; stale graph and release gates reported fail-closed |

This is nonrelease warm-cache evidence. The first failed node gate is stale authoritative structured
state: `typed-graphs.json` predates the proof receipt and still records `root_closed=false`. The
first release failure is the section 10.6 cold empty-cache hermetic gate. Complete transitive TCB
and supply-chain provenance, offline restoration, deterministic signed evidence, accepted H0/R0
reviews, and section 10.7 verification by a distinct identity in an independently provisioned clean
runner are absent. `Validation.lean` is only a same-workspace differential reconstruction. Thus
`audit_complete=false` and `theorem_complete=false`; the receipt requests only provisional worker
state pending master acceptance.
