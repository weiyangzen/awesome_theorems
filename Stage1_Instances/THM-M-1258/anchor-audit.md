# S56-M-1258-ANCHOR_AUDIT receipt

## Audit boundary

The audited root is the exact condition-valued declaration
`Stage1Instances.THM_M_1258.hormanderCondition` from `Statement.lean`. It is not the neighboring
THM-M-1259 hypoellipticity theorem, an elliptic special case, or a claim that every vector-field
family satisfies the bracket-generating condition.

## Pinned candidate inventory

The Lake manifest pins mathlib4 at immutable revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`) with Lean `v4.29.0`. A search over every Lean source
in that pinned package found no occurrence of Hormander/Hörmander, hypoelliptic, subelliptic, or
bracket-generating vocabulary.

| Candidate | Checked role | Exact mismatch with the root |
|---|---|---|
| `VectorField.lieBracket` and elementary identities | Defines the bracket used by `GeneratedBracket` | No generated-family rank predicate and no proof of a span equality |
| `Submodule.span` and `Submodule.span_eq_top_of_span_eq_top` | Supplies the target's linear-span vocabulary | Cannot establish `span = top` for arbitrary field values |

`AnchorAudit.lean` elaborates those exact names against the pin. They are supporting APIs only and
receive no terminal proof-body credit. Repository-local search outside this owned directory found
only legacy statement-shape/analytic-theorem material; none proves this frozen predicate.

## External discovery

On 2026-07-12, GitHub repository searches for `Hormander language:Lean`,
`Hörmander language:Lean`, `hypoelliptic language:Lean`, and
`bracket generating language:Lean` each returned `total_count: 0`. Each response had SHA-256
`08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2`. No candidate therefore
existed to pin and inspect for type, terminal body, dependencies, axioms, placeholders, toolchain,
or license. A fifth GitHub query hit HTTP 403, and the attempted grep.app queries hit HTTP 429;
these are recorded limitations rather than successful negative evidence.

The result is bounded: it does not rule out private, unindexed, differently named, or future work.
No dependency was fetched, cloned, updated, or added.

## Verdict

The anchor inventory is complete for this node and self-tested, with terminal candidate `null`.
Debt remains `[H2, M4, R4]`. In particular, a condition parameterized by arbitrary fields is not a
universally true theorem awaiting a generic proof. A later concrete instance would need its own
construction or span hypothesis. This receipt makes no proof or theorem-completion claim.

