# THM-M-1464 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`间断Galerkin方法` (discontinuous Galerkin method). The repository supplies only the gloss
`允许间断的有限元` ("finite elements allowing discontinuities"), attributes it to W. H. Reed
and T. R. Hill in 1973, and labels it `已验证`. A method name and description do not form a
truth-valued proposition with ordered binders, hypotheses, and a conclusion. The verified label is
untrusted metadata and supplies neither source nor proof credit.

The likely historical source was inspected in full: Wm. H. Reed and T. R. Hill, *Triangular Mesh
Methods for the Neutron Transport Equation*, LA-UR-73-479 / CONF-730414--2, OSTI 4491151
(1973). It defines an explicit, upwind, discontinuous piecewise-polynomial weighted-residual method
for the two-dimensional discrete-ordinates neutron transport equation on regular triangular meshes.
The paper reports numerical tests of accuracy and stability. It explicitly says that it has no
theoretical stability result for the continuous weight choices and that stability of the
discontinuous method with polynomial weights was found experimentally. Its observed convergence
rates are likewise drawn from test tables, not stated with a quantified mesh family, regularity
class, constants, or proof.

Consequently the catalog can refer to several proposition-changing roots: the Reed-Hill cell
construction, unisolvence of one local weighted system under fixed assumptions, exact reproduction
of a benchmark table, or a later sourced consistency, stability, convergence, or error theorem.
It can also refer to a different modern elliptic, hyperbolic, or conservation-law DG formulation.
The catalog selects none of these. Choosing a familiar interior-penalty or generic convergence
theorem would silently substitute new mathematics.

Pinned mathlib provides adjacent affine-simplex, measurable piecewise-integration, and coercive
bilinear-form APIs. `IntakeProbe.lean` authenticates those exact interfaces. None defines the
Reed-Hill scheme or closes any source-selected DG theorem.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog target as not yet a
stable proposition; it does not refute established DG results. All six downstream phases remain
open in `task-dag.json`. No canonical statement, proof body, accepted execution state, audit
completion, theorem completion, accepted receipt, or master acceptance is claimed.
