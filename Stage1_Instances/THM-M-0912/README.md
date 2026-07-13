# THM-M-0912 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `帕斯卡恒等式`
(`Pascal's identity`). The catalog supplies only the gloss `组合数的递推关系` ("the recurrence
relation for binomial coefficients"), an attribution to Blaise Pascal, the year 1654, and an
untrusted `已验证` label. It gives no formula, indexing convention, domain, boundary convention,
proof source, or formal declaration.

A strong modern statement lead was inspected: NIST DLMF 1.2.7, Chapter 26, Section 26.3(iii),
equation 26.3.5, states

```text
C(m,n) = C(m-1,n) + C(m-1,n-1),  m >= n >= 1.
```

The pinned mathlib source independently contains the zero-extended all-natural successor form
`Nat.choose_succ_succ`. These surfaces align after an index change when the DLMF side conditions
hold, but they do not have identical stated domains: mathlib's theorem also covers columns beyond
the row through its zero convention. Choosing the all-natural extension, the source-restricted
formula, or a conditional predecessor formulation is therefore deferred to the dependent
statement phase. Intake does not silently promote a candidate into the canonical root.

The provisional root vector is `[H1, M3, R4]`. `H1` records a published modern statement lead whose
historical source, complete proof, incorporated definitions, correction/errata history, and
independent review remain open. `M3` records exact pinned statement candidates, not a source-matched
canonical target or accepted proof. `IntakeProbe.lean` only authenticates those candidate APIs.

`scope-map.md` freezes the proposition-changing choices and boundary cases,
`source-statement-crosswalk.md` records the catalog/source/Lean relationship, and `task-dag.json`
leaves every downstream phase open. No accepted execution state, exact canonical Lean statement,
proof credit, audit completion, theorem completion, or master acceptance is claimed.
