# Exact-statement gate: blocked

Item: `S56-M-1532-STATEMENT`  
Theorem: `THM-M-1532`  
Base revision: `e291daffd22e3ff6fc8031f413e88a1a41b1af26`

## Decision

The exact Lean 4 target cannot be elaborated truthfully from the accepted intake and repository
source record. The received wording is only "the Standard Model of particle physics." It names a
physical theory, not a proposition with ordered binders, hypotheses, and a conclusion. The dossier
also has no pinned source edition containing a selected theorem-level claim.

Several inequivalent targets could be associated with the name: a field-content and Lagrangian
specification, gauge invariance, anomaly cancellation, a classical equation of motion, a
renormalizability result, a quantum construction, or an empirical prediction. They require
different gauge-group quotient conventions, representations, particle and neutrino content,
parameters, spacetime and regularity assumptions, and classical or quantum semantics. Choosing one
would narrow or substitute the received claim. Experimental confirmation cannot be turned into
Lean kernel proof.

The first failed gate is therefore exact source-statement identity. Without that identity there is
no canonical expression to elaborate, no honest minimal-import set or expression fingerprint, and
no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary-case mutation suite.
No Lean target was created, and no statement, proof, audit-completion, or theorem-completion credit
is claimed.

## Legacy candidate boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_199.lean` elaborates in the pinned environment, but
it is discovery input only. Its `StandardModelData` stores physics-specific assertions such as
Lagrangian construction, anomaly cancellation, and renormalizability as caller-supplied `Prop`
fields. Its `StatementShape` then asks for a conclusion package over that supplied data. This is an
explicit abstract interface, not a source-exact theorem about the Standard Model, and the module's
five direct imports cannot be called minimal for a canonical target that has not been identified.

## Required unblock

An accountable source reviewer must preserve a stable primary source, select an exact theorem,
proposition, or equation with a pinpoint locator, and transcribe its definitions, assumptions,
conventions, conclusion, boundary cases, and errata outcome. The logical force and the treatment of
empirical inputs must be explicit. Only then can a later worker encode the target, minimize pinned
imports, serialize the elaborated expression, check alternate encodings, and execute the required
statement mutations.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean used the existing pinned Lake environment. No
dependency update, build, clone, fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1532` | 0 | rank 199, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_199.lean)` | 0 | legacy abstract interface elaborated; this is candidate inspection only and receives no exact-statement credit |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_199.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `3e0ad1e0...0a57c` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

Known failures are the exact canonical claim, minimal imports, expression fingerprint, checked
alternate transports, and mutation suite. The assigned phase is therefore not self-tested to
completion, so `.stage1-worker-selftest.json` is intentionally absent.
