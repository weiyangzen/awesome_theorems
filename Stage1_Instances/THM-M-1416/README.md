# THM-M-1416 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry "Bowen-Margulis
measure" (`Bowen-Margulis测度`). The repository supplies only the phrase `双曲系统的测度`
("measure of/for hyperbolic systems"), an attribution to Rufus Bowen and Grigory Margulis, and the
year 1970. That phrase names a mathematical object or subject family, not a truth-valued theorem
with ordered binders, hypotheses, and a conclusion.

The modern phrase "Bowen-Margulis measure" is used in several settings. Depending on the source,
it can denote a measure for a geodesic flow or an Anosov/Axiom A system, a construction from
boundary measures or symbolic dynamics, or a theorem asserting existence, uniqueness, maximal
entropy, ergodicity, mixing, full support, or periodic-orbit equidistribution. These are inequivalent
claims. Intake does not silently select one, and it does not merge this target with the separately
cataloged Markov-partition, topological-entropy, measure-entropy, or SRB-measure records.

The provisional root vector is `[H5, M4, R4]`. Here `H5` records that the catalog wording is not a
stable proposition; it does not say that a reviewed Bowen-Margulis theorem is false or open. `M4`
and `R4` record that no exact formal artifact or proof reconstruction can be attached to an
unselected proposition. The exact human statement and canonical Lean target remain null, every
dependent phase remains open, and no source-proof, statement, machine-proof, audit-completion, or
theorem-completion credit is claimed.

The structured authority is `instance.json`; `scope-map.md` freezes the decision boundary and
`source-statement-crosswalk.md` maps every supplied field to the missing mathematical and Lean
components. `IntakeProbe.lean` only authenticates adjacent APIs in the pinned environment and states
no target theorem. Exact worker checks are recorded in `validation.md` and the provisional receipt.
