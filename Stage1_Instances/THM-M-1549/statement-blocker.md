# THM-M-1549 statement-phase blocker

Item: `S56-M-1549-STATEMENT`  
Base revision: `535a525f487a46804fc0abc236b3e993110c3c9d`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository source record
contains only "inverse scattering transform," Gardner/Greene/Kruskal/Miura, 1967, and "a method for
solving the KdV equation." The intake identifies the 1967 *Physical Review Letters* paper as a
historical anchor, but no repository artifact contains an independently reviewed exact theorem
transcription, theorem/page locator, premise map, or errata decision. The intake therefore
deliberately leaves the following statement-changing choices open:

- the sign and constants in KdV and in the associated Schrodinger/Lax operator;
- the initial-potential space, differentiability, decay moments, and real-valuedness assumptions;
- the time domain and the classical, strong, or weak solution class;
- zero-energy resonance, bound-state multiplicity, and other spectral restrictions;
- reflection, eigenvalue, norming-constant, and Marchenko-kernel normalizations;
- existence alone versus existence and uniqueness, and the topology in which the initial value is
  attained; and
- treatment of zero, reflectionless, and no-bound-state data.

These choices change the domains, ordered binders, hypotheses, conclusion, and boundary cases.
Selecting them from general knowledge would invent missing mathematics, while reducing the claim
to a soliton, Lax identity, or abstract reconstruction interface would substitute a weaker theorem.
Consequently there is no canonical declaration, elaborated-expression fingerprint, minimal import
list for the exact target, checked alternate transport, or valid removed-hypothesis/domain/scope/
boundary mutation suite.

## Lean boundary evidence

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_208.lean` elaborates in the pinned
environment, but it is not the exact target. Its `InverseScatteringModel` stores
`reconstruction_solves_kdv` and `reconstruction_matches_initial` as proof-bearing structure fields.
Its `StatementShape` merely projects those assumed conclusions for an arbitrary model. It does not
define the one-dimensional Schrodinger scattering problem, prove direct or inverse scattering,
state the Marchenko reconstruction theorem, or freeze the analytic assumptions above. The module's
nine imports are therefore legacy discovery inputs, not a minimal import closure for an exact
source theorem. Its successful elaboration earns no statement or proof credit.

The first failed gate is rev-5.6 exact source-statement identification, before canonical Lean
elaboration. The node remains open at `M4`. Retry after an immutable rigorous source theorem is
selected and independently reviewed with exact locator, definitions, assumptions, conventions,
conclusion, errata status, and degenerate-case policy.

## Commands and results

All commands ran in this worker clone. Lean reused the existing pinned `.lake` artifacts. No Lake
update/build, dependency fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1549` | 0 | Rank 208, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_208.lean` | 0 | Legacy abstract-model boundary elaborated; this does not elaborate the exact IST theorem |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_208.lean` | 0 | SHA-256 values `651c8a...b1d2`, `321626...2d81`, and `def0cf...3ff` respectively |
| repository-local `rg` search for IST/KdV/Marchenko/source-author terms, excluding `.lake` and this dossier | 0 | Found the terse source metadata, generated Stage1 description, legacy boundary module, and neighboring KdV material; no reviewed exact theorem transcription |

No statement acceptance, receipt, audit completion, or theorem completion is claimed. No
`.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than genuinely self-tested.
