# Scope map

## Preserved repository scope

The repository fixes target identity `THM-M-0898`, the title `Kirkman女学生问题`, Thomas Kirkman,
the year 1850, the gloss `Steiner三元系的存在性`, and an untrusted `已验证` label. Intake preserves
both the named schoolgirl subject and the literal gloss. It does not pretend that the two already
determine one proposition.

## Competing readings that require a source decision

1. **The named 15-schoolgirl problem.** Construct a schedule for a fixed 15-element point type:
   seven days, each day a partition into five 3-element groups, with every unordered pair of girls
   sharing exactly one group over the schedule. Equivalently, construct a resolution of the 35
   blocks of an `STS(15)` into seven parallel classes of five blocks, after the equivalence is
   explicitly proved.
2. **Existence of an ordinary fixed-order Steiner triple system.** For a specified `v`, construct a
   family of 3-element blocks on `v` points in which every 2-element subset occurs in exactly one
   block. The catalog gives no value of `v`.
3. **The general Steiner triple-system existence theorem.** Characterize all finite orders `v` for
   which an `STS(v)` exists, normally by an admissibility congruence. This is a quantified theorem
   family and is strictly broader than constructing the schoolgirl schedule.
4. **A general resolvable-system existence theorem.** Characterize orders admitting a resolvable
   Steiner triple system. This also goes beyond the single named schedule and needs its own source.

No reading receives canonical-statement or proof credit during intake.

## Statement-phase decisions

An independently reviewed source correction must freeze:

- which of the four readings is authoritative and how the catalog title/gloss conflict is resolved;
- the finite point type or natural order, nonemptiness, equality and decidability assumptions;
- whether blocks, daily groups, parallel classes, and resolutions are sets, finsets, indexed
  families, multisets, partitions, or quotient objects;
- exact block cardinality, pair-coverage uniqueness, within-day disjointness, day coverage,
  cross-day distinctness, and all ordered binders;
- whether the conclusion is a concrete witness, nonemptiness of a structure, an `Exists`, an
  iff characterization by congruences, or a checked equivalence between schedule and design forms;
- the treatment of small and degenerate orders, duplicate blocks/classes, empty carriers, and
  whether isomorphic schedules count as equal;
- minimal Lean imports, expression and environment fingerprints, foundation/TCB profiles, and
  mutations for removed uniqueness, changed order, altered binder scope, and boundary cases.

## Explicit exclusions

- Proving ordinary `STS(15)` existence without the seven parallel classes and calling it the
  schoolgirl solution.
- Proving only necessary congruence conditions, or assuming the design/schedule witness whose
  existence is the target.
- Defining `IsKirkmanSchedule` to contain the desired conclusion and closing the theorem by field
  projection or unfolding.
- Replacing pair coverage by coverage of ordered pairs, allowing a pair more than once, omitting
  daily partitions, or allowing repeated girls within a triple.
- Substituting generic design theory (`THM-M-0897`), Wilson's design-existence theorem
  (`THM-M-0899`), a Latin-square construction, or an unrelated block design.
- Treating a displayed schedule, computation, SAT result, or unchecked certificate as a Lean proof.
- Using the catalog's `已验证` label as human-source or kernel evidence.

The exact target, discovery protocol, obligation registry, proof architecture, and checked
schedule/design transports belong to later dependency-ordered nodes.
