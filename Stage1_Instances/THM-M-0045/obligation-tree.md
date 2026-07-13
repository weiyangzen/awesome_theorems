# THM-M-0045 frozen obligation architecture

Item: `S56-M-0045-OBLIGATION_TREE`.

Registry version 1 freezes 37 semantic obligations before any proof-phase closure credit.
The proof graph expands the immutable 300-line historical Schur source through its eigenspace
descent, orthogonal-complement recursion, collected orthonormal basis, block-entry cases, matrix
transport, unitary witness, triangular witness, and final factorization. Provenance, evidence,
trust, documentation, and workflow edges are separate and cannot act as proof premises.

## Proof route

```text
ROOT <- checked conditional adapter <- equation package
  <- unitary U + upper triangular T + A = U*T*star U
  <- matrix/endomorphism transport + recursive auxiliary basis
  <- zero/nontrivial dimension split
     nontrivial <- eigenvalue/eigenspace V + W = V orthogonal
       <- compressed restriction on W + strict finrank descent
       <- recursive basis on W + eigenbasis on V + internal direct sum
       <- V/V, W/V, W/W, and impossible block-entry cases
```

Only the first arrow is a checked current-pin composition certificate. Every internal reverse
edge is explicitly `logical_decomposition` until a current-pin abstract-child harness consumes
all of its frozen children.

## Node ledger

### m0045-root

Every finite complex square matrix is unitarily similar to an upper triangular matrix in the exact frozen convention.

Formal target: `Stage1Instances.THM_M_0045.SchurTriangularizationTarget`. Output: The exact canonical proposition.
Source boundary: Statement.lean; expression sha256 275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b. Budget: 12 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-s-target

Freeze the ordered n, A, U binders, complex scalar field, unitary predicate, conjugation orientation, and BlockTriangular id conclusion.

Formal target: `checked target-interface audit of Stage1Instances.THM_M_0045.SchurTriangularizationTarget`. Output: A binder, domain, and conclusion identity certificate for the root, not a second proof of it.
Source boundary: Statement.lean:16-21; statement.json. Budget: 24 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-s-domain

Specialize Schur triangularization to Matrix (Fin n) (Fin n) Complex with its canonical finite linear order and decidable equality.

Formal target: `forall n : Nat, Matrix (Fin n) (Fin n) Complex`. Output: The root's exact domain and typeclass context.
Source boundary: Statement.lean:17-21. Budget: 16 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-s-boundary

Retain n = 0 and n = 1, and impose no invertibility, normality, diagonalizability, or nonzero-dimension hypothesis.

Formal target: `Stage1Instances.THM_M_0045.ObligationTree.DimensionBoundary`. Output: Every natural dimension is zero or positive, with zero and one still inside the universal target.
Source boundary: BoundaryProbe.lean:14-31; ObligationTree.lean:DimensionBoundary. Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-s-equation

Transport one unitary factorization A = U*T*star U with upper-triangular T to the target conjugation convention.

Formal target: `Stage1Instances.THM_M_0045.ObligationTree.equationWitness_implies_targetAt`. Output: Matrix.BlockTriangular (star U * A * U) id for the same witness U.
Source boundary: ObligationTree.lean:equationWitness_implies_targetAt. Budget: 20 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-s-foundation

Account for Lean, mathlib, propext, Classical.choice, Quot.sound, exact imports, and the no-oracle/no-numerical-computation policy.

Formal target: `#print axioms root_of_equationPackage and equationWitness_implies_targetAt`. Output: A versioned foundation and TCB boundary.
Source boundary: ObligationTree.lean axiom probes; anchor-audit.json immutable_environment. Budget: 24 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-n-matrix-operator

Transport A to its Euclidean-space linear endomorphism and its matrix back in an orthonormal basis.

Formal target: `Matrix.toEuclideanLin and LinearMap.toMatrixOrthonormal`. Output: A matrix representation of the same endomorphism.
Source boundary: external SchurTriangulation.lean:252-259,288-295. Budget: 36 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-n-reindex

Construct the Boolean-sigma/Fin(m+n) index bridge used by the recursive basis, then reindex the resulting Fin d basis to the original finite linearly ordered matrix index type.

Formal target: `Fin.subNat'; Equiv.finAddEquivSigmaCond; Fintype.orderIsoFinOfCardEq; OrthonormalBasis.reindex`. Output: An orthonormal basis indexed first by Fin(m+n) and finally by the original matrix index type, with order cases preserved.
Source boundary: external SchurTriangulation.lean:29-70,171-172,248-265. Budget: 70 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-b-dimension

Split the recursive inner-product space into the nontrivial and subsingleton cases and recombine exhaustively.

