# Exact-statement gate: blocked

Item: `S56-M-1190-STATEMENT`  
Theorem: `THM-M-1190`  
Base revision: `31b7ab5b3902c4a80878c2007218f90566a8b85c`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its complete mathematical wording is the title "heat-equation L^p estimate" and the phrase
"L^p theory for parabolic equations". No primary source, edition, theorem/page, definitions, exact
hypotheses, or conclusion is supplied. The intake consequently and correctly leaves the canonical
claim ambiguous at `[H4, M4, R4]`.

The source wording does not determine any of the following statement data:

- the heat operator or more general parabolic operator, including coefficient hypotheses;
- spatial dimension, time interval, domain, initial data, and boundary conditions;
- weak, mild, or strong solution notion and the forcing/data spaces;
- the exponent range and treatment of `p = 1` or `p = infinity`;
- whether the result is semigroup contractivity, an `L^p-L^q` smoothing estimate, maximal
  parabolic regularity, or another inequivalent form of `L^p` theory;
- the exact norm inequality, derivative orders, constant dependencies, and local/global scope.

Those choices change domains, ordered binders, hypotheses, boundary cases, and the conclusion.
Choosing any one of them would substitute a convenient theorem for the unidentified source claim.
The title also narrows to the heat equation while the statement phrase broadens to parabolic
equations; the repository provides no authority for resolving that mismatch. The metadata label
`已验证` is explicitly untrusted and is neither human-source nor kernel evidence.

Therefore this phase fails at canonical human-claim identity, before a minimal import, elaborated
expression hash, checked alternate encoding, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutation suite can exist. No Lean declaration, axiom, placeholder,
weakened special case, or broadened abstract interface was introduced. Machine state remains `M4`;
statement acceptance, audit completion, and theorem completion remain false.

## Pinned environment and narrow validation

Commands ran from this worker clone on 2026-07-12. The canonical `.lake` artifacts were used read
only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
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
| `python3 scripts/stage1_target.py show THM-M-1190` | 0 | rank 384, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | pinned Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | pinned Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository and pinned-mathlib `rg` search for heat-equation `L^p`, parabolic `L^p`, and maximal parabolic regularity | 0 | no target-specific declaration; the only match was unrelated parabolic-boundary vocabulary in a legacy module |

There is no applicable `lake env lean <target>.lean` command: the exact expression required by the
assigned deliverable is missing. Elaborating a self-chosen estimate or an abstract structure that
assumes the desired result would be fake statement evidence rather than validation.

## Retry condition

An accountable source reviewer must identify an immutable primary source and exact theorem/page,
resolve the heat-versus-parabolic scope mismatch, and freeze every operator, domain, coefficient,
solution, data, exponent, norm, constant, locality, endpoint, and boundary choice listed above.
A later statement run can then encode that exact claim, minimize pinned imports, serialize the
elaborated expression and environment, check alternate transports, and execute all four mutation
classes.

The assigned statement phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. This artifact records the actionable blocker only and
claims no node acceptance or downstream credit.
