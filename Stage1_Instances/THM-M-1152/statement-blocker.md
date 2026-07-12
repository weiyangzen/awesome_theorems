# Exact-statement gate: blocked

Item: `S56-M-1152-STATEMENT`
Base revision: `331f3394ba689a537bffbf8764a780c63caecd72`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The complete repository claim is the
title "Perron method" and the gloss "the upper-solution/lower-solution method for the Dirichlet
problem." The intake correctly records that this identifies a construction method, not a unique
proposition. The repository supplies no primary-source theorem/page, inspected text, definition,
hypotheses, or conclusion from which the missing mathematics can be recovered.

In particular, the source does not determine:

- Laplace's equation or a later Perron method for a more general elliptic operator;
- the Euclidean dimension, boundedness or regularity of the domain, and the topology at its boundary;
- the scalar range and the semicontinuity, boundary-liminf/limsup, and order conventions defining
  upper and lower Perron classes;
- continuous boundary data or a generalized resolutive data class;
- nonemptiness and finiteness assumptions for the classes and envelopes;
- harmonicity of one envelope, equality of upper and lower envelopes, attainment at regular
  boundary points, or full existence and uniqueness as the root conclusion.

These choices produce materially different theorems. Choosing a familiar modern formulation,
encoding the conclusion as a field of an abstract Perron structure, or asserting a caller-supplied
`Prop` would broaden or replace the source claim. The nearby Poisson formula, Wiener criterion, and
regular-boundary-point targets do not select this target's scope. The metadata label `已验证` is
explicitly untrusted and cannot do so either.

Therefore the phase stops at the first failed gate, exact human-claim identity. Ordered binders,
hypotheses, conclusion, a minimal import for the target, serialized elaborated expression, checked
alternate transports, and meaningful removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations cannot be produced. No `Statement.lean` is created, and machine debt
remains `M4`.

## Lean discovery boundary

The pinned mathlib snapshot provides `InnerProductSpace.HarmonicAt` and
`InnerProductSpace.HarmonicOnNhd` for functions on finite-dimensional real inner-product spaces.
`StatementInfrastructureProbe.lean` elaborates those declarations using the narrow module
`Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`. A scoped source search found no classical
Perron-method, Perron-Dirichlet, superharmonic, or subharmonic API in pinned mathlib; occurrences of
"Perron" concern the generalized Perron integral or Perron-Frobenius theory.

This proves only that one possible classical harmonicity substrate is available. It neither
defines Perron classes nor selects the source theorem, so the probe import is discovery evidence,
not a claimed minimal import for an exact THM-M-1152 target.

## Required unblock

An accountable source review must inspect an immutable primary edition or scan and record an exact
theorem/page, wording, definitions, hypotheses, conclusion, relevant errata, and translation. It
must resolve every choice above plus empty classes, empty or disconnected domains, irregular
boundary points, constant data, and unbounded domains. A later statement execution can then encode
the source-faithful proposition, minimize imports, serialize its elaborated expression and
environment fingerprint, check alternate encodings, and execute all four mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. Lean reused only the existing `.lake` symlink to
the canonical pinned artifacts. No dependency update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1152` | 0 | rank 357; planned; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1152/StatementInfrastructureProbe.lean)` | 0 | the pinned harmonic substrate elaborated; the three expected declaration types were printed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| scoped `rg` search for Perron/Dirichlet and super/subharmonic declarations in pinned mathlib | 0 | no target API found; unrelated Perron integral and Perron-Frobenius occurrences were classified |
| `git diff --check -- Stage1_Instances/THM-M-1152` | 0 | no whitespace errors |

Known failures are the exact canonical target, target-minimal import determination, expression
fingerprint, checked source transport, and mutation tests. The assigned statement phase is not
self-tested or complete, so no `.stage1-worker-selftest.json` is emitted. This artifact claims no
theorem completion and no credit for any downstream node.
