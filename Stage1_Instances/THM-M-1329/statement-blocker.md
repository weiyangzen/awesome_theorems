# Exact-statement gate: blocked

Item: `S56-M-1329-STATEMENT`  
Theorem: `THM-M-1329`  
Base revision: `b1720c87b4674563b995fad5e6dd9828348b7230`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The entire mathematical statement supplied for Robert Brooks's 1981 result is "volume growth and
the essential spectrum." No primary-source edition, theorem/page, quotation, or errata record is
attached. The intake dependency consequently freezes only the theorem family and the vector
`[H4, M4, R4]`, not a proposition.

Several choices that change the proposition remain unresolved:

- connectedness, completeness, dimension, boundary, and finite- versus infinite-volume hypotheses;
- the basepoint, metric-ball volume, exponential-growth normalization, and limsup/liminf choice;
- the sign and self-adjoint realization of the Laplace-Beltrami operator;
- the definition and empty-spectrum convention for the bottom of the essential spectrum; and
- the inequality direction, numerical constant, exceptional cases, and whether the source result
  has more than one direction.

Selecting a familiar inequality from memory would manufacture the missing mathematics. Replacing
the source result with an abstract theorem over supplied `volumeGrowth` and `essentialSpectrum`
functions would broaden it, while placing the desired relation in a structure or hypothesis would
make the eventual proof circular. None is an exact encoding of the unidentified source theorem.
The neighboring `THM-M-1328` generic volume-growth entry and Rowland Brooks graph-coloring target
`THM-M-0858` do not resolve this identity.

The pinned mathlib source has Riemannian-manifold infrastructure, but the scoped search found no
declaration for essential spectrum, the bottom of a Laplacian spectrum, Laplace-Beltrami spectrum,
or the Brooks volume-growth result. This is an additional encoding/infrastructure boundary, not a
license to substitute an easier statement.

The phase therefore fails at canonical human-claim identity, before minimal imports, a canonical
Lean expression, expression fingerprint, checked alternate transports, or meaningful removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations exist. No Lean declaration,
axiom, placeholder, assumed theorem, or weakened specialization was introduced. Statement
acceptance and theorem completion remain false.

## Validation evidence

Commands ran from the worker-clone root on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were read only; no update, build, clone, or fetch was run.

- Toolchain: `leanprover/lean4:v4.29.0`; Lean commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1329` | 0 | rank 491, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for Robert Brooks and the exact English/Chinese gloss | 0 | found only the underspecified catalogue record and its Stage0 projection outside this dossier |
| pinned mathlib `rg` search for essential spectrum, bottom-of-spectrum/Laplacian combinations, Laplace-Beltrami, and volume growth | 1 | no matching source declaration or module |

There is no applicable `lake env lean <canonical-statement>.lean` check: no exact proposition has
been identified. Creating a candidate file would be fake elaboration evidence rather than the
assigned deliverable.

## Retry condition

An accountable source review must preserve an immutable primary edition, transcribe the exact
theorem and surrounding definitions, resolve corrections or errata, and freeze every convention
listed above. A later statement run can then encode that claim (adding honestly scoped spectral
infrastructure if required), minimize pinned imports, serialize the elaborated expression and
environment, check alternate transports, and run all four mutation classes.

This artifact records the first failed gate. It does not complete the statement node, accept a
receipt, alter the execution DAG, or claim audit/theorem completion. The assigned phase is not
genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
