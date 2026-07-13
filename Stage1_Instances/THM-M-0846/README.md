# THM-M-0846 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `图极限理论`
(`graph limit theory`). The mathematical catalog supplies only the gloss `图序列的极限` (`limits
of graph sequences`), the attribution Laszlo Lovasz and Balazs Szegedy, the year 2006, and an
untrusted `已验证` status. Those fields identify the dense-graph-limit theorem family, not one
binder-complete proposition.

The matching primary source, Lovasz and Szegedy's *Limits of dense graph sequences*, contains
several noninterchangeable results. Its central Theorem 2.2 gives five equivalent characterizations
of limiting homomorphism-density parameters. The narrower limit-object implication says that a
convergent dense simple-graph sequence is represented by a symmetric measurable function on the
unit square; the converse and the algebraic/reflection-positive characterizations are additional
claims. Corollary 2.6 separately constructs convergent random graph sequences from such functions.
The catalog selects none of these exact roots.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M4, R4]`: the theorem family and a primary source lead are known, but exact root,
definitions, assumptions, edition/errata mapping, and independent review are open; no exact formal
artifact is credited; and no source-faithful proof reconstruction can attach to an unfrozen root.

`IntakeProbe.lean` checks only adjacent pinned graph-density, homomorphism, regularity, measure, and
Fubini APIs. All six downstream tasks remain open. No canonical statement, H0, M0, R0, accepted
execution state, audit completion, theorem completion, accepted receipt, or master acceptance is
claimed.
