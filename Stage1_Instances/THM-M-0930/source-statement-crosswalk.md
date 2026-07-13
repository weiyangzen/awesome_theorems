# THM-M-0930 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6798-6803` records only:

- title: `组合Nullstellensatz`;
- attribution: Noga Alon;
- year: 1999;
- gloss: `多项式方法在组合中的应用`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:25363-25388`
repeats the gloss while explicitly leaving the formal system, exact definitions and assumptions,
proof path, equivalent forms, axioms, machine status, and artifact links open. These records
establish catalog identity only.

## Primary source lead

The matching source is Noga Alon, "Combinatorial Nullstellensatz," *Combinatorics, Probability
and Computing* 8 (1999), no. 1-2, pages 7-29, DOI
`10.1017/S0963548398003411`. The pinned mathlib bibliography records the same metadata.

An author-hosted 26-page PDF was inspected on 2026-07-13 outside the repository. Its SHA-256 is
`5933068242b0ecc6bba6944bf6d396492bb31c630d4cd7616e477b0a3e1646b7`; the layout-preserving
text extraction has SHA-256
`1ee86c030001e584bb0316aa463ed24fa6fa9773ad2ececadb329140518d0cec`.
The introduction states that the paper proves two theorems, numbered 1.1 and 1.2, "which may be
called Combinatorial Nullstellensatz." Their proofs appear in Section 2. This resolves the family
identity but demonstrates that the catalog gloss does not select a unique root.

This inspection supports `H1`, not `H0`. No lawful immutable source copy is admitted to the
repository, and no independent reviewer has accepted the complete definition chain, premise and
proof-node mapping, subring clause, corrections or errata disposition, or source-to-Lean
generalization.

## Source-to-candidate crosswalk

| Source clause | Pinned Lean candidate | Intake assessment |
|---|---|---|
| Theorem 1.1: field and finitely many variables | `CommRing R`, `IsDomain R`, finite type `sigma` | Lean is more general and uses a different variable encoding; transport open |
| nonempty finite coordinate sets | `S : sigma -> Finset R`, `forall i, (S i).Nonempty` | close candidate; finset and binder mapping open |
| vanishing on every product-grid point | `forall x, (forall i, x i in S i) -> eval x f = 0` | close candidate; exact source identity not accepted |
| `f = sum h_i g_i` | `f = linearCombination ... h` for finitely supported `h` | representation and finite-support transport open |
| source bound `deg h_i <= deg f - deg g_i` | `totalDegree (g_i * h_i) <= totalDegree f` | related bound, not accepted as definitional equality with the source clause |
| source subring-preservation clause | domain-general Lean theorem | requires a reviewed explanation or checked transport; not silently erased |
| Theorem 1.2: degree equals sum of `t_i` and selected coefficient is nonzero | `f.totalDegree = t.degree`, `f.coeff t != 0` for `t : sigma ->_0 Nat` | close candidate; notation and empty-index mapping open |
| `|S_i| > t_i` | `t i < #(S i)` | direct arithmetic orientation candidate |
| a grid point with nonzero evaluation | existential `s` with membership and `eval s f != 0` | close candidate; exact source target still unselected |

## Formal candidate ledger

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.Combinatorics.Nullstellensatz`:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `MvPolynomial.eq_zero_of_eval_zero_at_prod_finset` | source Lemma 2.1-style grid-vanishing result | supporting lemma only; not the catalog root |
| `MvPolynomial.combinatorial_nullstellensatz_exists_linearCombination` | source Theorem 1.1 candidate | exact source transport, body provenance, trust, and acceptance |
| `MvPolynomial.combinatorial_nullstellensatz_exists_eval_nonzero` | source Theorem 1.2 candidate | exact source transport, body provenance, trust, and acceptance |

The module source has SHA-256
`7702cbb3773e3bc6215f685018c4e4ed5a1b033411016d399c7996a2d90cfd3c`.
Its documentation says it follows `[Alon_1999]`; its theorem comments abbreviate the source labels
as "theorem 1" and "theorem 2," while the paper numbers them 1.1 and 1.2. This is a citation-
label normalization issue, not permission to choose a root.

Before leaving `H1`, an accountable source reviewer must preserve an approved edition, select and
pinpoint the exact root, map every premise, conclusion, definition, degree convention, proof node,
and correction, and obtain independent review. Before statement acceptance, Lean work must encode
only that root, minimize imports, serialize the elaborated expression and environment, compile all
credited transports, and pass removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations.
