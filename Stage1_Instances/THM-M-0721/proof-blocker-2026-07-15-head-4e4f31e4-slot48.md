# THM-M-0721 proof recheck at `4e4f31e4` (slot48)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T08:07:42+08:00`

Base revision: `4e4f31e4342e7160fe132b536fb7dc565fa1ded0`

Base tree: `e2c22705bcd18e365b5ac54abb241f70b338a853`

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
Cook-Levin endpoint. Its polynomial-time composition declaration is source-level `proof_wanted`,
is not an available checked declaration, and is ineligible for proof credit. Current-base repository
and pinned-source scans found no replacement. The frozen external audit classifies its candidates as
supporting-only, placeholder-dependent, or contract-incompatible; no moving dependency was fetched
or credited. Its replay could not be refreshed because the host network was unreachable.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is not
complete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `4e4f31e4...ded0`, tree `e2c22705...a853`; only the automation-provided `.lake` symlink was initially untracked, pointing to canonical pinned artifacts. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204`; all four mutations were distinguished; the pinned environment matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 and both terminal packages M4. |
| From `Formalizations/Lean`, stream the declaration-bearing portions of `Statement.lean` and `ObligationTree.lean` to `LEAN_NUM_THREADS=1 timeout 180s lake env lean --trust=0 -t0 --stdin` | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported exactly `[propext, Quot.sound]`; no terminal-package inhabitant or exact-root proof was produced. |
| `rg -n '(^|[^[:alnum:]_])(sorry|admit|axiom|unsafe)([^[:alnum:]_]|$)|proof_wanted|sorryAx' Stage1_Instances/THM-M-0721 --glob '*.lean'` | 1 expected | No prohibited token occurs in owned Lean files. |
| Same prohibited-device scan on pinned `Mathlib/Computability/TuringMachine/Computable.lean` | 0 | Sole hit: line 284, `proof_wanted TM2ComputableInPolyTime.comp`. |
| Scan pinned mathlib Lean source for `IsNPComplete`, `NPcomplete`, `NPComplete`, `CookLevin`, `cook_levin`, or `SATLang` | 1 expected | No eligible endpoint exists. |
| Ask Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` under the pinned import and trust-zero environment | 1 expected | Lean reported `Unknown constant`, confirming that the source-level `proof_wanted` command did not add a checked declaration. |
| Search repo-local Lean outside this target for the exact root, package names, and NP-completeness/Cook-Levin endpoint names | 1 expected | No matching proof endpoint or terminal-package implementation exists. |
| `cd Formalizations/Lean && lake env lean --version && lake --version && git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree} && test -z "$(git -C .lake/packages/mathlib status --porcelain)"` | 0 | Lean 4.29.0, Lake 5.0.0, mathlib `8a178386...ea95` / tree `bdc39a31...c2b`, dependency worktree clean. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Local pin and source-hash checks passed; the first remote replay then failed with `URLError: [Errno 101] Network is unreachable`. No fresh external evidence is credited. |
| Parse the fresh blocker JSON, no-index whitespace-check both fresh files, and assert `.stage1-worker-selftest.json` is absent | 0 overall | JSON parsed; both new-file checks returned expected exit 1 without diagnostics; completion self-test is deliberately absent. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already available in the pinned closure can be exact-type
checked, transported to the frozen TM2 encodings, and provenance-audited without changing the lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
