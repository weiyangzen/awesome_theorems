# THM-M-1252 validation-phase evidence

Item: `S56-M-1252-VALIDATION`. Base revision:
`6bcd5f977dc26298be5f77327a2616e726454eb7`.

The structured local recipe copied the dossier Lean modules into a temporary directory, built fresh
statement and obligation-tree oleans, elaborated the proof against those oleans, and separately
elaborated `Validation.lean`, which reconstructs the proposition directly from pinned mathlib. The
checked declarations report only `propext`, `Classical.choice`, and `Quot.sound`. Source scanning
found no placeholder, new axiom, or unsafe declaration. The validator also checked proof input
hashes, the frozen denominator, clean pinned mathlib revision, and the terminal anchor source hash.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1252` | 0 | rank 431; planned; theorem_complete false |
| `python3 Stage1_Instances/THM-M-1252/check_validation.py` | 0 | exact root, composition, and same-workspace reconstruction kernel-elaborated; trust, placeholder, hashes, denominator, pin, and provenance checks passed |

This is nonrelease warm-cache evidence. The first failed node gate is stale structured state:
`typed-graphs.json` predates proof closure and records `root_closed=false`. The section 10.6 cold
empty-cache hermetic gate also fails. Complete transitive TCB/SBOM evidence, offline restoration,
deterministic signed evidence, accepted H0/R0 review, and verification by a distinct identity in an
independently provisioned clean runner are absent. `audit_complete=false` and
`theorem_complete=false`; this receipt requests provisional worker acceptance only.
