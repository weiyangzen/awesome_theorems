# THM-M-0237 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Riemann-Roch theorem in the
complex-analysis catalog lane. The repository gives Bernhard Riemann and Gustav Roch, the year
1865, and only the gloss "divisor theory of compact Riemann surfaces." Its catalog label `已验证`
("verified") is untrusted metadata under rev-5.6 and supplies no human-source or Lean proof credit.

The title, date, attribution, category, and compact-Riemann-surface wording identify the classical
analytic Riemann-Roch family. They do not select an exact proposition. The intake therefore records
the standard divisor formula

`ell(D) - ell(K - D) = deg(D) + 1 - g`

only as a candidate statement shape. A source review still has to fix the connected compact Riemann
surface convention, divisor and degree definitions, `ell(D)`, genus, the canonical divisor or
canonical bundle, integer coercions, and exceptional cases. The Euler-characteristic line-bundle
form and the algebraic-curve form are related theorems, not automatically identical encodings.

This target is distinct from `THM-M-0105` and `THM-M-0175`, whose catalog records concern algebraic
curves. Their older dossiers and Lean files are discovery inputs only and confer no statement,
source, formalization, or acceptance credit here.

The provisional root vector is `[H1, M4, R4]`: a historically proved theorem family and relevant
published source candidates are identified, but no source-to-statement review is accepted; no exact
usable Lean theorem artifact is identified; and no source-faithful proof reconstruction exists.
`instance.json` is the scope authority, `scope-map.md` freezes the inclusions and exclusions,
`source-statement-crosswalk.md` records the unresolved source mapping, and `task-dag.json` leaves all
six downstream phases open. `IntakeProbe.lean` checks adjacent pinned APIs only. No canonical
mathematical or Lean proposition, H0, M0, R0, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
