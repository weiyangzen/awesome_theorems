# THM-M-0721 proof recheck at `3b741f76` (slot72)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T07:22:20+08:00`

Base revision: `3b741f76df83670ba151a8f6ad6257bb8b6f6ead`

Base tree: `021c27ee3fae960d30f31e7f932f29401412edb0`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The frozen statement requires both a concrete polynomial-time TM2 verifier package and, for every
language satisfying that verifier contract, a concrete polynomial-time TM2 many-one reduction.
The checked declaration `root_of_candidate_packages` only composes membership and hardness
hypotheses. It constructs neither root child:

- `M0721-T-SAT-IN-NP`: an encoded SAT language, verifier, correctness proof, certificate bound,
  and `TM2ComputableInPolyTime` verifier witness;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a polynomial-time TM2 reduction witness.

Pinned mathlib supplies the TM2 substrate and identity machine, but no NP, SAT, or Cook-Levin
endpoint. Its polynomial-time composition declaration is explicitly `proof_wanted`. The bounded
local and immutable-candidate searches found no replacement: the audited Cook-Levin projects are
supporting-only, placeholder-dependent, or contract-incompatible. The timed-out fresh replay is not
credited; these are the retained classifications of the frozen immutable audit.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining minimal root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is
incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `3b741f76...6ead`, tree `021c27ee...edb0`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...204`; all four mutations were distinguished; the pinned environment matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained open M3 and both terminal packages M4. |
| `(cd Formalizations/Lean && { sed -n '1,94p' ../../Stage1_Instances/THM-M-0721/Statement.lean; sed -n '11,26p' ../../Stage1_Instances/THM-M-0721/ObligationTree.lean; printf 'end Stage1Instances.THM_M_0721\n'; } \| LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 --stdin)` | 0 | Exact statement and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]`; no terminal-package inhabitant was produced. |
| `rg -n '(^\|[^[:alnum:]_])(sorry\|admit\|axiom\|unsafe)([^[:alnum:]_]\|$)\|proof_wanted\|sorryAx' Stage1_Instances/THM-M-0721 --glob '*.lean'` | 1 expected | No prohibited token occurred in owned Lean files. |
| `rg -n '(^\|[^[:alnum:]_])(sorry\|admit\|axiom\|unsafe)([^[:alnum:]_]\|$)\|proof_wanted\|sorryAx' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/TuringMachine/Computable.lean` | 0 | The sole hit was line 284, `proof_wanted TM2ComputableInPolyTime.comp`. |
| `rg -n 'ExistsNPCompleteLanguage\|NPComplete\|IsNPComplete\|NPcomplete\|CookLevin\|cook_levin\|SATLang' Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances/THM-M-0721 --glob '*.lean'` | 0 | Endpoint matches were confined to this target's statement and conditional interface. |
| `timeout 120s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 124 | Fresh immutable external replay did not finish within the bound; no fresh network evidence is credited. The frozen audit and its immutable hashes were not changed. |
| `(cd Formalizations/Lean && lake env lean --version && git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree} && test -z "$(git -C .lake/packages/mathlib status --porcelain)")` | 0 | Lean 4.29.0 at `98dc76e...740`; mathlib revision `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is blocked. |
| `python3 -m json.tool Stage1_Instances/THM-M-0721/proof-blocker-2026-07-15-head-3b741f76-slot72.json >/dev/null` | 0 | The structured blocker parsed as JSON. |
| `jq -e '.item_id == "S56-M-0721-PROOF" and .state == "[ ]" and .proof_phase_complete == false and .root_closed == false and .theorem_complete == false and .selftest_manifest_written == false and (.remaining_root_cut_set == ["M0721-T-SAT-IN-NP", "M0721-T-UNIVERSAL-HARDNESS"])' Stage1_Instances/THM-M-0721/proof-blocker-2026-07-15-head-3b741f76-slot72.json >/dev/null` | 0 | Blocked-state, no-closure, no-selftest, and exact-cut invariants passed. |
| `set +e; git diff --no-index --check /dev/null Stage1_Instances/THM-M-0721/proof-blocker-2026-07-15-head-3b741f76-slot72.json; j=$?; git diff --no-index --check /dev/null Stage1_Instances/THM-M-0721/proof-blocker-2026-07-15-head-3b741f76-slot72.md; m=$?; test "$j" -eq 1 -a "$m" -eq 1` | 0 | Neither new-file diff emitted a whitespace diagnostic; both returned the expected difference exit 1. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof can be pinned, exact-type checked, transported to the
frozen TM2 encodings, and provenance-audited without changing the dependency lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
