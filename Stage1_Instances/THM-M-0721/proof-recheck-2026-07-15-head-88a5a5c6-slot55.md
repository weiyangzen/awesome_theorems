# THM-M-0721 proof recheck at `88a5a5c6` (slot55)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T19:41:51+08:00`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

Base tree: `a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`; lifecycle stays
`planned`; the root vector stays `[H1, M3, R4]`; audit completion and theorem completion stay
false.

The only checked local route to the root is `root_of_candidate_packages`. It consumes, but does not
construct, the two immediate root packages:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encodings, verifier correctness, a polynomial
  certificate bound, and an actual bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: normalization of every frozen `InNP` verifier, Cook-Levin
  tableaux, both correctness directions, and an actual bundled polynomial-time TM2 reduction.

Eleven SAT and Cook-Levin packages remain open. The registry still gives the first of them,
`M0721-N-SAT-ENCODING`, only a planned prose signature. Concrete proof credit therefore requires
an append-only exact-signature refinement before missing bodies can be implemented and linked.

Pinned mathlib supplies the TM2 polynomial-time structure and its identity implementation, but no
NP, SAT-language, or Cook-Levin endpoint. Its apparent composition declaration is source-level
`proof_wanted`; trust-zero Lean reports that the constant is unknown. Current-base scans of
repository source, pinned mathlib, and target history found no inhabitant of either terminal
package and no prior proof module, receipt, or checker. The immutable external audit remains
supporting-only, placeholder-dependent, or contract-incompatible.

## Required Split

There were already 28 target-owned unresolved proof JSON records before this run. Including this
recheck, the documented minimum is 29. Blueprint section 10.2 requires a split after five
unresolved execution ticks. The integration lane must stop scheduling this monolithic proof item
and introduce dependency-legal child proof nodes for the eleven frozen packages, beginning with an
exact-signature child for `M0721-N-SAT-ENCODING`. The authoritative DAG nevertheless still reports
attempts `0` and no children; this worker did not edit that DAG or the generated checklist.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `88a5a5c6...6d68`, tree `a0a75048...e8e4`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 with both terminal packages M4. |
| Stream statement lines 1-94 and composition lines 11-26 to `lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for prohibited proof-device tokens | 1 expected | No `sorry`, `admit`, axiom, unsafe, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs in owned Lean files. |
| Search repository and pinned-mathlib Lean sources outside this dossier for the exact root/packages and NP-completeness endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists. |
| Ask trust-zero Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` created no checked declaration. |
| Search all target-history trees for `Proof.lean`, `proof-receipt.json`, or `check_proof.py` | 1 expected | No historical proof module, proof receipt, or proof checker exists under this target. |
| `timeout 240s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Reported that local pins/hashes and all three immutable external candidates match; the frozen root classification remained M2. |
| Query Lean/Lake/dependency identities, dependency status, and pinned hashes | 0 | Lean 4.29.0 at `98dc76e3...740`; Lake 5.0.0; mathlib `8a178386...ea95` tree `bdc39a31...c2b`; flt-regular `56161b6e...1a27` tree `32c9eace...c893`; both dependency worktrees were clean and pinned hashes matched. |
| `python3 -m json.tool Stage1_Instances/THM-M-0721/proof-recheck-2026-07-15-head-88a5a5c6-slot55.json` | 0 | Blocker artifact is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0721/proof-recheck-2026-07-15-head-88a5a5c6-slot55.json Stage1_Instances/THM-M-0721/proof-recheck-2026-07-15-head-88a5a5c6-slot55.md` | 0 | No whitespace error in the blocker pair. |

## Reopen Condition

The master first splits the oversized item into dependency-legal children and append-only refines
their exact Lean signatures. Workers can then implement the eleven frozen packages without
placeholders. An alternative is an immutable compatible Lean 4 proof already present in the pinned
closure that can be exact-type checked, transported to the frozen TM2 encodings, and
provenance-audited without changing the dependency lock; the current search found none.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
