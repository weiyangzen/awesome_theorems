# THM-M-0632 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for `贝尔-豪斯多夫定理`
(Baire-Hausdorff theorem). The repository catalog supplies only the gloss `贝尔空间的性质`
("properties of Baire spaces"), attributes the item to Rene Baire and Felix Hausdorff in 1909,
and labels it `已验证`. It gives no truth-valued proposition, citation, definition convention,
assumptions, conclusion, proof, or formal artifact. The status label is untrusted discovery
metadata under rev-5.6.

The received wording names a topic family rather than one theorem. Intake therefore leaves the
canonical mathematical statement and Lean target null. It does not silently choose the defining
countable-intersection property, either Baire category theorem, preservation by open or dense
`G_delta` subspaces, a meagreness/residual-set characterization, or a functional-analysis
application. These have different domains, binders, assumptions, and conclusions.

K. Yosida's *Functional Analysis* contains a chapter titled "Applications of the
Baire-Hausdorff Theorem" (1965 edition, pages 68-81, DOI
`10.1007/978-3-642-52814-9_3`). Publisher metadata says completeness of a B-space or F-space
enables its use, but does not expose the exact theorem in Chapter 0. This is a credible
bibliographic lead only, not a source-statement admission or proof source.

`IntakeProbe.lean` checks adjacent pinned mathlib interfaces for Baire spaces, their principal
category consequences, complete-pseudometrizable and locally compact R1 instances, and Baire
subspaces. These declarations demonstrate feasible formal substrate but cannot select the catalog
root. The provisional vector is `[H5, M4, R4]`: `H5` classifies the received wording as an
unstable proposition, not the underlying standard results as false or open. There is no accepted
statement, proof state, source review, audit completion, theorem completion, or master acceptance.
