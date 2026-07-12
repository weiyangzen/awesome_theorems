# Exact-statement gate: blocked

Item: `S56-M-0146-STATEMENT`  
Theorem: `THM-M-0146`  
Base revision: `024dea59d40069399858f4e49dfcadb026874ddb`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository's authoritative record.
That record supplies only the name "Iitaka theorem", Shigeru Iitaka, the year 1971, and the gloss
"Kodaira dimension of algebraic varieties". It supplies no proposition, primary-source theorem or
page, edition, assumptions, or conventions. The intake therefore correctly leaves
`canonical_claim` null and treats Iitaka's *On D-dimensions of algebraic varieties* as an
uninspected discovery candidate rather than an identified statement.

The metadata does not select among materially different claims associated with Iitaka, including a
definition or characterization of the Iitaka dimension, an addition theorem, or another result in
the 1971 paper. It also does not freeze:

- the base field and the class of varieties or schemes;
- irreducibility, normality, completeness, smoothness, or projectivity hypotheses;
- whether the object is a divisor, line bundle, or canonical divisor;
- the section-ring and rational-map formulation;
- the convention for absent plurisections and the value `-infinity`;
- the quantifier order, equality or inequality direction, and degenerate dimensions.

These choices change the domains, binders, hypotheses, and conclusion. Choosing any one of them
would invent or substitute mathematics. In particular, neither a definition packaged as a theorem
nor an abstract predicate that assumes the desired conclusion is an admissible proxy.

Consequently the statement gate fails before minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be produced. No Lean declaration, `sorry`, axiom, opaque placeholder,
weakened special case, or broadened target was introduced. Machine state remains `M4`; statement
acceptance, audit completion, and theorem completion are false.

## Pinned environment and validation

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake`
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
| `python3 scripts/stage1_target.py show THM-M-0146` | 0 | Rank 321, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for Iitaka, Kodaira dimension, D-dimension, and the candidate paper | 0 | Found only the underspecified catalogue metadata, this intake dossier, and unrelated mentions; no source-frozen proposition or legacy target |
| pinned-mathlib `rg` search for Iitaka, Kodaira dimension, D-dimension, and pluricanonical terminology | 1 | No matching source declaration (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0146` | 0 | No whitespace errors |

There is no applicable `lake env lean <target>.lean` command: the exact expression that such a file
would have to contain is precisely what the missing source identity prevents. Compiling an invented
interface would be fake statement evidence rather than validation of the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact theorem/page,
record its wording and errata status, and crosswalk every field, assumption, convention, and
boundary case listed above. It must explain why that theorem, rather than the other Iitaka-related
claims, is the catalogue target. A later statement run can then encode the exact claim, minimize its
pinned imports, fingerprint its elaboration, add checked transports, and run all four required
mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
