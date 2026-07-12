# Exact-statement gate: blocked

Item: `S56-M-1263-STATEMENT`  
Theorem: `THM-M-1263`  
Base revision: `0e82a3864b3f40086db1c16ddc59d35e64cbf5d7`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical statement is the phrase "wavefront sets and propagation of singularities";
the associated metadata adds only Lars Hormander and the 1970s. It supplies no primary-source
edition, theorem number, page interval, exact wording, or accepted errata. The intake's reference
to chapter XXVI of *The Analysis of Linear Partial Differential Operators III* is explicitly a
discovery-family reference, not a selected and inspected source theorem.

The phrase denotes several inequivalent results and does not determine:

- differential versus pseudodifferential operators, their order, proper-support conditions, or
  scalar versus bundle-valued setting;
- the manifold and cotangent-bundle hypotheses, symbol convention, characteristic set, or precise
  meaning of real principal type;
- ordinary versus Sobolev wavefront sets and, in the latter case, the regularity indices and order
  shift for the forcing term;
- local propagation in a conic neighborhood, invariance along a bicharacteristic segment, or the
  global union-of-maximal-bicharacteristics corollary;
- the quantifier order and maximality/existence assumptions for Hamilton integral curves;
- treatment of elliptic points, stationary Hamilton fields, radial points, boundary phenomena,
  and points in the wavefront set of the forcing term.

Each choice changes the domains, binders, hypotheses, or conclusion. Encoding a generic set as
flow-invariant, assuming an abstract propagation predicate, choosing the smooth-forcing corollary,
or substituting elliptic regularity would therefore weaken, broaden, or invent the target. No such
proxy declaration, axiom, or assumed analytic interface was introduced.

Consequently the canonical human claim fails before minimal imports can be selected. There is no
expression to elaborate or fingerprint, no source-faithful alternate encoding to transport, and
no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary mutation suite. The
machine debt remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing pinned `.lake` artifacts were read only; no
update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1263` | 0 | rank 440; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese title, English theorem family, wavefront sets, and principal type | 0 | found only the underspecified Stage0/research metadata, generated target records, this intake, and unrelated target prose; no source-frozen proposition |
| pinned-mathlib `rg` search for wavefront sets, pseudodifferential operators, microlocal analysis, bicharacteristics, principal type, and cotangent Hamiltonian dynamics | 1 | no matching microlocal-analysis API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check because the exact target does not exist.
Elaborating an invented abstract interface would be false evidence rather than the requested
minimal-import elaboration.

## Retry condition

An accountable source review must select an immutable primary-source edition and pinpoint theorem,
inspect its surrounding definitions and errata, and freeze every operator, symbol, wavefront,
regularity, Hamilton-flow, locality, and boundary convention listed above. A later statement run
can then transcribe the exact ordered binders and conclusion, identify minimal pinned imports (or
record missing formal infrastructure), serialize the elaborated expression and environment, check
alternate transports, and execute all four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
