# Build and validation contract

Worker command (and the only locally authorized validation):

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean
```

The worker does not invoke Lean, Lake, Elan, a network fetch, or a canonical
checkout. Each Lean file has one executable `import Mathlib`; the numeric
FormalConjectures module path and qualified declaration occur only in a frozen
provenance comment. The three files are standalone and contain transparent
theorems only—no local definition, abbreviation, notation, syntax, macro,
instance, namespace alias, unsafe declaration, bodyless oracle, or placeholder.

Master acceptance still requires a cold from-source offline build at trust zero,
exact-root elaboration, per-declaration body/dependency/axiom inspection,
semantic-shadow mutations, and a comparison with the pinned THM-M-0387 negative
fixture. The local `--no-lean` receipt is not that acceptance.
