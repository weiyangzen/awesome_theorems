# THM-M-1451 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10595-10600` supplies exactly the title `QR算法`, attribution
`John Francis/Vera Kublanovskaya`, year 1961, gloss `特征值的QR迭代`, importance "high," and
status `已验证`. All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. No edition, theorem/page, matrix domain, algorithm,
hypotheses, conclusion, proof, errata, or formal artifact is attached.

`Docs/Stage0_Blueprint.md:39460-39485` repeats the gloss and explicitly leaves the exact definition
and premises, proof process, dependencies, equivalent statements, axioms, machine status, and
artifact links open. Its generic closed-result and leaf-budget prose is planning metadata. The
rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `QR` | repeated QR factorization | square matrices; chosen factors `Q_k`, `R_k`; unitary and triangular predicates | factor convention and selection absent |
| `迭代` | `A_(k-1)=Q_k R_k`, `A_k=R_k Q_k` | sequence or transition relation; initial state; exact/shifted update | algorithm variant absent |
| `特征值` | preservation or recovery of eigenvalues | characteristic polynomial, spectrum, eigenvalue multiset, or Schur diagonal transport | output relation absent |
| algorithm name | invariant, convergence, rate, stability, or termination theorem | one exact truth-valued conclusion | no conclusion selected |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no credit |

The wording cannot populate the exact domain, ordered binders, hypotheses, conclusion, alternate
encodings, degenerate cases, or expression fingerprint required by the rev-5.6 statement gate.

## Inspected modern lead, not credited as root

Peter Arbenz, *Numerical Methods for Solving Large Scale Eigenvalue Problems*, Chapter 4, "The QR
Algorithm," author-hosted chapter PDF observed 2026-07-13, SHA-256
`9826e5327bafd4d00c42abf5f643c62ec99bed3644d45b853c176234e323eeac`:

- printed page 63 gives equation (4.1), `A_k = R_k Q_k = Q_k^* A_(k-1) Q_k`, hence consecutive
  iterates are unitarily similar;
- printed page 64, Algorithm 4.1, initializes `A_0=A`, `U_0=I`, repeats QR factorization and the
  reversed product, and describes the intended Schur endpoint `A=UTU^*`;
- printed page 64 separately assumes mutually distinct eigenvalue magnitudes for below-diagonal
  convergence/rate and says the proof appears later/cites Wilkinson.

This disambiguating passage demonstrates that unconditional invariance and conditional convergence
are distinct claims, but it is not a complete convergence statement: further diagonalizability or
Jordan restrictions and generic initial coordinate-flag/eigenvector overlap assumptions may be
needed in addition to distinct eigenvalue magnitudes. The passage is not cited by the catalog, has
not been immutably admitted or independently reviewed, and does not provide the full convergence
proof. It is therefore a source lead, not `H0` or a selected canonical statement.

## Historical leads, not credited

Crossref metadata corroborates these publications but does not expose their proposition text:

| Candidate | Bibliographic locator | Intake boundary |
|---|---|---|
| J. G. F. Francis, *The QR Transformation A Unitary Analogue to the LR Transformation--Part 1* | *The Computer Journal* 4(3), 1961, 265-271, DOI `10.1093/comjnl/4.3.265` | metadata inspected; publisher PDF returned HTTP 403; theorem, assumptions, proof, errata, and catalog mapping uninspected |
| J. G. F. Francis, *The QR Transformation--Part 2* | *The Computer Journal* 4(4), 1962, 332-345, DOI `10.1093/comjnl/4.4.332` | metadata only; primary text and exact role uninspected |
| V. N. Kublanovskaya, *On some algorithms for the solution of the complete eigenvalue problem* | *USSR Computational Mathematics and Mathematical Physics* 1(3), 1962, 637-657, DOI `10.1016/0041-5553(63)90168-X` | metadata only; publication-year relationship to the catalog's 1961 and primary theorem/proof remain unreviewed |

No primary source currently satisfies the edition/theorem/page/assumption/errata/node-crosswalk and
independent-review requirements for `H0`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Candidate | Role | Why it is not the root |
|---|---|---|
| `Matrix.charpoly_mul_comm` | proves `(Q*R).charpoly = (R*Q).charpoly` over square matrices | one-step invariant only; assumes supplied factors and says nothing about convergence |
| `Matrix.mem_spectrum_iff_isRoot_charpoly` | bridges spectrum membership to a characteristic-polynomial root over a field | downstream bridge only |
| `InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` | orthonormalization/triangular coefficient infrastructure | no iteration sequence or eigenvalue conclusion |
| `OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary` and `Matrix.mem_unitaryGroup_iff` | unitary change-of-basis interfaces | no QR selection or iteration theorem |
| `Matrix.charpoly_of_upperTriangular` and `Matrix.BlockTriangular` | triangular endpoint/eigenvalue infrastructure | endpoint predicates and formulas only |

A bounded exact-topic search found no declaration named or documented as QR iteration, QR
algorithm convergence, or Francis iteration. Passing `IntakeProbe.lean` authenticates only these
adjacent interfaces. The first downstream gate is an approved pinpoint source and exact root
selection; only then can minimal imports, a canonical Lean expression, transports, and mutations be
frozen.
