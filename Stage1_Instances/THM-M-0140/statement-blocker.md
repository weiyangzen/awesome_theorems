# THM-M-0140 statement-phase blocker

Item: `S56-M-0140-STATEMENT`  
Theorem: `THM-M-0140`  
Base revision: `8e9399a4a89f54acc9f9d6436447a0a77238bed1`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The intake selects the
existence and uniqueness of the Kazhdan-Lusztig canonical basis for the generic one-parameter Hecke
algebra of a Coxeter system, but its only source locator is the whole of Section 1 of the 1979
Kazhdan-Lusztig paper. It does not pinpoint the defining result or freeze the paper's parameter,
quadratic relation, standard-basis normalization, bar involution, coefficient lattice, or which of
the commonly exchanged `C_w` and `C'_w` conventions is canonical. The intake explicitly leaves
those choices to this phase and supplies no checked convention transport.

Those choices change the ordered binders and the actual triangularity formula, rather than merely
changing notation. Selecting one without an exact source transcription and premise-level
crosswalk would invent missing mathematics. Consequently there is no source-faithful expression
to serialize and no legitimate removed-hypothesis, changed-domain, binder-scope, or boundary
mutation suite to run.

The pinned mathlib snapshot supplies `CoxeterMatrix`, `CoxeterSystem`, simple reflections, word
products, reduced words, and Coxeter length. Repo-local search found no Coxeter Bruhat-order or
Hecke-algebra construction and no Kazhdan-Lusztig basis declaration in that dependency closure.
The historical `AwesomeTheorems.Stage1.S1_M_056.StatementShape` does not resolve the gap: it stores
the Hecke algebra, Bruhat relation, triangularity, normalization, and required conditions as
unconstrained abstract fields. Accepting it would substitute a weaker interface theorem for the
named mathematical result.

`StatementInfrastructure.lean` therefore checks only the uncontroversial pinned Coxeter API. It
declares no canonical theorem or proxy proposition. The first failed gate is exact
source-statement identification, followed by the absent concrete object model. The node remains
open at `M4`; no statement or theorem completion is claimed.

## Environment

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

All commands ran in this worker clone. Lean used the existing pinned Lake environment; no update,
fetch, clone, or dependency build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0140/StatementInfrastructure.lean` | 0 | six Coxeter-system declarations elaborated and printed |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_056.lean` | 0 | historical abstract interface and adjacent Coxeter anchors elaborated; no exact-target credit |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact expected mathlib revision |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0140` | 0 | rank 56, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'sorry\|admit\|axiom\|placeholder\|fake results' Stage1_Instances/THM-M-0140/StatementInfrastructure.lean` | 1 | expected no-match exit; the checked Lean artifact contains none of the forbidden devices |
| `git diff --check -- Stage1_Instances/THM-M-0140` | 0 | no whitespace errors in the owned-path changes |

## Retry condition

Provide an immutable primary-source copy and pinpoint the exact existence/uniqueness result, then
freeze its parameter and basis conventions with a premise-level transcription. A later statement
run can define or import the corresponding Hecke and Bruhat objects, check transports between any
credited normalization variants, serialize the elaborated expression, and run the required
mutations.

Because the assigned statement phase is blocked rather than self-tested to completion, no
`.stage1-worker-selftest.json` is emitted.
