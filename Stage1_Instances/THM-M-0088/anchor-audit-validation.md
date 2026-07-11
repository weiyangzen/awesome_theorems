# Anchor-audit validation record

Item: `S56-M-0088-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `94e3ff8d01686341332e0fbae530f51b5cdb5a6f`

## Result

The exact mathlib anchor is `CategoryTheory.Yoneda.fullyFaithful` in
`Mathlib.CategoryTheory.Yoneda` at immutable revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The manifest pin, local dependency
HEAD, source blob `d4afb27182601dcd39feb5adeb40b9650d25279b`, and source SHA-256
`abf848cf1d1de154bff0dc0b3c0fb7cabefac92e44187f4b7992f9942c48622c` were
recorded independently. `AnchorAudit.lean` checks that the declaration inhabits the frozen
data-valued target without transport. For both the terminal declaration and audit wrapper, Lean
reports `[propext, Classical.choice, Quot.sound]`; these are recorded rather than silently treated
as an empty trust boundary.

The repository's historical `S1_M_137` wrapper resolves to the same terminal body and earns no
independent proof-body credit. Four external repositories were classified at immutable revisions;
none is imported or credited. Remote discovery was bounded: unauthenticated GitHub code search
returned HTTP 401 and later raw-content requests timed out, so this record does not claim an
exhaustive Internet search.

## Commands and exact results

Commands ran from the repository root unless the table names `Formalizations/Lean` as the cwd.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0088` | 0 | rank 137; planned; theorem incomplete; legacy artifacts unaccepted |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the Lake manifest pin |
| `git -C Formalizations/Lean/.lake/packages/mathlib ls-tree HEAD Mathlib/CategoryTheory/Yoneda.lean` | 0 | blob `d4afb27182601dcd39feb5adeb40b9650d25279b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib show HEAD:Mathlib/CategoryTheory/Yoneda.lean \| sha256sum` | 0 | `abf848...8622c` |
| `lake env lean ../../Stage1_Instances/THM-M-0088/AnchorAudit.lean` (cwd `Formalizations/Lean`) | 0 | exact wrapper elaborated; both `#print axioms` results were `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool Stage1_Instances/THM-M-0088/anchor_audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `rg -n '\\b(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-0088/AnchorAudit.lean` | 1 | no placeholder or custom-axiom token found; exit 1 is the expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0088 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This phase is self-tested audit evidence pending master acceptance. It establishes candidate
identity, immutable revision, exact type, source location, local feasibility, and terminal axiom
output. It does not close the proof DAG, prove the theorem under rev-5.6, establish transitive TCB
or release provenance, or advance any dependent node.
