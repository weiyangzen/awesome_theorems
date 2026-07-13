# Intake validation

## Boundary

This validates only the `S56-M-0063-INTAKE` dossier. It checks target membership, the planned
scope packet and open task DAG, exact source-record provenance, dependency pins, and the adjacent
Cayley-theorem API plus its regular-action specialization. It does not accept a canonical Lean
target or validate theorem closure.

The immutable worker base is Git revision
`c5f6fb269f6eb84efa935ee66c4e9bab92495e61`, tree
`7a41063c920c1b9cb849aa35c2f02ec4a4733655`. Before edits, `git status --short
--untracked-files=all` showed only the automation-provided `Formalizations/Lean/.lake` symlink to
the canonical pinned environment. The symlink and packages were used read-only. No `lake update`,
`lake build`, clone, fetch, or dependency mutation was run; this dirty worker packet is nonrelease
evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0063` | 0 | rank 1094; planned; no legacy slot; theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0063/IntakeProbe.lean)` | 0 | named Cayley anchor, regular-action specialization, and axiom report elaborated |
| Crossref metadata query for DOI `10.1080/14786445408647421` | 0 | 1854 Cayley bibliography confirmed; no article-body or H0 claim |
| `python3 -m json.tool` on each owned JSON artifact | 0 | structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0063-pycache python3 -m py_compile Stage1_Instances/THM-M-0063/check_intake.py` | 0 | checker compiles outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0063/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, pins, sources, H1/M3/R4, artifacts, receipt, packet, and open DAG agree |
| prohibited-token scan over owned Lean | 1 | expected no match; no placeholder, custom axiom, opaque, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-0063 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

## Result

The intake is self-tested and proposes `[_]` for integration review. Lifecycle remains `planned`;
the provisional root is `[H1, M3, R4]`; `audit_complete=false` and `theorem_complete=false`. The
first unclosed acceptance gate is integration-lane replay and master acceptance. The first
downstream mathematical gate is an independently approved source statement and exact regular-action
encoding suitable for pinned Lean elaboration, fingerprinting, and statement mutations.
