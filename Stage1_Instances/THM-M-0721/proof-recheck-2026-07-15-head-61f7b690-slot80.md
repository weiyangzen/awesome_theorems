# THM-M-0721 proof recheck at `61f7b690` (slot80)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T18:01:44+08:00`

Base revision: `61f7b69093a1a921bba3b39c1c58955f9b3a4808`

Base tree: `5849148c92f4a72549a18481b3eda847afb1e3da`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`; lifecycle stays
`planned`; the root vector stays `[H1, M3, R4]`; audit completion and theorem completion stay
false.

The checked declaration `root_of_candidate_packages` is conditional composition. It consumes, but
does not construct, the immediate root packages:

- `M0721-T-SAT-IN-NP`: a faithful binary SAT encoding, correct certificate verifier, polynomial
  certificate bound, and bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary frozen-`InNP` verifier normalization, Cook-Levin
  tableaux, both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven SAT and Cook-Levin packages remain open. Their registry entries still freeze planned prose
fingerprints rather than exact Lean declaration types; the exact implemented interface ends at
`CandidateMembership` and `CandidateHardness`. Thus the first failed implementation gate is
`M0721-N-SAT-ENCODING`, and an append-only registry refinement is needed before concrete leaf
bodies can receive proof credit.

Pinned mathlib supplies `TM2ComputableInPolyTime` and its identity implementation, but no NP,
SAT-language, or Cook-Levin endpoint. Its apparent polynomial-time composition declaration is a
source-level `proof_wanted`; trust-zero Lean reports the constant as unknown. Scoped repository,
pinned-dependency, history, and independent proof searches found no inhabitant of either terminal
package. A constant-machine experiment with an altered input encoding, and a failing head-bit
machine experiment, close no frozen obligation and are not included as proof artifacts.

The frozen external audit remains unchanged: its one supporting example lacks an NP endpoint, and
its two headline endpoints are placeholder-dependent or contract-incompatible. Empty, universal,
identity, singleton, fixed-source, and classical-choice witnesses cannot manufacture a universal
polynomial-time reduction. Branching on `source input` would assume a polynomial-time decider not
supplied by arbitrary verifier-based `InNP`.

## Required Split

This run is at least the twenty-fifth dossier-recorded unresolved proof attempt. Blueprint section
10.2 requires a split after five unresolved execution ticks. The integration lane should stop
retrying the monolithic proof item and introduce dependency-legal child proof nodes for the eleven
frozen SAT and Cook-Levin packages, beginning with exact signatures for
`M0721-N-SAT-ENCODING`. This worker did not edit the authoritative DAG or generated checklist.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No dependency update, build,
clone, fetch, checkout, or `.lake` mutation was performed. The immutable anchor validator made
read-only HTTPS requests to replay its three frozen external candidates; no network result is used
as proof closure.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `61f7b690...a4808`, tree `5849148c...e3da`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 with both terminal packages M4. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and freshly downloaded immutable files for all three external candidates matched the frozen audit; root stayed M2 at the candidate-audit boundary. This was discovery replay only, not accepted proof evidence. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 600s lake env lean ../../Stage1_Instances/THM-M-0721/Statement.lean` | 0 | The exact target elaborated normally in the pinned Lake environment. |
| Stream statement lines 1-94 and composition lines 11-26 to `lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and produced no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in owned Lean files. |
| Search other repo-local and pinned-mathlib Lean source for the exact root/packages and NP-completeness endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists outside this dossier. |
| Ask trust-zero Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that `proof_wanted` created no checked declaration. |
| Search all target-history trees for `Proof.lean`, `proof-receipt.json`, or `check_proof` | 1 expected | No historical proof module, proof receipt, or proof checker exists under this target. |
| Query Lean/Lake/dependency identities and hash frozen inputs | 0 | Lean 4.29.0 at `98dc76e3...740`; Lake 5.0.0; mathlib `8a178386...ea95` tree `bdc39a31...c2b`; flt-regular `56161b6e...1a27` tree `32c9eace...c893`; dependency worktrees clean; all recorded hashes matched. |

## Reopen Condition

Append-only refine exact Lean signatures, then implement the eleven frozen SAT and Cook-Levin
packages without placeholders. Alternatively, identify an immutable compatible Lean 4 proof
already present in the pinned closure and exact-type check, transport, and provenance-audit it
without changing the dependency lock.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` remains absent.
