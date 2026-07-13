# THM-M-0821 rev-5.6 intake

This directory began as the fail-closed `planned` intake dossier for `Sperner定理` (Sperner's
theorem). The repository supplies the attribution Emanuel Sperner, the year 1928, and the gloss
`幂集反链的最大大小` (maximum size of an antichain in a power set), but no citation,
binder-complete statement, equality convention, or formal artifact. Its `已验证` label is untrusted
metadata.

The original paper was located and inspected. On printed page 544 it defines a distinguished
family as one in which no member is a subset of another, proves the middle-binomial upper bound,
and also classifies equality: the unique middle layer for even ground-set size and either adjacent
middle layer for odd size. The catalog gloss does not say whether the target is only the sharp
upper bound, the maximum-value statement including an extremizer, or the full equality
classification. Intake therefore records the source family without silently selecting one of
these materially different propositions.

Pinned mathlib contains a strong formal candidate, `IsAntichain.sperner`, which checks the upper
bound for a finite family of finite subsets. It does not state attainability or the source paper's
equality classification, and mathlib's file marks equality cases as TODO. `IntakeProbe.lean`
authenticates this exact candidate and its middle-layer APIs only; it does not freeze the canonical
target, audit the terminal proof body, or provide root proof credit.

The provisional root vector is `[H1, M3, R4]`. `instance.json` is the structured scope authority,
`scope-map.md` freezes proposition-changing choices and exclusions, and
`source-statement-crosswalk.md` maps the catalog, primary source, and formal candidate. All six
downstream phases remain open in `task-dag.json`. This is a self-tested worker proposal only: no
canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.

## Statement-phase result

The statement phase provisionally resolves the catalog's variant ambiguity by reading "maximum
size" literally: `SpernerMaximumTarget` conjoins an attaining antichain with the universal sharp
middle-binomial upper bound. This is stronger than the available upper-bound interface alone but
does not silently add the 1928 paper's stronger classification of every equality family.

`Statement.lean` uses only `Mathlib.Data.Finset.Slice`, not the proof-bearing LYM module. It checks
an iff to the concrete lower-middle-layer witness, the `Fin 0` and `Fin 1` boundaries, and four
structural mutations. `check_statement.py`, `statement.json`, `statement-validation.md`, and
`statement-receipt.json` bind the exact elaborated expression and pinned environment.

The vector remains `[H1, M3, R4]`. This is a worker-self-tested statement proposal pending
dependency-ordered master acceptance; no upper-bound proof body, full equality classification,
`H0`, `M0`, `R0`, audit completion, theorem completion, or release is claimed.
