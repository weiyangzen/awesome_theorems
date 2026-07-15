# THM-M-0721 proof recheck at `b5085dce` (slot38)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-16T00:26:36+08:00`

Base revision: `b5085dcef95933c753b6877bce0f634c1082a98d`

Base tree: `c9baed8c952fce6f884a6ee997845c0ec979b52b`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M3, R4]`, and neither audit completion nor theorem completion
is claimed.

The exact target requires a concrete binary language with both verifier-based NP membership and a
polynomial-time iff reduction from every language satisfying that same NP definition. The only
checked local route to the root is `root_of_candidate_packages`; it consumes, but does not
construct, the two immediate packages:

- `M0721-T-SAT-IN-NP` needs faithful binary SAT encodings, a certificate bound, verifier
  correctness, and a bundled polynomial-time TM2 verifier.
- `M0721-T-UNIVERSAL-HARDNESS` needs arbitrary frozen-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Their eleven dependencies remain open with `planned:v1` fingerprints and null terminal-body IDs.
The first failed mathematical proof gate is therefore `M0721-N-SAT-ENCODING`, and the immediate
root cut remains the two packages above. Exact leaf signatures must be append-only refined before
leaf implementations can receive proof credit.

Pinned mathlib provides the TM2 structure and identity implementation, but no NP, SAT-language, or
Cook-Levin endpoint. Its apparent polynomial-time composition theorem is source-level
`proof_wanted`; trust-zero Lean reports `Turing.TM2ComputableInPolyTime.comp` as an unknown constant.
Current repository and pinned-mathlib searches found no other root or root-package body. The frozen
external candidates remain supporting-only, placeholder-dependent, or contract-incompatible.
Identity gives only reduction reflexivity; empty, universal, fixed-source, conditional, or
self-referential shortcuts do not satisfy universal polynomial-time iff hardness.

## Dependency And Split Gates

The generated blueprint shows only worker-provisional `[_]` evidence for
`S56-M-0721-OBLIGATION_TREE`; target-local `task-dag.json` still has no accepted states and marks
both that prerequisite and this proof task open. Provisional work may be prepared, but proof
acceptance is not dependency-legal before the integration lane accepts or repairs the prerequisite.

There were 35 dated unresolved proof JSON records before this run, making this the 36th. Blueprint
section 10.2 requires splitting after five unresolved execution ticks. The authoritative proof item
nevertheless still records attempts `0` and no children. The master must stop scheduling the same
monolithic proof request and create dependency-legal child nodes for the eleven frozen packages,
beginning with an exact signature and implementation for `M0721-N-SAT-ENCODING`. This worker did not
edit the authoritative DAG or generated checklist.

## Current-Base Delta

The only scoped target change since the preceding recheck base `505ce3e3` is integration of that
recheck's Markdown and JSON pair at commit `b5085dce`. The exact statement, conditional composition,
obligation registry, typed graphs, anchor audit, validation specification, target manifest,
execution skill, toolchain, dependency manifest, and pinned mathlib source are byte-identical. No
new proof source, dependency pin, accepted prerequisite, or child split appeared.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network operation, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `b5085dce...a98d`, tree `c9baed8c...b52b`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed all 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 and both terminal packages M4. |
| From `Formalizations/Lean`, run `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0721/Statement.lean` | 0 | Printed the exact target as an existential language satisfying `NPComplete`. |
| Stream statement lines 1-95 and composition lines 9-28 to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and supplied neither root package. |
| Import the pinned computability module and ask trust-zero Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that `proof_wanted` created no checked declaration. |
| Scan owned Lean files for prohibited proof-device tokens | 1 expected | No `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs. |
| Search pinned mathlib and other repo-local Lean for the exact root/packages or NP-completeness, SAT-language, and Cook-Levin endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists outside this dossier. |
| Inspect tool and dependency identities | 0 | Lean 4.29.0; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`; flt-regular `56161b6e...1a27`, tree `32c9eace...c893`; dependency worktrees clean. A first combined query used paths relative to the changed directory and exited 128 after printing Lean/Lake versions; corrected absolute-path queries exited 0. |
| Parse/assert the blocker JSON; run `git diff --no-index --check /dev/null` on each untracked artifact while accepting expected diff exit 1; scan trailing whitespace; assert `.stage1-worker-selftest.json` is absent | 0 | Structured blocker invariants passed; both no-index checks produced no whitespace diagnostics, the trailing-whitespace scan returned expected no-match exit 1, and the completion self-test remained deliberately absent. |

## Reopen Condition

The master should accept or repair the obligation-tree prerequisite and split this oversized proof
item into dependency-legal children. Append-only refine exact Lean signatures and implement the
eleven frozen SAT and Cook-Levin packages without placeholders. The alternative is an immutable,
compatible Lean 4 proof already in the pinned closure that can be exact-type checked, transported
to the Bool-word TM2 encodings, and provenance-audited without changing the dependency lock; no
such proof is currently present.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned positive proof phase is not complete,
`.stage1-worker-selftest.json` remains deliberately absent.
