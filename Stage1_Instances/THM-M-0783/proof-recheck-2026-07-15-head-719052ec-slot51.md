# THM-M-0783 proof recheck at `719052ec` (slot51)

Item: `S56-M-0783-PROOF`  
Intent: `prove`  
Recorded: `2026-07-15T14:37:58+08:00`  
Base revision: `719052ec5fae5190f38e013d646fd7461d29be5d`  
Base tree: `a8de041884ae39d41031493cb436b3e4a66bbfa0`

## Verdict

`blocked`. No placeholder-free proof body for the exact proposition
`Stage1Instances.THM_M_0783.MartinsAxiom` exists in the repository-local pinned dependency closure.
Martin's axiom is an additional set-theoretic axiom, not a theorem derivable from the selected
Lean/mathlib foundation. Blueprint section 3.1 classifies this target as `H5`, which blocks ordinary
theorem-proof execution and requires target redirection rather than a manufactured proof.

The substantive leaf `M0783-L-DENSE-FAMILY` is definitionally `ExpandedMartinsAxiom`, so it is the
entire missing content: uniformly for every cardinal below the continuum, it must construct a
filter meeting every suitably bounded dense family in every nonempty ccc partial order. The existing
`root_of_denseFamilySolver` consumes exactly that proposition as a premise and transports it to the
canonical target. It is valid conditional composition evidence, not an unconditional proof body.

Pinned mathlib does contain the Rasiowa-Sikorski construction for an `Encodable` family in
`Mathlib/Order/Ideal.lean`, but that proves only the countable-family boundary. The frozen target
quantifies over every family of size at most every cardinal strictly below the continuum, so the
countable theorem cannot close or replace it.

This attempt does not introduce the target with `axiom`, a bodyless declaration, or a premise; use a
placeholder; weaken the cardinal, ccc, order, density, family, or filter contract; or substitute a
relative-consistency, independence, countable-family, or consequence theorem. Those routes would
change the foundation or target and cannot satisfy the assigned proof phase.

The item remains `[ ]`, lifecycle remains `planned`, and the root remains `[H5, M4, R4]`. No proof
receipt, worker `[_]`, accepted state, audit completion, theorem completion, validation, release, or
master acceptance is claimed. Because the requested positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate

The first failed gate is exact kernel closure of `M0783-L-DENSE-FAMILY` without placeholders,
undeclared premises, or a foundation extension. The proof-relevant cut is:

```text
M0783-L-DENSE-FAMILY
```

The full frozen cut additionally contains `M0783-X-SOURCE`, `M0783-X-FOUNDATION`,
`M0783-X-PROVENANCE`, `M0783-X-READABLE`, and `M0783-X-WORKFLOW`. A retry requires an immutable,
license-compatible Lean 4 terminal body for the exact target with acceptable exact-type, axiom,
placeholder, provenance, and composition reports. Alternatively, the master must redirect this
additional axiom to a theory-extension, consistency, or independence target. That is a target-policy
correction, not proof completion.

## Narrow Validation

The automation-provided `Formalizations/Lean/.lake` symlink was treated as read-only. No `lake
update`, `lake build`, dependency clone/fetch, or checkout repair was run. Narrow elaboration invoked
the pinned Lake executable from the target directory and supplied only existing pinned package
object directories through `LEAN_PATH`; temporary output was created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0783/check_statement.py` | 0 | canonical expression hash `c5896a33...5599ada`; all four structural mutations were killed; pinned Lean 4.29.0 and mathlib `8a178386...ea95` |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open M4 |
| `python3 Stage1_Instances/THM-M-0783/check_anchor_audit.py` | 0 | anchor boundary, six probes, statement status, and pinned mathlib revision passed |
| pinned `lake env lean --trust=0 -t0` on `Statement.lean` with read-only object-directory `LEAN_PATH` and isolated temporary output | 0 | exact canonical target elaborated; `Statement.olean` SHA-256 `a3bd8eef...415c6`; temporary output removed |
| same pinned `lake env lean` route on `ObligationTree.lean` | 0 | conditional composition elaborated; axiom report exactly `[propext, Classical.choice, Quot.sound]`; olean SHA-256 `0098b71d...f550`; temporary output removed |
| scoped prohibited-construct scan of owned Lean source | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, unsafe/oracle escape, or proof placeholder |
| scoped exact-candidate scan across installed pinned package Lean sources | 1 | expected no-match: no Martin's-axiom, forcing-axiom, or dense-family-solver declaration was found |
| scoped `forcing` scan in pinned mathlib | 0 | only unrelated model-theory documentation, order-ideal commentary, and incidental prose |
| `git diff --check -- Stage1_Instances/THM-M-0783 .stage1-worker-selftest.json` | 0 | no whitespace errors in the target-scoped handoff artifacts |

The successful Lean commands validate the exact statement and the already frozen conditional
child-to-root composition. They are evidence for this blocker boundary, not a proof of Martin's
axiom. Exact structured details and hashes are recorded in the sibling JSON artifact.
