# THM-M-0721 proof recheck at `557b928b` (slot63)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T07:53:47+08:00`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The frozen target requires both a concrete polynomial-time TM2 verifier package and, for every
language satisfying that verifier contract, a concrete polynomial-time TM2 many-one reduction.
The checked `root_of_candidate_packages` declaration only composes membership and hardness
hypotheses. It constructs neither root child:

- `M0721-T-SAT-IN-NP`: encoded SAT, verifier correctness, certificate bound, and a bundled
  `TM2ComputableInPolyTime` verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a bundled polynomial-time TM2 reduction.

Pinned mathlib supplies the TM2 substrate and identity machine, but no NP, SAT-language, or
Cook-Levin endpoint. Its polynomial-time composition declaration is explicitly `proof_wanted` and
is ineligible for proof credit. Current-base repository and pinned-source scans found no replacement.
The frozen external audit likewise classifies its candidates as supporting-only, placeholder-
dependent, or contract-incompatible; no moving dependency was fetched or credited.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is not
complete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `557b928b...37aa`, tree `e677879a...9465`; only the automation-provided `.lake` symlink was initially untracked, pointing to canonical pinned artifacts. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204`; all four mutations were distinguished; the pinned environment matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 and both terminal packages M4. |
| From `Formalizations/Lean`, concatenate the declaration-bearing portions of `Statement.lean` and `ObligationTree.lean` into a temporary file, then run `LEAN_NUM_THREADS=1 timeout 180s lake env lean --trust=0 -t0 <temporary-file>` | 0 | Exact statement and conditional composition elaborated; the type retained both terminal-package premises; `#print axioms` reported exactly `[propext, Quot.sound]`; temporary file removed. |
| `rg -n '(^|[^[:alnum:]_])(sorry|admit|axiom|unsafe)([^[:alnum:]_]|$)|proof_wanted|sorryAx' Stage1_Instances/THM-M-0721 --glob '*.lean'` | 1 expected | No prohibited token occurs in owned Lean files. |
| Same prohibited-device scan on pinned `Mathlib/Computability/TuringMachine/Computable.lean` | 0 | Sole hit: line 284, `proof_wanted TM2ComputableInPolyTime.comp`. |
| Scan pinned mathlib Lean source for `IsNPComplete`, `NPcomplete`, `NPComplete`, `CookLevin`, `cook_levin`, or `SATLang` | 1 expected | No eligible endpoint exists. |
| `cd Formalizations/Lean && lake env lean --version && lake --version && git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree} && test -z "$(git -C .lake/packages/mathlib status --porcelain)"` | 0 | Lean 4.29.0, Lake 5.0.0, mathlib `8a178386...ea95` / tree `bdc39a31...c2b`, dependency worktree clean. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already available in the pinned closure can be exact-type
checked, transported to the frozen TM2 encodings, and provenance-audited without changing the lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
