# THM-M-0721 proof recheck at `6623474b` (slot38)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T21:39:17+08:00`

Base revision: `6623474b775e74ea6f20e717a65bac54d45ea927`

Base tree: `d0d9fd959333b17d754206b296df2250a4efee1e`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M3, R4]`, and neither audit completion nor theorem completion
is claimed.

The only checked local route to the root is `root_of_candidate_packages`. It consumes, but does not
construct, the two immediate packages:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encodings, a polynomial certificate bound, verifier
  correctness, and a bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a bundled polynomial-time TM2 reduction.

All eleven SAT and Cook-Levin packages remain open. Their registry entries have only `planned:v1`
fingerprints and null terminal-body IDs, not exact Lean declarations. Append-only exact-signature
refinement is therefore required before leaf proof credit. The first failed gate is
`M0721-N-SAT-ENCODING`; the immediate root cut remains `M0721-T-SAT-IN-NP` plus
`M0721-T-UNIVERSAL-HARDNESS`.

Pinned mathlib supplies the TM2 structure and identity implementation, but no NP, SAT-language, or
Cook-Levin endpoint. Its apparent polynomial-time composition item is source-level `proof_wanted`;
trust-zero Lean reports the constant as unknown. Repository source and target history have no other
root or terminal-package body. The frozen external candidates remain supporting-only,
placeholder-dependent, or contract-incompatible. Empty, universal, identity, fixed-source,
classical-choice, conditional, or self-referential shortcuts do not satisfy the exact universal
polynomial-time iff-reduction target.

## Required Split

There were 33 dated unresolved proof JSON records before this run, so this is the documented 34th
unresolved attempt. Blueprint section 10.2 requires a split after five unresolved execution ticks.
The master should accept or repair the obligation-tree prerequisite, replace this monolithic retry
with dependency-legal children for the eleven packages, and append-only refine their exact Lean
signatures, beginning with `M0721-N-SAT-ENCODING`. The authoritative DAG nevertheless still reports
attempts `0` and no children. This worker did not edit that DAG or the generated checklist.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network command, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `6623474b...a927`, tree `d0d9fd95...e1e`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed all 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 and both terminal packages M4. |
| From `Formalizations/Lean`, run `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0721/Statement.lean` | 0 | Printed the exact target as `exists language, NPComplete language`. |
| Stream statement lines 1-95 and composition lines 9-28 to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and supplied neither root child. |
| Scan owned Lean files for prohibited proof-device tokens | 1 expected | No `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs. |
| Scan pinned mathlib and repository-local Lean for an exact endpoint or terminal-package implementation | 1 expected | No eligible NP-completeness, SAT-language, Cook-Levin, root, or root-child body exists. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that `proof_wanted` created no checked declaration. |
| Inspect Lean/Lake and dependency identities | 0 | Lean 4.29.0; Lake 5.0.0; mathlib `8a178386...ea95`; flt-regular `56161b6e...1a27`; dependency worktrees clean. |
| Count dated unresolved proof JSON artifacts and assert `Proof.lean`, `proof-receipt.json`, and `check_proof.py` are absent | 0 | Found 33 prior blocker records and no proof authority artifact. |

## Reopen Condition

Accept or repair the obligation-tree prerequisite, split the proof item, and append-only refine and
implement the eleven frozen packages without placeholders. The alternative is an immutable,
compatible Lean 4 proof already in the pinned closure that can be exact-type checked, transported
to the Bool-word TM2 encodings, and provenance-audited without changing the dependency lock.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the proof phase is not genuinely complete, `.stage1-worker-selftest.json`
remains deliberately absent.
