# THM-M-0226 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Schwarz lemma. The repository
records Hermann Schwarz, 1869, and only the gloss "a holomorphic map from the unit disk to itself."
Its `已验证` ("verified") label is untrusted metadata and supplies no source or Lean proof credit.

The gloss names a classical theorem family but is not itself a truth-valued theorem. A standard
Schwarz lemma adds the essential fixed-origin hypothesis `f(0) = 0` and may conclude the pointwise
bound `|f(z)| <= |z|`, the derivative bound `|f'(0)| <= 1`, and a rigidity statement when equality
holds. The catalog does not say which conclusions belong to its root, whether the self-map is
strictly into the open disk or merely bounded by the closed disk, or whether equality cases are in
scope. Choosing those clauses at intake would manufacture an exact proposition.

Pinned mathlib has strong proved candidates for all principal inequality clauses and an affine
equality case. `IntakeProbe.lean` checks those declarations and a prospective two-inequality
specialization, but the candidate is not identified with the source root. The provisional vector
is therefore `[H1, M3, R4]`: the established theorem family is recognizable, exact source fidelity
and review are open, usable formal interfaces exist without an accepted target transport, and no
source-faithful readable reconstruction exists.

`instance.json` is the planned scope authority. `scope-map.md` freezes decisions and forbidden
substitutions, `source-statement-crosswalk.md` records the clause mapping, and `task-dag.json` keeps
all six downstream phases open. No canonical statement, H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
