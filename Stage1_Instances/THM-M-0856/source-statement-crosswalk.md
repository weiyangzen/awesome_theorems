# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6278-6283` supplies exactly the title `Tutte定理`, attribution
to William Tutte, year 1947, gloss `完美匹配存在的条件`, importance `高`, and status `已验证`.
All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definitions,
binders, hypotheses, bibliography, theorem locator, proof boundary, corrections, or formal artifact.

`Docs/Stage0_Blueprint.md:23360-23385` repeats those fields and explicitly leaves the formal system,
foundation, precise definitions and premises, proof history, dependencies, equivalent forms, axioms,
machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Primary-source lead

The leading identity is W. T. Tutte, "The Factorization of Linear Graphs," *Journal of the London
Mathematical Society* s1-22, issue 2 (April 1947), pages 107-111, DOI
`10.1112/jlms/s1-22.2.107`. Crossref and OpenAlex metadata confirm author, title, date, journal,
volume, issue, and page range; OpenAlex reports no open full text. The publisher endpoint was not
admitted as a stable primary-text snapshot. Consequently the precise theorem/page inside the
article, source definitions of factor/linear graph, all assumptions, proof boundary, corrections or
errata, and an independent source review remain open. The citation is a strong identity lead, not
an `H0` packet.

## Clause crosswalk

| Catalog/source component | Intended mathematical component | Pinned Lean candidate | Intake status |
|---|---|---|---|
| `Tutte定理`, William Tutte, 1947 | Tutte's finite 1-factor theorem | `SimpleGraph.tutte` | identity strongly supported; exact primary locator and review open |
| graph | finite undirected loopless graph | `{G : SimpleGraph V}` with `[Finite V]` | worker-frozen Lean representation; primary-source convention review open |
| perfect matching / 1-factor | spanning set of pairwise disjoint edges covering every vertex | `∃ M : G.Subgraph, M.IsPerfectMatching` | worker-frozen pinned definition; alternate representation transports uncredited |
| delete vertex subset `U` | induced graph on vertices outside `U` | `((⊤ : G.Subgraph).deleteVerts U).coe` | worker-frozen operation; primary source-definition map open |
| odd components | connected components whose vertex support has odd cardinality | `.oddComponents.ncard` | worker-frozen pinned count; primary source-definition map open |
| at most `|U|` | no subset leaves strictly more odd components than removed vertices | `∀ U, ¬ G.IsTutteViolator U` | local inequality/no-violator `Iff` checked; upstream candidate audit open |
| necessary and sufficient | both directions for every finite graph | `(∃ M, M.IsPerfectMatching) ↔ ∀ U, ¬ G.IsTutteViolator U` | full `Iff` worker-frozen pending master acceptance |

## Pinned formal candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.SimpleGraph.Tutte` contains:

```lean
def SimpleGraph.IsTutteViolator (G : SimpleGraph V) (u : Set V) : Prop :=
  u.ncard < ((⊤ : G.Subgraph).deleteVerts u).coe.oddComponents.ncard

theorem SimpleGraph.tutte [Finite V] :
    (∃ M : G.Subgraph, M.IsPerfectMatching) ↔ ∀ u, ¬ G.IsTutteViolator u
```

The theorem entered mathlib at commit `358193a686dedec6d9d4d69374d1bdd6ecad9b25` on 2025-05-15,
which is an ancestor of the pin. The intake probe elaborates the definition, matching predicate, and
theorem, and reports axioms `propext`, `Classical.choice`, and `Quot.sound`. These facts establish a
credible direct proof-bearing candidate, not accepted `M0-W`. The statement proposal now supplies
the exact local expression, minimal non-proof import, fingerprints, checked local transports, and
mutations. Proof-body origin, transitive declaration and axiom closure, placeholder/unsafe/oracle
review, wrapper, anchor acceptance, and master acceptance remain ordered downstream work.

## Source gate

Before `H0`, an independent graph-theory source reviewer must inspect and preserve an authoritative
primary text, identify the exact result and incorporated definitions, and approve every domain,
premise, equivalence, boundary case, conclusion, proof-boundary, and correction row. Before machine
credit, the integration lane must accept the worker-frozen and mutation-tested exact Lean target;
the anchor-audit phase must then audit the candidate rather than inherit proof credit from its name,
the checked statement transports, or this crosswalk.
