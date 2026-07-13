# Scope map

## Preserved repository scope

Intake preserves all of the received metadata without silently reconciling it: target
`THM-M-0968`, title `Erdős盒原理`, Paul Erdős, year 1965, the gloss `超图中的匹配`, combinatorics /
enumerative combinatorics, and the untrusted `已验证` label. The title, attribution, date, and gloss
are inputs to a source-correction decision, not clauses from which a theorem may be invented.

## Competing readings

1. **Literal box-principle reading.** The Chinese title can suggest a pigeonhole or box-counting
   principle. The repository already assigns the ordinary finite pigeonhole principle to
   `THM-M-0914`, so copying that statement here would duplicate and substitute another target.
2. **Erdős matching-conjecture family.** The author, 1965 date, and hypergraph-matching gloss align
   with the extremal problem for an `r`-uniform family on an `n`-element ground set whose matching
   number is bounded. One common later form gives the maximum family size as the larger of two
   extremal constructions. This is a strong source lead, not an intake-selected formula.
3. **The 1965 sufficiently-large-domain theorem.** The reviewed 1965 paper proves a result for
   sufficiently large `n` relative to the uniformity and requested matching size. That partial
   theorem is materially different from the full extremal conjecture.
4. **An unspecified hypergraph matching theorem.** The gloss alone could denote existence of a
   matching, a bound on matching number, a min-max theorem, an algorithm, or another extremal
   result. No hypotheses or conclusion select among them.

No reading receives canonical-statement, source-fidelity, or proof credit during intake.

## Statement-phase decisions

An independently reviewed source correction must freeze:

- whether the title is erroneous, nonstandard, or intended to name a distinct box principle;
- whether the root is the full Erdős matching conjecture, a specific 1965 theorem, one special
  case, or another explicitly sourced hypergraph-matching result;
- the finite ground-set carrier, hyperedge representation, uniformity parameter, matching
  predicate, matching-number convention, and finiteness and decidability context;
- all ordered binders and arithmetic side conditions, including positivity, `r <= n`, and the
  relationship among `n`, `r`, and the requested matching size;
- the exact extremal quantity and off-by-one convention: maximum size with no matching of a given
  size versus minimum size forcing such a matching;
- the conclusion form, extremal constructions, equality versus inequality strength, and whether
  a sufficiently-large-`n` threshold is existential or explicit;
- empty ground sets, zero uniformity, zero or one requested edges, repeated edges, impossible
  matchings, the regime `n < r k`, and ties between extremal constructions;
- the source edition, exact result and pages, incorporated definitions, proof boundary, printed
  correction and later errata, translation, independent review, and neighboring-target ownership;
- minimal Lean imports, expression and environment fingerprints, checked transports, and removed-
  hypothesis, changed-domain, binder-scope, and boundary-case mutations.

## Explicit exclusions

- Ordinary pigeonhole (`THM-M-0914`) or another box-counting fact as the root without a source
  correction demonstrating that the hypergraph gloss, author, and year are erroneous.
- A graph (`r = 2`) matching theorem, the intersecting-family (`matching number one`) special case
  separately owned by Erdős-Ko-Rado (`THM-M-0822`), or a sufficiently-large-`n` theorem presented
  as the unrestricted general conjecture.
- Hilton-Milner (`THM-M-0964`), Ahlswede-Khachatrian (`THM-M-0965`), Kruskal-Katona
  (`THM-M-0966`), Lovász-Kneser (`THM-M-0967`), Hall, Tutte, or Lovász local lemma
  (`THM-M-0969`) used as a convenient substitute.
- A definition or structure field that assumes the extremal inequality, matching, or witness that
  the selected target is meant to establish.
- A finite search, optimization result, numerical table, solver output, or unchecked certificate
  used as source fidelity or kernel proof.
- The catalog's `已验证` label, an API probe, or a bounded no-match search used as theorem evidence.

The canonical target, discovery protocol, obligation registry, proof architecture, and source-
approved transports belong to dependency-ordered downstream nodes.
