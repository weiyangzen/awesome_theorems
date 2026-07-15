# THM-M-0324 proof-phase execution

Item: `S56-M-0324-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `be2be0dfe2f4f2cbdd35f1f2397e5a372d199eb9`

## Verdict

`blocked`. This execution adds a real placeholder-free Schauder-projection
proof branch, but it does not construct Enflo's counterexample space or prove
failure of the exact source-faithful approximation property. The exact target
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open, the root
vector remains `[H1, M3, R4]`, and no proof receipt or completion self-test is
emitted.

## Implemented bodies

`Proof.lean` defines a sequential finite-rank approximation package whose
approximants converge to the identity uniformly on every compact set. It then
proves:

| Declaration | Exact contribution | Boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Uses `SchauderBasis.proj`, `range_proj_eq_span`, uniform boundedness, equicontinuity, and Ascoli to build the compact-convergence package | Real substrate for `M0324-L-PROJECTIONS` and `M0324-L-BASIS-TO-AP`; source identification of `M0324-D-APPROX` remains open |
| `noSchauderBasis_of_not_compactApproximationProperty` | Specializes the frozen logical composer to show failure of the local property excludes every Schauder basis | Assumes property failure and supplies no Enflo witness or `M0324-L-NO-AP` proof |

Both declarations elaborate at trust level zero and report only `propext`,
`Classical.choice`, and `Quot.sound`. They contain no `sorry`, `admit`, axiom
declaration, unsafe declaration, oracle, or substituted root.

## Failed gate

The first unavailable construction is `M0324-C-SPACE`: the repository and
pinned dependency closure contain no implementation of Enflo's counterexample.
Consequently the Banach packaging, separability, infinite-dimensionality, and
failure-of-approximation packages remain open. The source gate also has not
fixed and independently crosswalked the exact approximation-property convention,
so this execution does not relabel its local technical predicate as Enflo's
source theorem.

The remaining root cut recorded by the frozen architecture begins with
`M0324-C-SPACE`, `M0324-X-SOURCE`, and `M0324-X-FOUNDATION`. Assuming any open
package, treating the conditional composer as a root body, or using a merely
nonseparable shortcut would violate the exact-target and placeholder gates.

## Validation

All commands ran in this worker clone with the pre-existing pinned Lake
artifacts reused read-only. No `lake update`, `lake build`, dependency fetch or
clone, network request, or `.lake` mutation was performed. Lean outputs were
created only in a disposable directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| Disposable trust-zero Lean replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | `statement_exit=0 obligation_exit=0 proof_exit=0`; exact target and both composers elaborated; the new declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| The same disposable replay invoked through `lake env lean` | 1 | Lake stopped before Lean execution because the pre-existing pinned package `flt-regular` could not resolve `HEAD`; no dependency repair or mutation was attempted |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | Frozen registry remained structurally valid with 15 obligations and 55 typed edges; root open at `M3` |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected no-match) | No prohibited proof device found |
| `python3 -m json.tool Stage1_Instances/THM-M-0324/proof-blocker.json` | 0 | Structured blocker parsed |
| `git diff --check -- Stage1_Instances/THM-M-0324` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is incomplete |

The disposable replay used the pinned Lean 4.29.0 executable with `--trust=0
-t0`, an explicit `LEAN_PATH` made from the existing package build artifacts,
and a temporary module directory containing copies of the three owned modules.
This direct invocation was necessary because Lake currently inspects the
unrelated broken `flt-regular` Git metadata before launching Lean. It uses the
same pinned compiler and existing package oleans and does not fetch or alter a
dependency; the Lake failure remains recorded as a nonrelease environment
limitation.

## Reopen condition

Resume after implementing Enflo's construction and every downstream analytic
package without placeholders, with the exact source convention crosswalked.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact target and re-run exact-type, trust, provenance, and
composition checks.

This packet is partial proof work plus blocker evidence. It does not satisfy
the assigned proof item, promote scheduler state, close the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance,
or master acceptance. Because the phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
