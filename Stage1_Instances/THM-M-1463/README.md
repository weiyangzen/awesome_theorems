# THM-M-1463 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `Petrov-Galerkin方法` (Petrov-Galerkin method). The repository attributes the topic to many
mathematicians in the twentieth century and gives only the gloss `推广的Galerkin方法` ("a
generalized Galerkin method"). A method name and the word "generalized" do not form a truth-valued
proposition with ordered binders, hypotheses, and a conclusion. The catalog value `已验证` is
untrusted metadata and supplies neither source nor proof credit.

Petrov-Galerkin commonly permits different trial and test spaces, but that observation still does
not choose a theorem. A source-selected result could be unique solvability under an inf-sup
condition, stability of the discrete solution, a Babuška-type quasi-optimal error estimate,
convergence for an approximation family, or a theorem for one concrete finite-element scheme.
These alternatives differ in spaces, scalar fields, bilinear or sesquilinear conventions,
nondegeneracy assumptions, constants, and conclusions. Ordinary Galerkin, Lax-Milgram, and
Banach-Nečas-Babuška are related but cannot be silently substituted.

Ivo Babuška's 1973 paper *The finite element method with Lagrangian multipliers* is recorded as a
bibliographic theorem-family lead. The catalog does not cite it, and only publisher metadata was
inspected here; no theorem passage, assumption list, proof boundary, erratum, or independent source
review was accepted. It therefore cannot select the canonical claim.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received method gloss as not yet a
stable proposition; it does not refute established Petrov-Galerkin results. `IntakeProbe.lean`
authenticates adjacent pinned bilinear-map, projection, and Lax-Milgram APIs only. All six
downstream phases remain open. No canonical statement, H0, M0, R0, accepted state, audit
completion, theorem completion, or master acceptance is claimed.
