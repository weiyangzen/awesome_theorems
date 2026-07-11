# Statement-phase blocker

Item: `S56-M-1307-STATEMENT`  
Theorem: `THM-M-1307`  
Base revision: `be286e95464895d6966301556151584a57536a1b`

## Verdict

The exact-statement gate is blocked before a canonical Lean declaration can be frozen. The
repository gloss says only "null condition and global existence." The accepted intake identifies
S. Klainerman, "The null condition and global existence to nonlinear wave equations," *Lectures in
Applied Mathematics* 23 (1986), 293-326, as a discovery anchor, but the repository contains no
fixed edition or transcription identifying an exact theorem and all definitions on which it
depends.

The missing source facts include the equation class, semilinear/quasilinear scope, number of
components, coefficient regularity and vanishing order, the exact null-condition formula,
dimension, data regularity and localization or decay, smallness norm, solution class, time domain,
uniqueness, and any asymptotic conclusion. These choices distinguish non-equivalent theorems.
Selecting them from general mathematical knowledge would substitute or broaden the unknown root.
Consequently no truthful canonical expression hash, environment fingerprint, credited alternate
encoding, or removed-hypothesis/domain/binder-scope/boundary mutation suite can be produced.

## Lean boundary

The historical `AwesomeTheorems.Stage1.S1_M_166` module compiles in the pinned environment and
defines useful finite-dimensional Minkowski and null-form scaffolding, but its `KlainermanInput` stores the
nonlinear-term representation, commutator package, weighted energy estimate, decay bootstrap, and
continuation criterion as abstract proposition-valued fields. Its `StatementShape` assumes those
major proof packages and is explicitly documented as a normalization boundary, not a
source-exact theorem. Importing it therefore does not satisfy the rev-5.6 statement gate. Nor does
the module's eight imports establish a minimal import set for a target that has not been identified.
`StatementCandidateProbe.lean` separately confirms that those eight direct mathlib imports and
representative analysis declarations are available; it is infrastructure evidence only.

## Validation record

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` using the existing pinned
Lake environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1307` | 0 | rank 166; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_166.lean` | 0 | historical scaffold elaborated; no terminal theorem is credited |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1307/StatementCandidateProbe.lean` | 0 | eight pinned analysis imports and representative declarations elaborated |
| `git diff --check -- Stage1_Instances/THM-M-1307` | 0 | no output |

## Retry condition

Retry after an authoritative stable copy supplies an exact theorem/page and the surrounding
definitions needed to crosswalk every ordered binder, hypothesis, restriction, and conclusion.
The statement phase can then model exactly that result, minimize imports, serialize the elaborated
expression and pinned environment, check alternate transports, and run all four required mutation
classes.

This artifact does not complete the statement node, accept a receipt, modify the execution DAG, or
claim audit/theorem completion. No `.stage1-worker-selftest.json` is emitted because the assigned
deliverable cannot be genuinely self-tested.
