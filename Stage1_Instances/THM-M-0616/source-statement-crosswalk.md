# Source-statement crosswalk

## Repository source identity

`Docs/researches/math_theorems.md:4573-4578` supplies exactly the title `连续性定义`, attribution to
"many mathematicians", the nineteenth century, the gloss `ε-δ定义与开集原像定义等价`, high
importance, and formalization status `已验证`. All six uncited fields originate in repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:16855-16880` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifacts open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

Neither repository record supplies an edition, theorem or page, displayed formula, proof,
definition chain, errata, reviewer, or formal declaration. The generic attribution and period do
not establish source fidelity or `H0`.

## Inspected human-source lead

Sidney A. Morris, *Topology Without Tears: Including a Graduate Course on Topological Groups*,
version of August 6, 2024, Section 5.1, printed pages 110-112, was inspected from the author's
website. The front matter identifies the author and version. The relevant route is:

1. Printed page 110 gives global continuity for `f : Real -> Real` in the usual pointwise
   epsilon-delta form.
2. Lemma 5.1.1, printed page 111, proves equivalence with the local open-neighborhood condition for
   real functions.
3. Lemma 5.1.2, printed page 112, proves equivalence between the local open-neighborhood condition
   and the condition that every open set has open preimage for maps of topological spaces.
4. Definition 5.1.3 defines a continuous map by open preimages, and the following sentence states
   that it coincides with the usual definition on the reals.

This is a complete modern proof lead for a real-to-real reading and a definition bridge to general
topological spaces. It is not accepted `H0`: the catalog does not cite this source; its real-to-real
root is not identical to the prospective two-pseudometric-space Lean root; no complete
source-to-Lean assumption and conclusion crosswalk, correction/errata audit, immutable repository
archive, or independent review exists. The observed PDF and locator are discovery evidence only.

## Clause crosswalk

| Catalog phrase | Material mathematical reading | Pinned Lean surface | Intake status |
|---|---|---|---|
| epsilon-delta | for every center and positive epsilon, there is positive delta controlling images of all sufficiently close points | `Metric.continuous_iff` | direct global candidate for pseudometric spaces; source scope unresolved |
| epsilon-delta at one point | epsilon-delta with a fixed center | `Metric.continuousAt_iff` | distinct candidate, not global continuity |
| epsilon-delta on a subset | centers and comparison points constrained to a set | `Metric.continuousOn_iff` | distinct relative candidate |
| open-preimage definition | preimage of every open codomain set is open | `Continuous` and `continuous_def` | direct definition interface; topology must match the distances |
| equivalent | both expanded predicates hold exactly for the same function | prospective composition through `Continuous f` | no canonical composition or fingerprint frozen |
| domain | reals in the inspected source; metric or pseudometric spaces in a common generalization | universe-polymorphic `PseudoMetricSpace` types | catalog does not choose the generality |
| `已验证` | untrusted inventory label | no expression, proof object, or receipt | explicitly rejected as evidence |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`:

- `Mathlib.Topology.Defs.Basic` defines `Continuous f` by the open-preimage field
  `isOpen_preimage`.
- `Mathlib.Topology.Continuous` exposes
  `continuous_def : Continuous f <-> forall s, IsOpen s -> IsOpen (f ⁻¹' s)`.
- `Mathlib.Topology.MetricSpace.Pseudo.Defs` exposes the pointwise, on-set, and global
  epsilon-delta characterizations `Metric.continuousAt_iff`, `Metric.continuousOn_iff`, and
  `Metric.continuous_iff`.

The intake probe checks the fully explicit types. It reports that `continuous_def` depends on no
axioms, while the three metric characterizations report `propext`, `Classical.choice`, and
`Quot.sound` in this pinned environment. These are candidate reports, not accepted trust closure.
No normalized root, checked source transport, proof-body ownership, transitive declaration audit,
placeholder scan of candidate bodies, or composition certificate is credited at intake.

## First source and statement gate

An independent source review must select either the real-to-real theorem or an authoritative
general metric-space formulation and map every incorporated definition, domain, binder,
hypothesis, conclusion, proof boundary, correction, and erratum. The statement phase must then
choose global versus pointwise versus relative continuity, metric versus pseudometric structures,
inequality conventions, topology-distance compatibility, degenerate cases, and root packaging;
elaborate one exact expression with minimal pinned imports; compile every credited transport; and
run the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
