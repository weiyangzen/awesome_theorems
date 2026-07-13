# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0906`, the title `列表着色`, the attribution
`Vizing/Erdős/Rubin/Taylor`, the year 1976, and the gloss `列表色数的理论`. Importance "high" and
status `已验证` are catalog metadata, not a proposition or receipt. No bibliography, definition,
parameterized graph class, inequality, equality, existence claim, or proof accompanies the record.

The wording identifies list coloring and the list chromatic number as a subject. Intake preserves
that subject boundary without manufacturing a theorem root.

## Candidate definitions, not credited

A future source-selected formalization may need concepts resembling the following:

- a graph `G` on a vertex type and a color carrier;
- an assignment `L` sending each vertex to a finite allowed-color collection;
- an `L`-coloring, meaning a proper vertex coloring whose value at each vertex belongs to its
  assigned collection;
- `k`-choosability, quantifying over assignments with exactly or at least `k` allowed colors; and
- the choice number or list chromatic number, defined as a least admissible `k`, with an explicit
  convention if no finite `k` exists.

This is a vocabulary map only. Definitions do not select the repository's missing theorem, and no
candidate is a canonical statement or proof obligation at intake.

## Proposition-changing decisions

An approved source correction must freeze all of the following:

- the exact root: definition, existence theorem, monotonicity result, upper or lower bound,
  equality, characterization, or theorem about a named graph class;
- simple graphs, multigraphs, directed graphs, hypergraphs, edge coloring, or vertex coloring;
- finite versus infinite vertex and color types, local finiteness, and any graph finiteness or
  nonemptiness hypotheses;
- finite sets, multisets, lists, or arbitrary sets as allowed-color assignments, including whether
  duplicates count and which decidable-equality assumptions are required;
- exactly `k` versus at least `k` allowed colors and the direction, hypotheses, and choice
  principles of any thinning transport;
- the ordered binders and scope of `G`, `k`, the color carrier, list assignment, and coloring;
- the representation of finite or infinite choice number, attainment of a least `k`, and the
  relationship to ordinary chromatic number; and
- all universes, typeclasses, side conditions, foundation/TCB/computation profiles, and alternate
  encodings with checked transports.

These choices yield inequivalent propositions. They are a resolution ledger, not a theorem
statement.

## Degenerate and boundary cases

No case is excluded at intake. Source review must decide empty and singleton vertex types, the
empty graph, complete and edgeless graphs, empty color carriers, `k = 0` and `k = 1`, empty or
undersized allowed-color collections, infinite palettes with finite local assignments, graphs with
no finite choice number, vacuous properness, duplicate-bearing lists, and the behavior of minima
when the admissible set is empty. It must also decide whether loops or parallel edges are outside
scope or represented by another graph model.

## Neighbor and substitution exclusions

- `THM-M-0904` owns the Dinitz array/list-edge-coloring problem; its special-case statement or
  future evidence does not define this general topic.
- `THM-M-0905` owns Galvin's theorem. A bipartite-multigraph list-chromatic-index result cannot be
  substituted for a general vertex list-coloring target.
- `THM-M-0907` owns the Alon-Tarsi theorem and its polynomial method.
- `THM-M-0908` owns Thomassen's planar-graph list-coloring theorem.
- `THM-M-0909` owns Voigt's non-4-choosable planar-graph result.
- Ordinary vertex coloring, chromatic number, bipartiteness, line graphs, or one explicitly colored
  graph does not establish a theorem about arbitrary allowed-color assignments.
- A structure or premise storing the desired coloring, bound, equality, or least number supplies
  no proof.
- The catalog's `已验证` label, a theorem name, an API probe, or a finite experiment supplies no H
  or M credit.

## Downstream boundary

The statement phase must first admit an immutable independently reviewed source that selects one
exact proposition and reconciles the attribution, year, neighbor targets, and every clause above.
Only then may it freeze a Lean module and expression, environment fingerprint, checked transports,
and mutation suite. Anchor audit, obligation architecture, proof, validation, and release remain
separate open phases.
