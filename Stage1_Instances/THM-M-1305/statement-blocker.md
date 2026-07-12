# Exact-statement gate: blocked

Item: `S56-M-1305-STATEMENT`  
Theorem: `THM-M-1305`  
Base revision: `c326cc33b70825386f90cf5d885ad451004fbbff`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record contains only the label "Alinhac theorem," attribution to Serge Alinhac, the year 1986, and
the gloss "singularities of nonlinear hyperbolic equations." It supplies no primary publication,
theorem number, page, equation, or exact statement. The accepted intake therefore correctly freezes
the ambiguity rather than selecting one of Alinhac's several results on blow-up and singularities.

The metadata does not determine any of the proposition-changing choices required for a canonical
target:

- scalar equation or system, and its quasilinear or semilinear form;
- space dimension, spacetime domain, operator, and hyperbolicity assumptions;
- initial-data regularity, size, support, and sign or nondegeneracy conditions;
- solution concept, maximal-lifespan quantifiers, and boundary cases;
- the meaning and locus of singularity, including which norm or derivative diverges; or
- whether the conclusion is finite-time blow-up, a lifespan estimate, geometric blow-up, or
  propagation of an existing singularity.

These choices alter domains, ordered binders, hypotheses, and conclusions. Choosing a familiar
theorem from Alinhac's later 1995 book, an unverified 1986 paper, a generic nonlinear-wave blow-up
result, or an abstract interface that assumes singularity formation would broaden or substitute the
unknown theorem. The catalog's untrusted `已验证` label supplies neither source fidelity nor machine
evidence.

The statement gate therefore fails before minimal imports, an elaborated expression fingerprint,
checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary
mutations can be established. No Lean declaration, axiom, placeholder, weakened special case, or
assumed PDE interface was introduced. Machine debt remains `M4`; statement acceptance, audit
completion, and theorem completion remain false.

## Pinned environment and checks

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory
was reused read-only through the existing worker symlink. No update, build, clone, fetch, or other
dependency mutation was run.

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
| `python3 scripts/stage1_target.py show THM-M-1305` | 0 | Rank 473, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the English/Chinese labels, gloss, attribution, and 1995 book title | 0 | Found only underspecified catalog metadata and the existing intake discovery lead; no exact proposition or primary-source transcription |
| pinned-mathlib `rg` search for Alinhac, nonlinear hyperbolic equations, shock formation, and singularity formation | 1 | No matching theorem-specific declaration or source (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check because the exact expression required by
this phase does not exist. Elaborating an invented abstract proposition merely to obtain exit 0
would be fake statement evidence.

## Retry condition

An accountable source review must identify an immutable primary publication and exact theorem/page,
reconcile the claimed 1986 date and any errata, and freeze every equation, domain, solution, data,
quantifier, singularity, and conclusion choice listed above. A later statement run can then encode
that proposition exactly, minimize its pinned imports, fingerprint its elaboration, crosswalk every
source premise and conclusion, and execute all four mutation classes.

The assigned phase is blocked rather than genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
