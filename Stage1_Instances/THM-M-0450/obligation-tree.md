# THM-M-0450 frozen obligation architecture

Item: `S56-M-0450-OBLIGATION_TREE`.

The registry freezes fourteen root-relevant obligations before proof execution.
It follows the weak-Mordell-Weil plus height-descent route exposed by pinned
mathlib. The architecture is an inventory, not evidence that its open premises
are true.

## Typed proof route

```text
M0450-ROOT exact canonical proposition
`-- M0450-T-ASSEMBLE checked conditional descent
    |-- M0450-B-WEAKMW finite index of doubling
    |   |-- M0450-B-KUMMER construct and control descent map
    |   |   `-- M0450-X-TRANSPORT checked model transport
    |   `-- M0450-B-QUOTIENT finite descent target
    `-- M0450-H-HEIGHT elliptic height package
        |-- M0450-H-NONNEG nonnegative normalization
        |-- M0450-H-PARALLEL approximate parallelogram law
        |-- M0450-H-NORTHCOTT bounded-height finiteness
        `-- M0450-X-TRANSPORT checked model transport
```

`M0450-S` records the exact statement encoding. `M0450-X-SOURCE`,
`M0450-X-PROVENANCE`, and `M0450-X-TRUST` remain separate source, provenance,
and trust boundaries and cannot be counted as mathematical proof premises.

## Semantic ledgers

| ID | Premises and inference | Output and use | Budget/status |
|---|---|---|---|
| `M0450-ROOT` | Exact number-field, elliptic, Jacobian-point binders | `AddGroup.FG E.toJacobian.Point`; terminal root | 20, open M3 |
| `M0450-S` | Statement imports and mutation-tested binder boundary | Frozen target fingerprint; refines root | 30, checked locally |
| `M0450-T-ASSEMBLE` | Weak MW and height package for each elliptic curve | Apply `AddCommGroup.fg_of_descent'`; feeds root | 20, checked conditionally |
| `M0450-B-WEAKMW` | Descent-map construction and finite target | Finite index of doubling; feeds assembly | 80, open |
| `M0450-B-KUMMER` | Number-field and elliptic hypotheses plus model transport | Controlled Kummer/descent map | 100, open |
| `M0450-B-QUOTIENT` | Arithmetic ramification/unit/class-group controls | Finite target containing `E(K)/2E(K)` | 100, open |
| `M0450-H-HEIGHT` | Three height laws and transported point model | `HeightPackage K E`; feeds assembly | 60, open |
| `M0450-H-NONNEG` | Normalize or shift the selected height | Pointwise nonnegative height | 60, open |
| `M0450-H-PARALLEL` | Addition law and comparison of naive/canonical heights | Uniform bounded parallelogram defect | 100, open |
| `M0450-H-NORTHCOTT` | Number-field arithmetic and height comparison | Finiteness of bounded-height point sets | 100, open |
| `M0450-X-TRANSPORT` | Available affine/short-model results | Checked equivalence to frozen Jacobian points | 100, open |
| `M0450-X-SOURCE` | Primary sources, locators, assumptions, errata | Reviewed premise-to-node map | 100, open H1 |
| `M0450-X-PROVENANCE` | Every terminal body/import/revision/license | Transitive provenance inventory | 70, open |
| `M0450-X-TRUST` | Axiom reports, pinned replay, freshness, second review | Accepted trust closure | 70, open |

## Freeze boundary

The immediate mathematical root cut is `M0450-B-WEAKMW` plus
`M0450-H-HEIGHT`; model transport is shared deeper work. The checked Lean
composition only consumes these packages and does not construct either one.
Primary-source reconstruction, terminal provenance, trust replay, readable
review, and independent acceptance also remain open. Any change to obligation
identity, eligibility, or decomposition requires a new registry version and an
append-only delta. This phase claims neither audit completion nor theorem
completion.
