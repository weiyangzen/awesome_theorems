# THM-M-1551 statement-phase blocker

Item: `S56-M-1551-STATEMENT`  
Base revision: `057a073c6e854b6552236ab330b9de2e388d24ea`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The accepted intake bounds
the claim family as compatibility/flatness for an auxiliary linear system, but it deliberately
leaves open the concrete integrable equation, coefficient space, matrix size or Lie algebra,
independent-variable domain, regularity, derivative convention, operator order, commutator sign,
spectral-parameter domain and quantification, and whether compatibility is pointwise, formal, or
an operator identity. These choices change the proposition, its ordered binders, hypotheses, and
boundary cases. The repository source record supplies only the phrases "zero-curvature
representation" and "gauge theory of integrable systems"; it contains no reviewed exact theorem
transcription, equation anchor, convention crosswalk, or errata decision from which those choices
can be recovered without selecting a different theorem on the repository's behalf.

The two primary-source candidates recorded at intake, Zakharov-Shabat (1974) and
Ablowitz-Kaup-Newell-Segur (1974), describe families of auxiliary problems rather than resolving
which concrete member this repository UID denotes. Choosing either candidate and one of its
systems would narrow the generic repository label and would overlap the separately tracked
`THM-M-1557` (Zakharov-Shabat system) or `THM-M-1558` (AKNS system). That is a material theorem
selection, not statement normalization.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean` elaborates in the
pinned environment, but it is negative boundary evidence rather than the exact target. It replaces
partial derivatives of coefficient functions by arbitrary linear endomorphisms of an abstract Lie
algebra and defines `LaxCompatibilityEquation` as the algebraic rearrangement
`Dx V + [U,V] = Dt U`. Its `ZeroCurvatureRepresentationStatement` therefore asserts only that this
rearranged equality implies the definitionally selected curvature equality. It has no auxiliary
wavefunction, commuting mixed evolutions, spectral parameter, concrete nonlinear equation, or
checked bridge to a primary-source system. Copying that declaration would substitute an abstract
tautological wrapper for the intake-selected source theorem.

First failed gate: rev-5.6 section 5 exact human-claim and source-statement identification, before
the Lean 4 statement gate in section 5.1. The statement node remains open at `M4`; there is no
canonical declaration, normalized-expression fingerprint, minimal exact-target import list,
checked alternate transport, or valid four-class mutation suite. Retry only after an accountable
source decision identifies one exact auxiliary system and freezes every convention above,
including constant-potential, zero-potential, and spectral-boundary behavior. No statement
acceptance, proof credit, audit completion, or theorem completion is claimed.

## Commands and results

All commands ran in this worker clone. The Lean check reused the canonical pinned `.lake` artifacts
through the worker link. No update, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1551` | 0 | Rank 210, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_210.lean` | 0 | Legacy abstract boundary module elaborated; this does not elaborate an exact source-controlled zero-curvature theorem |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean` | 0 | SHA-256 values `651c8a...b1d2`, `321626...2d81`, and `bb147a...a8b` respectively |
| `rg -n -i 'zero.?curvature\|Zakharov\|Shabat\|Ablowitz\|Kaup\|Newell\|Segur' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1551/**'` | 0 | Found the generic metadata, separate ZS/AKNS targets, legacy abstract wrappers, and incidental mentions; no reviewed exact source transcription for this UID |

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than genuinely self-tested.
