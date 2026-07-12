# Exact-statement gate: blocked

Item: `S56-M-1049-STATEMENT`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The accepted intake
records `canonical_statement_status` as `unresolved_theorem_family` and leaves
the formal module, declaration, expression hash, and environment fingerprint
unset. The repository metadata supplies only "martingale characterization of
diffusion processes." It does not identify a primary-source theorem, page, or
complete hypotheses. The intake crosswalk consequently leaves four
non-equivalent possible roots:

1. weak SDE solution implies a martingale-problem solution;
2. a martingale-problem solution yields a weak SDE realization;
3. equivalence of weak solutions and martingale-problem solutions; or
4. existence and uniqueness under a particular coefficient regime.

Those alternatives also leave unresolved the state space, coefficient
regularity and ellipticity, explosion convention, initial point versus initial
law, test-function class, local versus true martingale status, and the precise
law-equality conclusion. Choosing any one without a pinpointed source decision
would substitute a nearby theorem for the manifest's unidentified theorem
family. Section 5 of the rev-5.6 standard makes statement ambiguity and a
missing expression fingerprint hard blockers.

## Legacy Lean artifact

The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_242.lean` elaborates in the
pinned environment, but it cannot close this gate. Its `MartingaleProblemData`
stores the central mathematical content in unconstrained proposition fields:
`diffusionGeneratorShape`, `accumulatedGeneratorIsIntegral`,
`pathRegularity`, `martingaleProblemWellPosed`, and
`transitionLawCharacterizesProcess`. Its `StroockVaradhanHypotheses` assumes
both `martingaleProblemWellPosed` and `SolvesMartingaleProblem`; its conclusion
then repeats those properties and requests the opaque
`transitionLawCharacterizesProcess` field. Thus `StatementShape` is a typed
shell around caller-supplied propositions, not a source-exact encoding of a
Stroock-Varadhan theorem.

Crediting that shell would broaden the hypotheses and make the intended
characterization circular. It also has six direct imports, so successful
elaboration does not establish the required minimal-import result. The legacy
module remains discovery evidence only.

## Validation record

Base revision: `ab44bba1a95810115e765744d2ee1b5b92ebcf35`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1049` | 0 | rank 242; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_242.lean` | 0 | legacy shell and its printed declaration checks elaborate; this is not an exact-statement result |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-1049` | 0 | no whitespace errors after this record was added |

The Lean checks used the existing canonical `.lake` link. No dependency update,
fetch, clone, or build was performed.

## Gate result and retry condition

First failed gate: exact canonical statement identity. Because no one
mathematical proposition is frozen, there is no truthful canonical Lean
expression, expression fingerprint, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutation suite. Machine debt remains
`M4`.

Retry only after an authoritative primary-source transcription or explicit
source decision fixes one theorem and all of the conventions above. The Lean
encoding must then define the generator, compensator, regularity, and law
conclusion rather than accept their truth as fields.

This assigned phase is not self-tested as complete, so no worker self-test
manifest is emitted. No proof, downstream phase, or theorem completion is
claimed.
