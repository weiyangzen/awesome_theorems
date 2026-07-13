# THM-M-0889 rev-5.6 intake

`THM-M-0889` is the combinatorics/graph-theory catalog item named the
Alon-Milman theorem. The repository attributes it to Noga Alon and Vitali Milman, dates it to
1985, and supplies only the gloss "spectral gap and expansion" plus an untrusted `verified` label.

## Intake result

This dossier records a fail-closed `planned` instance. The matching primary source family is Alon
and Milman, *lambda_1, Isoperimetric Inequalities for Graphs, and Superconcentrators*, JCTB 38
(1985), 73-88. That paper defines the combinatorial Laplacian `Q = C^T C`, calls its second-smallest
eigenvalue `lambda_1`, and proves several different relations between that eigenvalue and graph
expansion or concentration.

The catalog does not choose a numbered result. Plausible roots include Lemma 2.1, Theorems 2.5
through 2.7, and the extended-double-cover expander result Theorem 4.3. A later standard two-sided
`d`-regular edge-expansion formulation is also commonly attributed to Alon-Milman, but it changes
definitions, notation, and presentation. Selecting any one of these at intake would substitute
missing mathematics. The statement phase must admit and independently review an immutable source,
select the exact result, and freeze every definition and binder.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned APIs for finite simple graphs, graph distance,
degrees, adjacency and Laplacian matrices, positive semidefiniteness, and Hermitian eigenvalues. It
is an API probe only. It defines no expansion invariant or spectral gap, declares no target
theorem, and supplies no proof credit.

The provisional vector is `[H1, M4, R4]`: a matching primary paper and several exact result
candidates are known, but source-to-root selection and review remain open; no usable exact Lean
artifact is credited; and no reviewed readable proof reconstruction exists. All six downstream
tasks remain open. No accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