Formal target: `if hE : Nontrivial E then ... else ...`. Output: A SchurTriangulationAux package in either dimension case.
Source boundary: external SchurTriangulation.lean:150-154,223-230. Budget: 18 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-b-zero

For a subsingleton space, use dimension zero, the empty orthonormal basis, and vacuous upper triangularity.

Formal target: `Module.finrank_zero_of_subsingleton; Basis.empty; nofun`. Output: The zero-dimensional auxiliary package.
Source boundary: external SchurTriangulation.lean:223-230. Budget: 20 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-b-nontrivial

For a nontrivial space, choose an eigenvalue, split off its eigenspace, recursively triangularize the orthogonal complement, and assemble the invariant basis.

Formal target: `nontrivial branch of LinearMap.SchurTriangulationAux.of`. Output: The positive-dimensional auxiliary package.
Source boundary: external SchurTriangulation.lean:154-222. Budget: 24 substantive steps maximum; structured ledger: 12 recorded step(s).

### m0045-c-eigenvalue

Choose an eigenvalue of the endomorphism over an algebraically closed RCLike field.

Formal target: `let mu : f.Eigenvalues := default`. Output: An eigenvalue with a nonzero eigenvector witness.
Source boundary: external SchurTriangulation.lean:155; Module.End.exists_eigenvalue. Budget: 28 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-eigenspace

Construct the selected eigenspace V and retain its nontriviality for the descent measure.

Formal target: `let V : Submodule K E := f.eigenspace mu`. Output: A nonzero invariant submodule V.
Source boundary: external SchurTriangulation.lean:156,200-202,236. Budget: 32 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-c-orthogonal

Construct W = V orthogonal and record the V/W orthogonal-family facts.

Formal target: `let W : Submodule K E := V orthogonal`. Output: The orthogonal complement W and orthogonality between V and W.
Source boundary: external SchurTriangulation.lean:157,164. Budget: 28 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-c-compressed

Restrict f to W and project back to W to obtain the smaller compressed endomorphism g.

Formal target: `orthogonalProjection W comp f.domRestrict W`. Output: An endomorphism g of W for the recursive call.
Source boundary: external SchurTriangulation.lean:160. Budget: 26 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-recursion

Recursively construct an orthonormal upper-triangular basis for the compressed endomorphism on W.

Formal target: `LinearMap.SchurTriangulationAux.of g`. Output: Dimension n, basis bW, and triangularity hg for g.
Source boundary: external SchurTriangulation.lean:161. Budget: 30 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-l-descent

Prove finrank W < finrank E using positivity of finrank V and finrank additivity.

Formal target: `Module.finrank K W < Module.finrank K E`. Output: The well-founded recursion decrease.
Source boundary: external SchurTriangulation.lean:231-237. Budget: 34 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-eigenbasis

Choose the standard orthonormal basis bV of the eigenspace V.

Formal target: `stdOrthonormalBasis K V`. Output: An orthonormal basis bV indexed by Fin (finrank K V).
Source boundary: external SchurTriangulation.lean:163. Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-complement-basis

Use the recursively returned orthonormal basis bW of W with its upper-triangular compressed matrix invariant.

Formal target: `recursive fields bW and hg`. Output: An orthonormal basis of W carrying the recursive invariant.
Source boundary: external SchurTriangulation.lean:161,168. Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-internal-sum

Prove the V/W orthogonal family is internal and spans top.

Formal target: `DirectSum.IsInternal (cond . V W)`. Output: The internal direct-sum certificate needed to collect the bases.
Source boundary: external SchurTriangulation.lean:164-170. Budget: 38 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-collected-basis

Collect bV and bW into an orthonormal basis of E and reindex the Boolean sigma index to Fin (m+n).

Formal target: `int.collectedOrthonormalBasis hV B; Equiv.finAddEquivSigmaCond`. Output: The assembled orthonormal basis of E.
Source boundary: external SchurTriangulation.lean:168-176. Budget: 52 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0045-b-entry-split

For every entry strictly below the diagonal, split whether the column and row lie in the V block or W block, including the impossible cross-index case.

Formal target: `if hj : j < m then if hi : i < m then ... else ... else ...`. Output: All below-diagonal matrix coefficients vanish.
Source boundary: external SchurTriangulation.lean:177-221. Budget: 30 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0045-l-vv-zero

In the V/V block, use the eigenvector equation and orthonormality to make below-diagonal coefficients zero.

Formal target: `bV.orthonormal.right and f.HasEigenvector.apply_eq_smul`. Output: The V/V below-diagonal entry is zero.
Source boundary: external SchurTriangulation.lean:193-207. Budget: 44 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-l-wv-zero

In the W/V block, combine the eigenvector equation with membership in V orthogonal.

