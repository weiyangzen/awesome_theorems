# Obligation-tree validation receipt

Item: `S56-M-1131-OBLIGATION_TREE`  
Base revision: `1f5104f9436b89dd301e48be5dcc8b9c16a07b26`  
Validation date: 2026-07-12 (Asia/Shanghai)

The registry contains 14 canonical obligations with denominator SHA-256
`48b6c9204c77135055dfc3e3e709fabf64531a5e71c08bff2fb583ef99b326d6`. The graph bundle has
32 typed edges across separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. The checked Lean declarations are conditional composition certificates only.

Commands ran in this worker clone. Lean used the existing pinned Lake environment. The temporary
`Statement.olean` was written under `/tmp`; no dependency update, build, clone, fetch, or install ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1131/build_obligation_artifacts.py` | 0 | generated registry, graphs, and 14 validation recipes; denominator printed |
| `python3 Stage1_Instances/THM-M-1131/check_obligation_tree.py` | 0 | deterministic regeneration, required node fields, hashes, reciprocal proof edges, and open-root boundary passed |
| three scoped `python3 -m json.tool` checks | 0 | registry, graph bundle, and validation specifications parsed |
| `lake env lean -R ../../Stage1_Instances/THM-M-1131 -o /tmp/thm-m-1131-obligation/Statement.olean ../../Stage1_Instances/THM-M-1131/Statement.lean` | 0 | exact statement elaborated into a temporary import artifact |
| `LEAN_PATH=/tmp/thm-m-1131-obligation lake env lean ../../Stage1_Instances/THM-M-1131/ObligationTree.lean` | 0 | two exact conditional composition declarations elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1131` | 0 | rank 336, planned, L0/rework-required, theorem incomplete |
| forbidden-term scan of `ObligationTree.lean` | 1 | expected no-match exit; no `sorry`, `admit`, or custom `axiom` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1131 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first direct Lean attempt, `lake env lean ../../Stage1_Instances/THM-M-1131/ObligationTree.lean`,
exited 1 because a sibling source file is not automatically an importable module. The successful
two-command recipe above creates only the required temporary olean and is the recorded replay spec.

## Status boundary

This node freezes architecture and validates conditional composition. `M1131-T-FLUXDIV` is the
minimal open root cut set and has no proof body. H0 source review, R0 reconstruction, trust and
provenance closure, root proof, hermetic release, independent acceptance, and theorem completion
remain open. The node is self-tested pending master acceptance; no authoritative item state was
edited.
