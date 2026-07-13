# THM-M-0031 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Cohen structure theorem. The
repository catalogue gives only the Chinese gloss `完备诺特局部环的结构` ("structure of complete
Noetherian local rings"), attributes it to Irving Cohen in 1946, and labels it `已验证`. Under
rev-5.6 that label is untrusted metadata, not an exact statement, source audit, or proof receipt.

The gloss identifies a classical theorem family but not one proposition. A modern reference gives
both coefficient-ring existence for complete local rings and, under finite generation of the
maximal ideal, a presentation as a quotient of a formal power-series ring over a coefficient ring
(a field, Cohen ring, or truncated case as applicable). Other commonly named forms split
characteristic cases, assume Noetherianity from
the outset, or state a regular-local cover. Intake does not choose among them or silently import
their hypotheses and conclusions.

The 1946 Cohen paper is recorded as a bibliographic lead. Its full theorem passages, definitions,
proof boundary, corrections, and relation to the catalogue wording have not been independently
accepted. The Stacks Project's tagged theorem `032A` is an inspected modern statement lead, not the
repository's selected canonical source and not H0 evidence.

Pinned mathlib provides local-ring, residue-field, Noetherian, adic-completeness, multivariate
power-series, and characteristic-splitting interfaces. The discovery probe elaborates those APIs
and two adjacent theorems. The bounded source search found only a `docs/1000.yaml` title for the
Cohen structure theorem, with no associated declaration. These interfaces are formal substrate,
not an exact root candidate.

The provisional root vector is `[H1, M4, R4]`: the classical theorem family and source leads are
known, but an exact accepted source claim is not; no usable exact formal artifact was found; and no
source-faithful proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the admissible family and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. Exact checks are recorded in `validation.md`.
All coefficient-field, Cohen-ring, and truncated `p`-nilpotent coefficient-ring cases remain part
of the unresolved statement boundary. No H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
