# Exact-statement gate: blocked

Item: `S56-M-0538-STATEMENT`

Theorem: `THM-M-0538`

Verdict: blocked; no canonical Lean target is claimed.

## First failed gate

The repository source record says only "an axiom system for homology theory." An axiom system is
not by itself a proposition with a proof. The intake identifies three inequivalent possible roots:
a structure or predicate defining the axioms, a theorem that a concrete theory satisfies them, or
a characterization/uniqueness theorem. Neither the repository record nor an inspected primary
source selects one. Choosing any of them during this phase would broaden or substitute the target.

Even the definition/package reading leaves proposition-changing choices open: reduced versus
unreduced theory, coefficients, natural-number versus integer grading, the category of
topological pairs, connecting maps and their degree shift, the exactness and excision formulations,
the point normalization, additivity, universes, and empty or negative-degree cases. The intake's
1952 Eilenberg-Steenrod monograph is only a bibliographic candidate; no stable edition,
chapter/section/page, exact wording, assumptions, errata check, or independent review is recorded.
The adjacent `THM-M-0537` is separately scheduled and supplies no source or proof credit.

Pinned mathlib does not resolve the source ambiguity. A scoped search at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` found absolute singular-chain and singular-homology
functors and dimension-like calculations for totally disconnected spaces, but no declaration
encoding the Eilenberg-Steenrod package, no topological-pair homology interface with connecting
maps, and no full model theorem. Assuming the missing laws as fields would merely construct a
definition and could not establish that singular homology satisfies the axioms.

Consequently the ordered binders, exact conclusion, canonical serialization and expression hash,
alternate-form transports, and removed-hypothesis/domain/binder-scope/boundary mutation tests
required by section 5.1 cannot truthfully be frozen. Machine debt remains `M4`; statement
acceptance and theorem completion are false.

## Lean boundary checked

`StatementInfrastructure.lean` has the sole direct import
`Mathlib.AlgebraicTopology.SingularHomology.Basic`. It elaborates the pinned absolute singular
chain/homology functors and two dimension-like declarations. These checks establish only that a
nearby substrate exists. They are not the canonical statement and provide no proof credit.

All commands ran on 2026-07-12 in the worker clone. Lean ran from `Formalizations/Lean` against the
existing canonical `.lake` artifacts. No update, build, clone, fetch, or dependency mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0538` | 0 | rank 595, planned, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0538/StatementInfrastructure.lean` | 0 | the four pinned absolute singular-homology declarations elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped `rg` searches for Eilenberg-Steenrod packages, homology theories, pair homology, connecting maps, and singular-homology infrastructure | 0/1 | nearby absolute infrastructure found; no exact package or model theorem located (scoped search, not an exhaustive absence proof) |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |
| `if rg -n '[ \t]+$' Stage1_Instances/THM-M-0538/StatementInfrastructure.lean Stage1_Instances/THM-M-0538/statement-blocker.md; then exit 1; fi` | 0 | no trailing whitespace in either statement-phase artifact |

Base revision: `38aba87433173923511031e270f670c02d0351c6`.

## Retry condition

The authoritative lane must approve an immutable primary or standard-source root and freeze every
convention listed above. For a concrete-model theorem, the statement phase must also obtain or
implement the topological-pair, relative-homology, boundary, exactness, and excision interfaces
needed to state all laws. Only then can the exact target and its required mutations be elaborated.

Because the assigned statement phase did not pass its completion gate, no
`.stage1-worker-selftest.json` is emitted.
