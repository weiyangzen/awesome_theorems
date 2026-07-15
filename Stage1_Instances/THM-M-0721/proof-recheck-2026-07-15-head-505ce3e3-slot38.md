# THM-M-0721 proof recheck at `505ce3e3` (slot38)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T22:44:20+08:00`

Base revision: `505ce3e35ad7f821c8313a3744c50150c5d543a6`

Base tree: `be6f30e43f2e30c57c82898440191a46576c86fa`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M3, R4]`, and neither audit completion nor theorem completion
is claimed.

The only checked local root route remains `root_of_candidate_packages`. It consumes, but does not
construct, `M0721-T-SAT-IN-NP` and `M0721-T-UNIVERSAL-HARDNESS`. Their eleven SAT and Cook-Levin
dependencies remain open with `planned:v1` fingerprints and null terminal-body IDs. Consequently
the first failed proof gate is `M0721-N-SAT-ENCODING`, and append-only exact-signature refinement is
required before leaf implementation can receive proof credit.

Pinned mathlib supplies the TM2 polynomial-time structure and identity implementation, but no NP,
SAT-language, or Cook-Levin endpoint. Its apparent composition theorem is source-level
`proof_wanted`; trust-zero Lean reports the name as an unknown constant. Current source, repository
history, sibling targets, and the pinned dependency closure contain no implementation of either
root package. The frozen external candidates remain supporting-only, placeholder-dependent, or
contract-incompatible. Empty, universal, identity, fixed-source, classical-choice, conditional,
and self-referential candidates do not provide the universally quantified polynomial-time iff
reductions required by the exact target.

## Current-Base Delta

The only scoped target change since the preceding recheck base `6623474b` is the integration of
that recheck's Markdown and JSON pair at commit `505ce3e3`. The exact statement, composition
interface, obligation registry, typed graphs, anchor audit, validation specification, target
manifest, execution skill, toolchain, dependency manifest, and pinned mathlib source are
byte-identical. No new proof source, dependency pin, accepted prerequisite, or child split appeared.

There are now 34 dated unresolved proof JSON records. Blueprint section 10.2 requires an item to be
split after five unresolved execution ticks, while the authoritative proof node still records
attempts `0` and no children. This worker did not modify the authoritative DAG or generated
checklist. The integration lane must accept or repair the obligation-tree prerequisite and replace
the monolithic proof retry with dependency-legal child nodes for the eleven frozen packages,
starting with exact signatures and an implementation for `M0721-N-SAT-ENCODING`.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network command, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `505ce3e35ad7...a6`, tree `be6f30e43f2e...fa`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed all 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 and both terminal packages M4. |
| From `Formalizations/Lean`, run `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0721/Statement.lean` | 0 | Printed the exact target as `exists language, NPComplete language`. |
| Stream statement lines 1-95 and composition lines 9-28 to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and supplied neither root package. |
| Scan owned Lean files for prohibited proof-device tokens | 1 expected | No `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs. |
| Search repository, history, sibling targets, and pinned mathlib for the exact root/packages or NP-completeness endpoint | 1 expected | No eligible endpoint, terminal-package implementation, historical `Proof.lean`, receipt, or checker exists. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that `proof_wanted` created no checked declaration. |
| Inspect tool and dependency identities | 0 | Lean 4.29.0; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`; flt-regular `56161b6e...1a27`, tree `32c9eace...c893`; dependency worktrees clean. |

## Reopen Condition

Accept or repair `S56-M-0721-OBLIGATION_TREE`, split this oversized proof node, append-only refine
the exact Lean signatures, and implement the eleven frozen SAT and Cook-Levin packages without
placeholders. An alternative is an immutable compatible Lean 4 proof in the pinned closure that
can be exact-type checked, transported to the Bool-word TM2 encodings, and provenance-audited
without changing the dependency lock; no such proof is currently present.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned positive proof phase is not complete,
`.stage1-worker-selftest.json` remains deliberately absent.
