# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:698-703` supplies exactly the title `卡当分解定理`, attribution
to Elie Cartan, the year 1913, the gloss `半单李代数的根空间分解` ("root-space decomposition of a
semisimple Lie algebra"), importance `high`, and status `verified`. Git history places all six
uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2713-2738` repeats the metadata while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifacts open. The rev-5.6 manifest retains `verified` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The catalog gives no bibliography, theorem locator, field, characteristic, dimension, splitting
condition, Cartan convention, root-space definition, directness contract, ordered binders, exact
conclusion, proof boundary, correction history, or reviewer.

## Inspected modern source lead

Pavel Etingof, *18.745: Lie Groups and Lie Algebras I*, full Fall 2020 lecture notes issued through
MIT OpenCourseWare and observed on 2026-07-13, was inspected. Section 19 works with
finite-dimensional Lie algebras over an algebraically closed field and, from Section 19.2 onward,
characteristic zero. Section 19.4, Proposition 19.11, printed page 103, fixes a semisimple Lie
algebra `g`, a Cartan subalgebra `h`, and a nondegenerate invariant symmetric bilinear form `B`.

- Part (i) states `g = h direct-sum (direct-sum over alpha in R of g_alpha)`, where `g_alpha`
  consists of the `x` satisfying `[h,x] = alpha(h)x` for every `h` in the Cartan subalgebra, and
  `R` is the finite set of nonzero linear forms having nonzero root space.
- Part (ii) states `[g_alpha,g_beta]` lies in `g_(alpha+beta)`.
- Parts (iii)-(iv) give orthogonality away from opposite roots and a nondegenerate pairing between
  opposite root spaces.
- Its proof refers back to the joint eigenspace decomposition and Proposition 19.6.

The observed PDF SHA-256 is
`908b49bd938da6b28f2bceb01311028c8f453c721af6830ce0e32a1e52b6b929`. The catalog does not cite
these notes. No complete incorporated-definition and proof-node crosswalk, correction audit,
historical verification of Cartan/1913, repository preservation, or independent review is
credited. This is an `H1` lead, not accepted `H0` evidence.

## Component crosswalk

| Catalog component | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "semisimple Lie algebra" | finite-dimensional semisimple `g` over algebraically closed characteristic-zero `k` | `LieAlgebra.IsSemisimple`, `FiniteDimensional` | catalog omits every field and dimension clause |
| "root space" | ordinary simultaneous eigenspace for the adjoint action of a Cartan `h` | `LieModule.weightSpace`; pinned `LieAlgebra.rootSpace` is generalized | equality/transport and root index remain open |
| Cartan summand | chosen toral subalgebra equal to the ordinary zero root space (source Definition 19.8) | `LieSubalgebra.IsCartanSubalgebra`, `LieAlgebra.rootSpace_zero_eq` | mathlib instead defines Cartan as nilpotent and self-normalizing; existence, choice, definition bridge, and ordinary/generalized bridge open |
| "decomposition" | internal direct sum of `h` and finitely many nonzero root spaces | `iSupIndep` plus `cartan_sup_iSup_rootSpace_eq_top`, or a direct-sum encoding | pinned spanning theorem alone is not the entire source claim |
| companion clauses | bracket grading and bilinear-form pairing properties | root-space product and Killing-form APIs | catalog does not say whether these belong to the root |
| `verified` | untrusted inventory label | source review and kernel receipts would be required | no H or M closure credit |

## Pinned Lean crosswalk

Pinned mathlib contains ordinary `LieModule.weightSpace`, generalized `genWeightSpace`, generalized
independence and spanning theorems, `LieAlgebra.rootSpace_zero_eq`, and
`LieAlgebra.cartan_sup_iSup_rootSpace_eq_top`. The last theorem assumes a finite-dimensional Lie
algebra over a field, a Cartan subalgebra, and a triangularizable restricted adjoint action; it
states spanning by the Cartan subalgebra and nonzero generalized root spaces.

There is also a Cartan-definition mismatch: Etingof's Definition 19.8 uses a toral subalgebra whose
ordinary zero root space is itself, whereas mathlib's `IsCartanSubalgebra` class means nilpotent and
self-normalizing. Their equivalence in the intended setting requires a checked bridge and is not
inferred from the shared name.

`Mathlib.Algebra.Lie.Weights.Killing` supplies ordinary-root behavior under `IsKilling` and suitable
field hypotheses. `Mathlib.Algebra.Lie.Killing` proves `IsKilling` implies semisimple but explicitly
records the characteristic-zero converse as missing. Therefore current APIs are meaningful `M3`
substrate, not permission to strengthen the received semisimple hypothesis or to credit an exact
ordinary direct decomposition.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable lawful edition, select the
exact clause package, map every incorporated definition, ordered binder, hypothesis, conclusion,
transport, and boundary case, audit corrections and historical attribution, and independently
approve fidelity to `THM-M-0095`. Only then may the statement phase freeze minimal imports, the
elaborated expression and environment hashes, checked alternate encodings, and all required
statement mutations.
