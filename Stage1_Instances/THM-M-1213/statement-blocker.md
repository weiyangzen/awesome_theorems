# Exact-statement gate: blocked

Item: `S56-M-1213-STATEMENT`  
Theorem: `THM-M-1213`  
Base revision: `7c261cad5ed43a724864ac5581564164750b865c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical claim is `NLS的局部适定性` (local well-posedness of NLS), accompanied only by
the names Jean Ginibre and Giorgio Velo and the year 1979. The intake records a plausible paper as
a bibliographic discovery candidate, but neither the catalog nor an inspected immutable primary
source selects an exact theorem and page.

The label leaves proposition-changing choices unresolved:

- the spatial domain and dimension, scalar field, and time interval;
- the exact Schrodinger equation, sign convention, nonlinearity, and assumptions on that
  nonlinearity;
- the initial-data space, exponent and regularity ranges, including endpoint policy;
- the solution space and weak, mild, or strong solution notion;
- the quantifier order for the datum, lifespan, and solution;
- the uniqueness class and the topology and uniformity used for continuous dependence;
- whether maximality, blow-up alternatives, persistence of regularity, or conservation clauses
  belong to the selected conclusion;
- the treatment of zero data and other degenerate or boundary cases.

Different choices give inequivalent local well-posedness theorems. Selecting a convenient power
NLS, one dimension, one Sobolev range, an abstract contraction principle, or a proposition that
assumes an unspecified `IsLocallyWellPosed` field would invent or substitute mathematics. The
separately scheduled Cazenave-Weissler critical-regularity theorem (`THM-M-1214`), Bourgain periodic
theorem (`THM-M-1215`), and Ginibre-Velo nonlinear-wave theorem (`THM-M-1222`) also cannot resolve
this target by proximity.

Consequently the canonical human-claim identity gate fails before a minimal import can be chosen,
an expression can be elaborated and fingerprinted, alternate encodings can receive checked
transports, or the required removed-hypothesis, changed-domain, binder-scope, and boundary
mutations can be defined. No Lean declaration, axiom, placeholder, weakened special case, or
broadened interface was introduced. Machine debt remains `M4`; the statement node and theorem
completion remain open.

## Pinned environment and searches

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
artifacts were read only; no update, build, clone, or fetch command was used.

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
| `python3 scripts/stage1_target.py show THM-M-1213` | 0 | Rank 406, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two file hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `THM-M-1213`, `Ginibre-Velo`, and the exact NLS-local-well-posedness gloss | 0 | Found the underspecified source metadata, generated manifest projections, and this intake dossier; no exact proposition or target-specific Lean module |
| pinned-mathlib `rg` search for `Giorgio Velo` and nonlinear Schrodinger terminology | 1 | No target-specific declaration or NLS statement (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command: the exact expression required by the
assigned phase does not exist. Elaborating a generic interface would be fake statement evidence,
not narrow validation of the catalog claim.

## Retry condition

An accountable source review must pin and hash an immutable primary-source edition, select the
exact theorem/page intended by the catalog entry, dispose of errata, and freeze every equation,
domain, dimension, nonlinearity, data and solution space, exponent range, quantifier, uniqueness,
dependence, lifespan, and boundary convention listed above. It must explicitly distinguish the
selection from the neighboring NLS and NLW targets. A later statement run can then encode that
claim, minimize its pinned imports, print and hash the elaborated expression and environment, add
checked transports, and run meaningful structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
