# Scope map

## Preserved theorem family

The intake preserves the variable-model Moser-Tardos algorithmic Lovasz Local Lemma family named by
the catalog. Its natural source root is the sequential resampling algorithm and the asymmetric
expected resampling bounds of Moser-Tardos Theorem 1.2. This family description is not yet an
accepted canonical proposition.

The source's existential conclusion cannot stand alone as the target: existence of a valuation
avoiding all bad events is the ordinary Local Lemma conclusion and omits the algorithmic guarantee
named by the catalog. Conversely, adding the paper's parallel, deterministic, or lopsided extensions
without an approved package would broaden the target.

## Decisions required at statement freeze

1. Adopt and independently review an immutable source edition and decide whether Theorem 1.2 alone,
   its existential consequence plus algorithmic bound, or another explicit source package is the root.
2. Fix the finite variable and event index types, each variable's value space and law, the ambient
   probability space or product-law construction, measurability, and the exact meaning of mutual
   independence.
3. Define when an event is determined by a set of variables, whether `vbl(A)` is stored data or proved
   minimal support, and how two encodings are transported.
4. Define the dependency graph and neighborhood exactly, including exclusion of the event itself and
   overlap of determining-variable sets rather than an arbitrary dependency or lopsidependency graph.
5. Fix the codomain of probabilities and weights, strict bounds `0 < x(A) < 1`, finite product,
   division, casts, and the weak local-lemma inequality.
6. Formalize Algorithm 1.1: independent initialization, violation predicate, arbitrary violated-event
   selection, fresh independent resampling of exactly `vbl(A)`, unchanged complementary variables,
   and returned valuation.
7. Quantify the scheduler. The source permits any fixed deterministic or randomized selection
   discipline; the Lean claim must say whether the guarantee is universal over fair or arbitrary
   choices, parameterized by a scheduler, or tied to a specified kernel.
8. Fix the stochastic execution model, resampling count, stopping/terminal state, almost-sure versus
   expected termination claim, expectation definition, integrability, and per-event and total bounds.
9. Freeze ordered binders, universes, typeclasses, foundation/choice policy, conclusion ordering,
   checked alternate encodings, and every boundary case below.

## Degenerate and boundary cases

Source review must address empty variable and event families; variables with empty, singleton, finite,
countable, or general measurable value spaces; null or certain bad events; events with empty support;
duplicate or extensionally equal events; isolated and fully overlapping dependency graphs; weights
approaching zero or one; an initially satisfying valuation; an event that remains violated after
resampling; scheduler ties or nonmeasurability; infinite executions; zero resampling counts; and
arithmetic at zero denominators. Finiteness in Theorem 1.2 must not be silently generalized to
countable families.

## Excluded substitutions

- The nonconstructive asymmetric or symmetric Lovasz Local Lemma alone is weaker than the algorithmic
  theorem.
- Theorem 1.3's parallel logarithmic-step bound, Theorem 1.4's deterministic bounded-degree result,
  and the Section 6 lopsided theorem are distinct strengthenings or variants.
- Beck's earlier algorithm under stronger hypotheses, a cluster-expansion criterion, a resampling-
  oracle theorem, entropy compression, partial rejection sampling, or a specialized SAT/coloring
  application cannot replace the variable-model Theorem 1.2 family without a reviewed transport.
- Almost-sure termination without the source's expected eventwise bounds, or an expected bound for an
  unrelated stochastic process, is not the candidate root.
- A finite simulation, randomized test, empirical running time, extracted program without a checked
  correctness theorem, or numeric example supplies no proof credit.
- A structure field, premise, axiom, placeholder, oracle, or unchecked certificate containing the
  desired satisfying valuation, termination, or expectation bound supplies no proof.
- The catalog's untrusted `已验证` label, a paper citation, or API `#check` supplies no H0 or M credit.

## Neighbor boundaries

`THM-M-0969` owns the Lovasz Local Lemma itself and `THM-M-0971` owns Shearer's bound. Their future
statements, task states, and proof evidence remain separate. They may become explicit dependencies
only after exact statement and obligation freezes; neither substitutes for the Moser-Tardos
algorithmic conclusion.

## Formal boundary

No canonical Lean expression is frozen at intake. Pinned mathlib has general probability and
independence infrastructure but no exact target located by the bounded search. The probe checks
adjacent APIs only; it defines no bad-event variable model, dependency graph, resampling algorithm,
execution semantics, expectation bound, transport, or theorem. Exhaustive candidate discovery,
terminal-body provenance, minimal imports, trust closure, and source-to-Lean identity belong to later
phases.
