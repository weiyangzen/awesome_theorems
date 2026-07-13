# Source-statement crosswalk

## Literal repository record

The mathematical catalog record at `Docs/researches/math_theorems.md:5486-5491` contains exactly:

| Field | Literal value | Intake interpretation |
|---|---|---|
| title | `s-m-n定理` | identifies the s-m-n theorem family |
| proposer | `Stephen Kleene` | unreviewed attribution |
| time | `1943` | unreviewed year |
| statement | `参数定理` | name/gloss only; not binder-complete |
| importance | `高` | scheduling metadata, not evidence |
| formalization status | `已验证` | explicitly untrusted; no proof credit |

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The current catalog blob is
`b78ec1f48495aa5747ef252665ab58e418d195e4`. The Stage0 projection leaves the
formal system, definitions, premises, proof path, dependencies, equivalent statements, axiom use,
and machine artifact open.

The separate computer-science catalog says `存在可计算函数将程序索引和参数组合` (there exists a
computable function combining a program index and parameters). It projects to `THM-C-0005`, which
is outside the closed Stage1 target set. This clarifies the intended family but supplies neither an
exact formula nor transferable evidence.

## Inspected standard statement

Walter Dean and Alberto Naibo, *Recursive Functions*, Stanford Encyclopedia of Philosophy, Spring
2024 archive, Section 3.1, Theorem 3.1, was retrieved and inspected at the immutable archive URL
`https://plato.stanford.edu/archives/spr2024/entries/recursive-functions/` (observed SHA-256
`7d856ecda491ab83814622f4a75d277552b8750816412bca215b4a461d0b0af1`). It states, in the
entry's notation:

```text
For all n,m in N, there is a primitive recursive function
s_n^m(i,x_0,...,x_(m-1)) such that

phi^n_(s_n^m(i,x_0,...,x_(m-1)))(y_0,...,y_(n-1))
  ~= phi^(n+m)_i(x_0,...,x_(m-1),y_0,...,y_(n-1)).
```

The accompanying explanation says the transformer takes an index for an `(n+m)`-ary partial
computable function and values for its first `m` arguments, and returns an index for the residual
`n`-ary partial computable function. This is authoritative secondary evidence for the standard
family, not a primary proof source, accepted target statement, or H0 crosswalk.

## Primary-source lead and boundary

The repository's author/year points toward S. C. Kleene, *Recursive Predicates and Quantifiers*,
Transactions of the American Mathematical Society 53(1), 1943, pages 41-73, DOI
`10.1090/S0002-9947-1943-0007371-8`. Crossref metadata was retrieved and hashed as
`8883e9053f23489ef3abb13b1b316611e1593574490afbbf5cdd2b2286610be0`. The available
SEP entry cites this paper for other recursion-theoretic results but does not attribute its Theorem
3.1 to Kleene 1943. An attempt to retrieve the version-of-record PDF returned HTTP 429, so no
primary theorem passage, definitions, proof, page locator, corrections, or errata were inspected.
The paper is therefore a bibliographic lead only.

## Pinned Lean discovery candidate

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.PartrecCode`, contains:

```lean
Nat.Partrec.Code.smn :
  ∃ f : Code → ℕ → Code, Computable₂ f ∧
    ∀ c n x, eval (f c n) x = eval c (Nat.pair n x)
```

The source theorem uses witness `curry`, proof components `Primrec₂.to_comp primrec₂_curry` and
`eval_curry`, and reports axioms `propext`, `Classical.choice`, and `Quot.sound`. Pinned source
locations are `PartrecCode.lean:111-114`, `:506`, `:514-516`, and `:524-530`. The module itself
calls this the `S_n^m` theorem and cites Mario Carneiro's ITP 2019 formalization paper. This is a
checked discovery lead only.

## Field-by-field candidate crosswalk

| Mathematical field | Repository | SEP Theorem 3.1 | Pinned `Nat.Partrec.Code.smn` | Gate |
|---|---|---|---|---|
| program identifier | says program index only in duplicate record | natural index `i` | inductive `Code c` | choose model and check index/code transport |
| fixed parameters | unspecified | arbitrary `m`-tuple | one natural `n` | freeze arity and tuple encoding |
| residual inputs | unspecified | arbitrary `n`-tuple | one natural `x` | freeze arity and pairing transport |
| transformer strength | computable in duplicate gloss | primitive recursive | conclusion says `Computable₂`; witness separately has `Primrec₂` | choose exact strength and expose a checked bridge |
| semantics | unspecified | partial-function agreement `~=` | equality of partial evaluations for every `x` | freeze semantic equality and prove equivalence |
| quantifier order | absent | all `n,m`, then existence of `s_n^m`, then indices and tuples | exists `f`, computable, then all `c,n,x` | source/binder identity review |
| zero/malformed cases | absent | `n,m in N`; tuple conventions incorporated | `Code` syntax; total code decoder exists separately | freeze boundary conventions |
| proof/source | untrusted verified label | secondary theorem statement | pinned kernel-checked library body | primary proof mapping and formal provenance audit |

## Open source gate

To clear the next statement gate, an independent reviewer must accept a primary or otherwise
explicitly authoritative theorem statement and source locator, reconcile the 1943 attribution,
freeze all binders and boundary conventions, and select either the general natural-index theorem,
the packed unary code formulation, or checked transports between them. Until then, no candidate is
the canonical statement and H0, M0, R0, audit completion, and theorem completion remain false.
