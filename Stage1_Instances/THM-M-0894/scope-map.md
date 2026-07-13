# Scope map

## Received scope

The repository fixes only the title `距离正则图`, the collective attribution `众多数学家`, the
period `20世纪`, and the gloss `距离正则图的理论`. It gives no bibliography, definition, ordered
binders, hypotheses, conclusion, proof, correction history, or formal artifact. Stage0 repeats the
gloss and explicitly leaves the formal system, exact definitions and premises, proof route,
dependencies, equivalent forms, axioms, machine state, and artifact links open. The `已验证` label
is untrusted metadata.

The natural English subject translation is "distance-regular graphs." That translation identifies
a field, not a theorem. It does not determine whether the root is a definition, characterization,
parameter theorem, existence result, classification, spectral result, or diameter bound.

## Candidate mathematical families

An eventual source-approved target could concern one of the following, but none is asserted or
credited at intake:

- a definition or equivalent characterization using distance spheres and constant intersection
  numbers;
- existence and basepoint independence of intersection parameters `a_i`, `b_i`, and `c_i`, or an
  intersection array;
- consequences such as connected regularity, fixed valencies of distance layers, or recurrence
  relations for layer sizes;
- adjacency or distance-matrix algebra, eigenvalues, multiplicities, or association-scheme links;
- feasibility constraints, construction, existence, nonexistence, uniqueness, or classification for
  selected intersection arrays;
- diameter or valency bounds, including results belonging to the separate Bannai-Ito target.

These have different domains, binders, hypotheses, conclusions, boundary cases, and proof
architectures. A textbook definition cannot be substituted for a theorem about the theory.

## Proposition-changing decisions

Before the statement phase can freeze a canonical claim, an accepted source and independent
reviewer must fix:

1. Whether graphs are finite, locally finite, simple, undirected, connected, nonempty, and
   nontrivial, and how the vertex universe and decidable adjacency are represented.
2. Whether graph distance is natural-valued with a disconnected junk value or extended-natural,
   and whether diameter is finite, fixed, or quantified.
3. The exact distance-regularity definition: counts of neighbors in consecutive distance layers,
   common-neighbor counts indexed by a vertex pair's distance, adjacency-algebra closure, or another
   source definition.
4. Whether parameters are functions of the distance, explicit sequences, an intersection array, or
   existentially supplied data, and the indexing and out-of-range conventions.
5. The ordered quantifiers over vertices, basepoints, distances, parameters, graphs, diameter,
   valency, and arrays, including which independence facts are hypotheses or conclusions.
6. The precise result bundle: characterization, parameter identity, regularity consequence,
   spectral theorem, feasibility condition, existence, classification, or bound.
7. Equality versus graph isomorphism for uniqueness and how graph properties transport.
8. Every correction, erratum, convention translation, computation policy, and certificate boundary.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. Source review must decide empty, singleton,
and subsingleton vertex types; disconnected graphs; diameter zero or one; complete and edgeless
graphs; cycles and paths; degree zero, one, or two; distances beyond the diameter; empty distance
layers; subtraction or indexing at `i = 0` and `i = D`; zero intersection parameters; and finite
versus infinite locally finite graphs.

These choices are material. Mathlib's natural-valued `dist` and `diam` use zero at unreachable or
disconnected boundaries, while the extended versions use `top`. An unguarded encoding could make a
disconnected or subsingleton graph satisfy a condition for the wrong reason.

## Neighboring target boundaries

- `THM-M-0892` (Hoffman-Singleton theorem) owns a specific Moore-graph result family; it cannot
  select or discharge this broader subject target.
- `THM-M-0893` (Bannai-Ito conjecture) owns a diameter-bound theorem for distance-regular graphs;
  that result cannot silently become the generic root here.
- `THM-M-0895` (strongly regular graphs) owns a parameter-theory target closely related to the
  diameter-two case; `SimpleGraph.IsSRGWith` is not a generic distance-regular graph theorem.
- `THM-M-0896` (finite geometry) owns a separate graph-theory relationship topic; construction
  examples from finite geometry transfer no statement or proof credit.

Also excluded are an association-scheme theorem, a named classification, one explicit graph, or a
definition whose fields assume the desired conclusion unless an accepted source explicitly selects
that proposition and checked transports preserve the exact claim.

## Lean boundary

Pinned mathlib provides `SimpleGraph`, finite/local-finite neighborhood and degree APIs, graph
distance and diameter, common-neighbor sets, and strongly regular graph parameters. A bounded
literal search found no distance-regular graph or intersection-array declaration in repo-local Lean
or pinned mathlib. `IntakeProbe.lean` authenticates only adjacent substrate. It defines no
distance-regular predicate, canonical theorem, source transport, or proof body. The exhaustive
formal-candidate and provenance audit belongs to the later anchor-audit phase.

## Retry condition

Select a lawful immutable primary or authoritative edition and one pinpoint proposition; record all
incorporated definitions, complete binders, hypotheses, conclusion, proof boundary, corrections,
and boundary conventions; reconcile neighboring target ownership; and obtain independent source
review. A later statement phase may then encode exactly that proposition, minimize pinned imports,
serialize its expression and environment, check every credited transport, and run all four required
mutation classes.
