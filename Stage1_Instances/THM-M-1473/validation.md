# Intake validation

## Scope

This record validates only the `planned` intake for `S56-M-1473-INTAKE`: target membership, the
source and statement boundary, the scope map, six open downstream tasks, pinned adjacent Lean APIs,
and the provisional receipt/worker-packet agreement. It does not validate a canonical CFL
statement, a proof, an exhaustive anchor audit, audit completion, or theorem completion.

The repository base is `f4efdfc7c685252a98f3508a5974ba81c0377a95`, tree
`94a9cfc613f86042a21fdfa174ba887334b93893`. Before editing, the only untracked path was the
automation-provided `Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was
used read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

The external primary scan was inspected in temporary storage and not added to the repository. Its
hash and archival identifiers support source-family discovery, not release evidence or `H0`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard, assurance groups, and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework targets passed |
| `python3 scripts/stage1_target.py show THM-M-1473` | 0 | rank 1150 planned target, no accepted legacy artifacts, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided untracked `.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree above |
| `git blame -L 10749,10754 -- Docs/researches/math_theorems.md` | 0 | all catalog lines originate at `bcf3f9fa...` |
| Crossref DOI lookup and Göttingen IIIF/PDF inspection | 0 | matched Courant-Friedrichs-Lewy 1928, pp. 32-74; 44-page scan SHA-256 `2aee594c...2a30f`; discovery only |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...fab16740`, release build |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and status | 0 | revision `8a178386...5449d50efeea95`, tree `bdc39a31...5c2b`, clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1473/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; four representative axiom reports; stdout SHA-256 `c336880f...e23cc`, empty stderr |
| bounded exact-topic `rg` over pinned mathlib and tracked repository Lean | 1 expected | no CFL/domain-of-dependence/hyperbolic finite-difference target; empty-output SHA-256 `e3b0c442...b855` |
| `python3 -m json.tool` on owned JSON files and worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=<temporary> python3 -m py_compile Stage1_Instances/THM-M-1473/check_intake.py` | 0 | scoped validator parses without owned cache output |
| `python3 -B Stage1_Instances/THM-M-1473/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, null target, H1/M4/R4 boundary, source/pin hashes, receipt agreement, inventory, and six open tasks passed |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `git diff --check` plus no-index checks for new files | 0 | no whitespace diagnostics |

The structural self-test and whitespace checks were rerun after the receipt and root worker packet
were finalized.

## Known failures and boundary

Master acceptance is pending. The catalog gloss still does not select an exact proposition. Source
admission, translation/correction/errata review, independent source and numerical-PDE review,
canonical Lean target and mutations, exhaustive anchor audit, obligation registry, typed graphs,
proof, composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
