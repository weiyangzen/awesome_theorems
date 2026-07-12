# THM-M-1389 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1389`, the repository label
`Weyl渐近公式` (Weyl asymptotic formula). The catalog supplies Hermann Weyl, 1911, and only the
gloss `特征值的渐近分布` (asymptotic distribution of eigenvalues), plus an explicitly untrusted
`已验证` status. It gives no formula, source locator, operator, dimension, domain, boundary
condition, spectrum enumeration, asymptotic parameter, leading constant, or remainder.

Weyl's paper *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller
Differentialgleichungen (mit einer Anwendung auf die Theorie der Hohlraumstrahlung)* is a strong
historical source lead. Bibliographic metadata identifies it as *Mathematische Annalen* 71 (1912),
441-479, DOI `10.1007/BF01456804`. The catalog's 1911 date may refer to an announcement or earlier
work, but the catalog gives no citation. More importantly, the historical paper concerns linear
partial differential equations, while the repository places the item in its ordinary differential
equations neighborhood. Intake therefore records the source lead and date/category conflict without
silently selecting a multidimensional Laplacian/PDE law, a one-dimensional Sturm-Liouville
eigenvalue asymptotic, or another modern spectral formulation.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the received wording is not yet a stable truth-valued proposition; no usable exact
formal artifact or source-faithful reconstruction is identified. `H5` classifies this sparse target
record, not the established mathematics conventionally called Weyl's law.

`IntakeProbe.lean` elaborates only adjacent pinned asymptotic-equivalence and finite-dimensional
spectral interfaces. These generic APIs neither define the source-selected spectral counting
function nor prove a Weyl law. All six downstream phases remain open in `task-dag.json`. No exact
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
