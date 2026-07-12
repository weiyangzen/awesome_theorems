# THM-M-0897 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `设计理论`
(design theory). The repository supplies only the gloss `组合设计的存在性` (existence of
combinatorial designs), the attribution "many mathematicians," and the twentieth century. These
data name a large subject and an existence-problem family, but they do not form one truth-valued
proposition.

The gloss does not choose block designs, `t`-designs, balanced incomplete block designs, Steiner
systems, pairwise balanced designs, resolvable designs, Latin-square designs, or another design
class. It also fixes none of the parameters, admissibility conditions, quantifier order, block
multiplicity conventions, exact versus asymptotic scope, or boundary cases that determine an
existence theorem. Selecting a standard result would add proposition-changing mathematics and
could silently absorb neighboring `THM-M-0898`, `THM-M-0899`, `THM-M-0900`, or `THM-M-0901`.

Two reference pages were inspected only to test the breadth of the label. Peter J. Cameron's
*Encyclopaedia of Design Theory* says that there are many types of designs and treats existence,
uniqueness, and enumeration as different properties. The *Encyclopedia of Mathematics* block-design
entry distinguishes BIBDs, PBIBDs, Steiner systems, Latin-square block designs, and other classes.
Neither source is cited by the repository or selects the target theorem, so neither is accepted as
canonical source evidence.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the catalog wording as not yet a
stable proposition; it does not say that design-theory existence theorems are false or open. Pinned
mathlib provides finite set-family, fixed-cardinality subset, and counting interfaces, but a bounded
exact-name search found no block-design, `t`-design, BIBD, or Steiner-system declaration. These are
intake feasibility observations, not an anchor audit or proof.

`instance.json` is the structured scope authority. `scope-map.md` records every proposition-changing
choice and neighboring-target boundary. `source-statement-crosswalk.md` preserves the exact catalog
record and the source-discovery boundary. `task-dag.json` keeps all downstream phases open. No exact
mathematical or Lean statement, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
