# Full study — S5-CLM-00003700

## Statement and provenance

The frozen source is `FormalConjectures/ErdosProblems/1109.lean` at revision
`2270d31e8dd611521f979de6d86da364930b7669`, declaration
`Erdos1109.erdos_1109.variants.konyagin_lower`. Its source body contains a
placeholder and is statement authority only. The claim-owned surface expands
`Erdos1109.f`; consequently the proof never consumes the provider proof body.

## Mathematical reconstruction

The extremal quantity asks for a set whose complete pair-sum table, including
the diagonal, avoids divisibility by every prime square. A common residue class
modulo the squares of small primes makes all those local obstructions identical
and avoidable. For squares above the cutoff, the forbidden congruence graph is
sparse enough for the squarefree sieve to retain a family of order
`log(log N) (log N)^2`. The retained family is an admissible witness in the
natural-number supremum. Its cardinality lower bound therefore transfers to
the extremal function and then to the real-valued Big-O statement.

The proof DAG separates the five indispensable steps: frozen semantic root,
construction/sieve, supremum comparison, asymptotic packaging, and exact
source/target transport. This separation exposes the exceptional cases: small
`N`, diagonal sums, zero or negative logarithms before the eventual threshold,
natural-to-real coercion, and the source declaration's `sorryAx` debt. None is
silently discharged by prose; each is assigned to a node and a formal anchor.

## Trust and replay

The human construction is not provider-proof evidence. The executable Lean
surface imports only `Mathlib`; the provider module path is immutable
provenance text because numeric FormalConjectures modules are not canonical
Lake imports. The local preflight checks evidence shape and substitution
resistance without invoking Lean. The canonical Master alone can establish
the elaborated root digest, transitive declaration/type/body/source hashes,
observed axiom set, cold-build trace, and final M0 status.

## Distillation

Machine inventories and hashes live in JSON rather than being repeated here.
This study retains every mathematical hypothesis (there are none), inference,
output, formal anchor, downstream use, exceptional case, and trust boundary,
while the outline gives the unique readable fragment for each proof node.
