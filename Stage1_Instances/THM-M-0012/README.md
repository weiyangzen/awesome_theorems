# THM-M-0012 Historical Dossier

`THM-M-0012` is a retained `planned` instance for the fundamental theorem of algebra:
every nonconstant univariate complex polynomial has a complex root. The statement phase freezes
that conventional repository scope as
`Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget`, with nonconstant meaning outside
the image of `Polynomial.C` and root meaning `Polynomial.IsRoot` in `Complex`.

## Intake boundary

- Manifest rank: 1062; legacy slot: none.
- Lane: `hard_statement_first_partial_verification`; baseline: `L0 / rework_required`.
- Lifecycle: `planned`; accepted proof/task state: none.
- Root vector: `H1 / M3 / R4`.
- Audit complete: false; theorem complete: false.

The exact target elaborates with the sole direct import
`Mathlib.Analysis.Complex.Polynomial.Basic`. Checked iff witnesses connect it to the positive-degree
shape adjacent to `Complex.exists_root` and to evaluation at zero. Four structural mutations and
the zero, constant, and linear boundaries are checked. This is statement evidence only: the
candidate theorem body, provenance, trust closure, and source fidelity receive no proof credit.

## Open execution route

| Task | Required output | State |
|---|---|---|
| `S56-M-0012-STATEMENT` | Elaborate the exact target and mutation-test its scope | self-tested; master acceptance pending |
| `S56-M-0012-ANCHOR_AUDIT` | Audit formal candidates, bodies, revisions, imports, and trust boundaries | open; depends on statement |
| `S56-M-0012-OBLIGATION_TREE` | Freeze obligations and typed graphs before closure metrics | open; depends on audit |
| `S56-M-0012-PROOF` | Integrate and replay an admitted exact machine proof; new root work requires an active reviewed frontier exception | open; depends on tree and focus permission |
| `S56-M-0012-VALIDATION` | Run hermetic kernel, provenance, trust, and independent gates | open; depends on proof |
| `S56-M-0012-RELEASE` | Independently reconcile audit and theorem completion | open; depends on validation |

The first downstream retry condition is an immutable formal-candidate and proof-body provenance
audit. Pinpoint primary-source fidelity remains independently open on the H axis.

## Validation boundary

The statement validation record checks the exact expression fingerprint, environment, transports,
mutations, boundaries, dossier consistency, prohibited constructs, and whitespace. It reuses the
automation-provided canonical `.lake` artifacts read-only; no update, build, fetch, or dependency
mutation was run. This is provisional worker self-test evidence pending master acceptance, not an
accepted receipt or theorem-completion claim.
