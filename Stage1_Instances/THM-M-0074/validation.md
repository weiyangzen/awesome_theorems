# Intake validation

## Boundary

This is validation of the `S56-M-0074-INTAKE` dossier only. It proves that the target belongs to
the closed rev-5.6 population, its planned scope packet agrees with the authoritative execution DAG,
and adjacent pinned Lean APIs plus a deliberately nonterminal exact-order envelope elaborate. It
does not validate a canonical Monster statement or any construction proof.

The immutable worker base was Git revision
`d3cbfa8941a8bcaafa3b8a690d1333f9643288ad`, tree
`e912a107150c6f9c3fc096901412fce0337c7c01`. Before edits, `git status --short
--untracked-files=all` showed only the automation-provided `Formalizations/Lean/.lake` symlink to
the canonical pinned environment. The symlink and packages were used read-only. No `lake update`,
`lake build`, clone, fetch, or dependency mutation was run; this dirty worker packet is nonrelease
evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0074` | 0 | rank 1024; planned; legacy artifacts unaccepted; theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0074/IntakeProbe.lean)` | 0 | generic finite/simple/equivalence APIs and the nonterminal exact-order envelope elaborated |
| bounded source inspection of DOI `10.1073/pnas.78.2.689` and DOI `10.1007/BF01389186` | 0 | 1981 open announcement gives exact construction scope; 1982 full-paper bibliography corroborated; no H0 claim |
| bounded focused `rg` over repo-local and pinned mathlib Lean | 0/1 | no terminal Griess/Monster group declaration; unrelated bibliography and monster-model wording only |
| `python3 -m json.tool` on each owned JSON artifact | 0 | structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0074-pycache python3 -m py_compile Stage1_Instances/THM-M-0074/check_intake.py` | 0 | checker compiles outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0074/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, scope, sources, H1/M4/R4, artifact inventory, receipt, self-test, and open DAG agree |
| prohibited-token scan over owned Lean | 1 | expected no match; no placeholder, custom axiom, opaque, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-0074 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

## Result

The assigned intake phase is self-tested and proposes `[_]` for integration review. Lifecycle
remains `planned`; the provisional root is `[H1, M4, R4]`; `audit_complete=false` and
`theorem_complete=false`. The first unclosed acceptance gate is integration-lane replay and master
acceptance of this packet. The first downstream mathematical gate is an independently approved,
source-complete proposition and construction boundary suitable for exact Lean elaboration and
mutation testing.
