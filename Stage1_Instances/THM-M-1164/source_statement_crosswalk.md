# Source-statement crosswalk

| Claim component | Source anchor | Formal candidate | Intake assessment |
|---|---|---|---|
| Repository title | `Docs/researches/math_theorems.md`, entry “Green函数的对称性” | dossier root | Identifies symmetry, but not its mathematical parameters |
| Repository statement | Same entry: “自伴算子的Green函数” | self-adjoint inverse/Green operator | Supports the self-adjoint-operator reading; source metadata “众多数学家, 19世纪” is not a primary citation |
| Green operator | Standard functional-analysis formulation: `0` in the resolvent set and `G=A⁻¹` | future Lean inverse theorem | Invertibility is necessary and was absent from the source phrase; now explicit |
| Symmetry over complex scalars | Self-adjointness gives Hermitian rather than literal symmetric kernels | `K x y = conj (K y x)` a.e. | Scalar field and conjugation are now explicit |
| Kernel passage | Equality of sesquilinear forms plus uniqueness of the integral-kernel representation | future measure/integral bridge | Requires representation and uniqueness hypotheses; not credited at intake |
| Pointwise version | An a.e. identity plus suitable continuity/regularity | future optional corollary | Excluded from the root unless those hypotheses are supplied |

The repository research entry is the only identified source of the exact local wording. It is a
secondary metadata list and supplies no edition, theorem number, page, assumptions, proof, or errata
record. Consequently this intake makes no `H0` or primary-source fidelity claim. `H2` records a
stable statement family with unresolved primary-source provenance.

The anchor-audit phase must locate a primary functional-analysis or PDE source with an exact theorem
and page, identify its operator domain and boundary hypotheses, check corrections/errata, and map
each premise to the operator and kernel conclusions. The statement phase must independently select
the minimal pinned mathlib APIs, elaborate one exact root, and test mutations including removal of
self-adjointness, removal of invertibility, a real/complex domain change, binder-scope changes, and
the zero-mode boundary. No historical “已验证” label is proof or machine evidence.
