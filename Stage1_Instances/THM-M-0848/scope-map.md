# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0848`, the label `Erdős-Rényi随机图`, attribution to
Erdos and Renyi, the year 1959, and the gloss `随机图模型的基本理论`. Intake preserves the
finite random-graph subject boundary without turning "basic theory" into a theorem.

## Materially distinct candidate scopes

None of these candidates is selected or credited as the canonical claim:

1. The fixed-edge model `G(n, m)`: uniformly choose `m` edges among the `n choose 2` possible
   unordered edges on `n` labelled vertices.
2. The independent-edge model `G(n, p)`: include each possible unordered edge independently with
   probability `p`.
3. A statement that one of those constructions is a probability measure or has a stated singleton
   mass, edge-count distribution, independence property, or endpoint law.
4. One of the four asymptotic results in Erdos and Renyi's *On Random Graphs I*: connectivity,
   largest-component deficit, number of components, or the stopping time for connectivity.
5. A coupling, contiguity, or asymptotic transport between `G(n, m)` and `G(n, p)`.

The historical source and the modern umbrella terminology do not make `G(n, m)` and `G(n, p)` the
same probability law. A checked relationship would be a separate theorem with its own hypotheses
and limiting regime.

## Proposition-changing decisions

Before statement elaboration, an approved source review must freeze:

- one immutable primary source, incorporated definitions, exact theorem and page, proof boundary,
  corrections or errata, and independent review;
- fixed-edge versus independent-edge sampling, and whether the target is a definition, finite law,
  asymptotic limit, coupling, or algorithmic/stopping-time result;
- labelled versus unlabelled graphs, simple/undirected/loopless conventions, the vertex type and
  universe, and whether isolated vertices remain part of the graph;
- the probability representation (`Measure`, finite `PMF`, or another checked encoding),
  measurability, edge-independence, and equality or almost-everywhere conventions;
- ordered binders for `n`, `m` or `p`, graph events, auxiliary integers, and asymptotic parameters;
- parameter ranges such as `0 <= m <= n.choose 2`, `p` in `[0,1]`, whether `n` tends to infinity,
  which other quantities are fixed, and all rounding conventions;
- the exact conclusion and every normalization, logarithm base, strict/weak inequality, and limit
  topology used by that conclusion.

## Boundary and degenerate cases

No case is excluded at intake because no proposition has been selected. The statement phase must
resolve `n = 0`, `n = 1`, `m = 0`, `m = n.choose 2`, invalid `m`, `p = 0`, `p = 1`, empty graph
events, zero-probability conditioning, and all small-`n` or asymptotic threshold qualifications.
It must also decide whether graph equality is literal on a fixed labelled vertex type or modulo
isomorphism.

## Explicit exclusions and ownership boundaries

- `THM-M-0849` (random-graph phase transition), `THM-M-0850` (giant component),
  `THM-M-0851` (connectivity threshold), and `THM-M-0852` (Hamilton-cycle threshold) are separately
  owned conclusions. None may be silently selected as the meaning of "basic theory."
- `THM-M-1112` is a near-duplicate catalog record named "random graph" with the gloss
  "Erdos-Renyi random graph model." Its dossier is useful discovery context but transfers no
  accepted scope, source, status, or proof evidence to this target.
- `THM-M-1009`, the Erdos-Renyi second lemma extending Borel-Cantelli, is unrelated to random-graph
  models.
- A deterministic existence theorem obtained by discarding the probability law, a sampler or
  numerical experiment, or a structure/premise storing the desired distributional conclusion is
  not an admissible substitute.
- The catalog's untrusted `已验证` label and a successful adjacent-API probe provide no source or
  proof credit.

No Lean expression is frozen at intake. A later target must expose a concrete graph sample space
and probability law and map every binder, hypothesis, conclusion, and boundary case to the selected
source statement.
