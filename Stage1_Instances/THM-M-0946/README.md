# THM-M-0946 rev-5.6 intake

`THM-M-0946` is the catalog item `Green-Tao-Ziegler定理`. The repository attributes it to
Green, Tao, and Ziegler in 2006, gives only the gloss `线性方程组在素数中的解` (solutions of
systems of linear equations in the primes), and marks it `已验证`. The verified label is
untrusted metadata and supplies neither source nor proof credit.

## Intake result

The matching 2006 preprint *Linear Equations in Primes* is by Green and Tao, not all three named
authors. It contains several inequivalent possible roots: a conditional finite-complexity
generalized Hardy-Littlewood asymptotic, an unconditional complexity-at-most-two corollary, a
matrix-form weighted asymptotic for solutions of `Ax = b`, and a qualitative existence corollary. Later Green,
Tao, and Ziegler work proves the inverse Gowers-norm input used to obtain the general
finite-complexity consequence. The catalog does not identify which paper, revision, result, or
conditionality boundary it intends.

Those alternatives require different domains, local and archimedean factors, complexity and
nondegeneracy hypotheses, asymptotic conventions, and conclusions. Selecting one at intake would
substitute proposition-changing mathematics. The 2006 attribution is also incompatible with the
later three-author proof package, so it cannot resolve the ambiguity.

## Formal boundary

`IntakeProbe.lean` elaborates only pinned prime-counting, von Mangoldt, and generic affine-map
interfaces. A bounded exact-topic search found no Green-Tao-Ziegler, finite-complexity
prime-pattern, Gowers inverse, or nilsequence root declaration in repository-local Lean or pinned
mathlib. The APIs are adjacent substrate, not the theorem, and the search is intake discovery
rather than the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a matching primary-source family and exact result locators were inspected, but the
catalog-to-result and correction mapping is open; no usable exact formal artifact is credited; and
no readable proof can attach to an unidentified root. All six downstream phases remain open. No
exact statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