Formal target: `V.inner_left_of_mem_orthogonal`. Output: The W/V entry is zero.
Source boundary: external SchurTriangulation.lean:193-211. Budget: 34 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-l-ww-zero

In the W/W block, identify the coefficient with the compressed endomorphism and apply recursive triangularity after index subtraction.

Formal target: `hg (Nat.sub_lt_sub_right ...)`. Output: The W/W below-diagonal entry is zero.
Source boundary: external SchurTriangulation.lean:212-221. Budget: 42 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-l-index-impossible

Exclude a row in V with a strictly smaller column already outside V by transitivity of the finite order.

Formal target: `hj (Nat.lt_trans hji hi)`. Output: The impossible block-index branch is eliminated.
Source boundary: external SchurTriangulation.lean:212-215. Budget: 14 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-t-auxiliary

Package dimension equality, the assembled orthonormal basis, and all below-diagonal entry proofs into the recursive auxiliary result.

Formal target: `LinearMap.SchurTriangulationAux.of`. Output: An orthonormal basis whose matrix for f is BlockTriangular id.
Source boundary: external SchurTriangulation.lean:107-114,173-237. Budget: 24 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-matrix-basis

Adapt the recursive auxiliary basis from the Euclidean endomorphism back to the original matrix index type.

Formal target: `Matrix.schurTriangulationBasis`. Output: An orthonormal basis indexed by the original matrix indices.
Source boundary: external SchurTriangulation.lean:248-270. Budget: 34 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0045-c-unitary

Take the change-of-orthonormal-basis matrix and prove it belongs to Matrix.unitaryGroup.

Formal target: `Matrix.schurTriangulationUnitary`. Output: A unitary witness U.
Source boundary: external SchurTriangulation.lean:267-276. Budget: 28 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-c-triangular

Expose the matrix in the constructed basis as an upper-triangular matrix T.

Formal target: `Matrix.schurTriangulation`. Output: An upper-triangular witness T.
Source boundary: external SchurTriangulation.lean:278-281. Budget: 18 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-t-equation

Use the change-of-basis matrix identity to prove A = U*T*star U.

Formal target: `Matrix.schur_triangulation`. Output: The exact factorization equation for A.
Source boundary: external SchurTriangulation.lean:283-299. Budget: 38 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0045-t-package

Specialize the algebraically closed RCLike construction to Complex and Fin n and package U, T, unitarity, triangularity, and the equation for every A.

Formal target: `Stage1Instances.THM_M_0045.ObligationTree.SchurEquationPackage`. Output: A global SchurEquationPackage.
Source boundary: planned current-pin port/integration of external Matrix.schur_triangulation. Budget: 32 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0045-x-external-port

Port or immutably integrate the historical branch implementation and reproduce it at its own pins before current-pin use.

Formal target: `external commit 0a539f0ce764fd16726509b62ed7b870461070eb`. Output: A repo-local compatible or pinned external kernel artifact.
Source boundary: external-anchor-snapshot.json; anchor-audit.json. Budget: 60 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0045-x-source

Map Schur 1909 and Axler Theorem 6.38 to each mathematical obligation, with definition transport, errata review, and independent approval.

Formal target: `human-source crosswalk; no Lean proposition`. Output: Human-source coverage without machine proof credit.
Source boundary: source-statement-crosswalk.md. Budget: 80 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-x-provenance

Track every wrapper, historical proof body, current-pin port, import, revision, license, declaration dependency, and evidence packet.

Formal target: `content-addressed provenance closure`. Output: Unambiguous terminal-body and artifact provenance.
Source boundary: anchor-audit.json; external-anchor-snapshot.json. Budget: 60 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-x-trust

Close transitive axioms, placeholders, unsafe/oracle paths, executables, compiled artifacts, toolchains, dependencies, replay, and supply-chain trust.

Formal target: `release trust closure`. Output: An accepted TCB and foundation record.
Source boundary: anchor-audit.json trust_boundary; downstream validation. Budget: 60 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0045-x-readable

Produce an independently reviewed node-by-node reconstruction of the eigenspace descent and basis assembly, anchored to formal evidence.

Formal target: `structured readable proof record`. Output: R0-readable coverage for every required mathematical node.
Source boundary: obligation-tree.md is architecture only; full reconstruction pending. Budget: 100 substantive steps maximum; structured ledger: 2 recorded step(s).

## Freeze boundary

No obligation is accepted closed. External revision `0a539f0c` remains `M5/E3`: it is outside
the repository dependency closure, fails at the current pin, and has no own-pin kernel, axiom,
placeholder, unsafe, or transitive trust receipt. The root remains accepted `[H1, M3, R4]`.
Primary-source H0, readable R0, compatible integration, all internal composition certificates,
provenance/TCB closure, hermetic replay, independent verification, audit completion, theorem
completion, and master acceptance remain open.
