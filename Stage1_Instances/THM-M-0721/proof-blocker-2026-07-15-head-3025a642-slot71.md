# THM-M-0721 proof recheck at `3025a642` (slot71)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T08:49:32+08:00`

Base revision: `3025a6428cc070b33e16b1e88145ff9055f6dde2`

Base tree: `a684b3b5f61a32f7e79b8ce365a82e2d8e968714`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The exact target requires both a concrete bundled polynomial-time TM2 verifier package and, for
every language satisfying that verifier contract, a concrete bundled polynomial-time TM2
many-one reduction. The checked declaration `root_of_candidate_packages` only composes explicit
membership and hardness hypotheses. It constructs neither root child:

- `M0721-T-SAT-IN-NP`: encoded SAT, verifier correctness, certificate bound, and a
  `TM2ComputableInPolyTime` verifier witness;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a `TM2ComputableInPolyTime` reduction witness.

Pinned mathlib supplies the TM2 substrate and identity machine but no NP, SAT-language, or
Cook-Levin endpoint. Its polynomial-time composition item is source-level `proof_wanted`, and Lean
confirms that it creates no checked constant. Repo-local and pinned-source scans found no
replacement. The immutable anchor recheck passed for all three audited external candidates, but
those candidates remain supporting-only, placeholder-dependent, or contract-incompatible and have
no checked transport to the frozen binary-word TM2 target.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Empty-language, universal-language,
identity, classical-choice, computable-reducibility, fixed-source, or conditional shortcuts cannot
supply the required machine and runtime witnesses. Because the positive proof phase is incomplete,
no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `3025a642...dde2`, tree `a684b3b5...8714`; only the automation-provided `.lake` symlink was initially untracked, pointing to canonical pinned artifacts. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204`; all four structural mutations were distinguished; pinned Lean and mathlib identities matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 and both terminal packages M4. |
| From `Formalizations/Lean`, stream the declaration-bearing portions of `Statement.lean` and `ObligationTree.lean` to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact statement and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]`; neither terminal package was produced. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited token occurs in the owned Lean files. |
| Run the same scan over pinned `Mathlib/Computability/TuringMachine/Computable.lean` | 0 | Sole hit: line 284, `proof_wanted TM2ComputableInPolyTime.comp`. |
| Scan pinned mathlib Lean source for `IsNPComplete`, `NPcomplete`, `NPComplete`, `CookLevin`, `cook_levin`, or `SATLang` | 1 expected | No eligible endpoint exists. |
| Ask Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` under the pinned import and trust-zero environment | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| Search repo-local Lean outside this target for the exact root, package names, and NP-completeness/Cook-Levin endpoint names | 1 expected | No matching proof endpoint or terminal-package implementation exists. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable external candidates matched; root classification remained M2. |
| From `Formalizations/Lean`, print Lean/Lake versions and verify pinned mathlib revision, tree, and clean dependency status | 0 | Lean 4.29.0 at `98dc76e...740`; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean. |
| Parse the structured blocker with `python3 -m json.tool` and check its blocked-state invariants with `jq -e` | 0 | Item ID, `[ ]` state, open-root flags, absent-selftest flag, and exact two-node root cut all matched. |
| Run `git diff --no-index --check /dev/null` on each fresh blocker artifact and assert both expected new-file exits equal 1 | 0 | Neither diff emitted a whitespace diagnostic; both returned the expected difference exit 1. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already available in the pinned closure can be
exact-type checked, transported to the frozen TM2 encodings, and provenance-audited without
changing the dependency lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.
