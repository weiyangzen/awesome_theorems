# THM-M-1338 rev-5.6 intake

`THM-M-1338` is the catalog item "Bihari-LaSalle inequality" in ordinary differential
equations. The catalog supplies only the gloss "nonlinear Gronwall inequality", the date 1956,
the attribution Bihari/LaSalle, and an untrusted `verified` label. Those fields identify a theorem
family, not one binder-complete proposition.

## Intake result

This dossier records a `planned` instance. It identifies I. Bihari's 1956 paper, DOI
`10.1007/BF02022967`, as the strongest exact-year primary-source candidate found in the bounded
intake search. Publisher and Crossref metadata authenticate the paper, volume 7, issue 1, pages
81-94, but the accessible publisher surface does not expose the numbered generalized Bellman
lemma. The paper text, exact formula, theorem/page, definitions, proof boundary, and errata have
therefore not been accepted.

A common modern integral formulation is preserved only as an uncredited candidate family: a
nonnegative function `u` satisfying an inequality of the shape

```text
u(t) <= u0 + integral from t0 to t of f(s) * omega(u(s)) ds
```

is bounded after applying an antiderivative of `1 / omega`. The catalog does not fix the interval,
regularity, monotonicity and positivity assumptions, generalized inverse, range condition, zero
initial value case, or whether this integral form rather than a differential or uniqueness variant
is the root. None of that candidate prose is the canonical statement.

## Formal boundary

The pinned environment contains linear Gronwall and interval-integral APIs. `IntakeProbe.lean`
elaborates a small selection of those interfaces. A bounded name search found no Bihari, LaSalle,
or nonlinear/generalized Gronwall declaration in repo-local Lean or pinned mathlib. This is
discovery-only evidence, not an exhaustive anchor audit and not proof of the target.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a plausible primary source and established result family are known, but exact source
fidelity is unaudited, no usable exact Lean artifact is identified, and no proof reconstruction can
attach to an unfrozen proposition. `audit_complete=false` and `theorem_complete=false`.

See `scope-map.md`, `source-statement-crosswalk.md`, and `validation.md` for the exact boundaries
and worker evidence. Every downstream task remains open in `task-dag.json`.
