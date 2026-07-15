# THM-M-0721 proof recheck at `c4715a2b` (slot16)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T21:09:01+08:00`

Base revision: `c4715a2babbead02e04d70708c3ebc58c75a1942`

Base tree: `28cd40da86c57dea61aed02b4965f80699894bd3`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M3, R4]`, and neither audit completion nor theorem completion
is claimed.

The only checked route to the root is `root_of_candidate_packages`. It consumes, but does not
construct, the two immediate packages:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encodings, a polynomial certificate bound, verifier
  correctness, and a bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a bundled polynomial-time TM2 reduction.

All eleven SAT and Cook-Levin packages remain open. Their frozen registry entries have only
`planned:v1` fingerprints and null terminal-body IDs, not exact Lean declaration types. Therefore
append-only exact-signature refinement is required before leaf proof credit. The first failed gate
is `M0721-N-SAT-ENCODING`; the immediate root cut remains `M0721-T-SAT-IN-NP` plus
`M0721-T-UNIVERSAL-HARDNESS`.

Pinned mathlib supplies the TM2 structure and identity implementation, but no NP, SAT-language, or
Cook-Levin endpoint. Its apparent polynomial-time composition item is source-level `proof_wanted`;
trust-zero Lean reports the constant as unknown. Repository source and all target-history trees have
no other root or terminal-package body. The frozen external candidates remain supporting-only,
placeholder-dependent, or contract-incompatible. Empty, universal, identity, fixed-source,
classical-choice, or conditional shortcuts do not satisfy the exact universal polynomial-time
iff-reduction target.

There are now 33 dated unresolved proof JSON records including this one, far beyond the mandatory
five-tick split threshold in blueprint section 10.2. The master should accept or repair the
obligation-tree prerequisite, split this monolithic item into dependency-legal package children,
and append-only refine their exact Lean signatures. This worker did not edit the authoritative DAG
or generated checklist.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `c4715a2b...1942`, tree `28cd40da...94bd3`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed all 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 and both terminal packages M4. |
| Stream statement lines 1-94 and composition lines 11-26 to `LEAN_NUM_THREADS=1 timeout 180s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and supplied neither root child. |
| Scan owned Lean files for prohibited proof-device tokens | 1 expected | No `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs. |
| Scan pinned mathlib and repository-local Lean for an exact endpoint or terminal-package implementation | 1 expected | No eligible NP-completeness, SAT-language, Cook-Levin, root, or root-child body exists. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that `proof_wanted` created no checked declaration. |
| Search all target-history trees for `Proof.lean`, `proof-receipt.json`, or `check_proof.py` | 1 expected | No historical proof artifact exists. |
| Compare scoped proof inputs against prior base `f976b9b2...6231` | 0 | All proof inputs and pins were byte-identical; only the prior blocker pair was integrated under this target. |
| Inspect Lean/Lake and dependency identities | 0 | Lean 4.29.0; Lake 5.0.0; mathlib `8a178386...ea95`; flt-regular `56161b6e...1a27`; dependency worktrees clean. |
| Parse and assert this blocker, run `git diff --check`, and assert `.stage1-worker-selftest.json` is absent | 0 | JSON identity/base/open-state/no-proof invariants matched; no whitespace error; the completion manifest remained deliberately absent. |

## Reopen Condition

Accept or repair the obligation-tree prerequisite, split the proof item, and append-only refine and
implement the eleven frozen packages without placeholders. The alternative is an immutable,
compatible Lean 4 proof already in the pinned closure that can be exact-type checked, transported
to the Bool-word TM2 encodings, and provenance-audited without changing the dependency lock.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the proof phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent.
