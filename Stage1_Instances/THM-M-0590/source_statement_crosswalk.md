# Source-statement crosswalk

| Claim component | Human source discovery anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Essentially normal operators are classified up to unitary equivalence modulo compact operators by essential spectrum and index data | L. G. Brown, R. G. Douglas, and P. A. Fillmore, *Unitary equivalence modulo the compact operators and extensions of C*-algebras*, Lecture Notes in Mathematics 345 (1973), pp. 58-128 | bounded operators, compact self-commutator, unitary conjugation modulo compact operators | Primary source identified bibliographically, but exact theorem/page, assumptions, edition hash, and corrections review are not accepted: `H1` |
| Extension-theoretic organization of the invariant | L. G. Brown, R. G. Douglas, and P. A. Fillmore, *Extensions of C*-algebras and K-homology*, Annals of Mathematics (2) 105 (1977), pp. 265-324 | Busby invariant into a Calkin algebra and extension equivalence | Primary source identified; theorem numbering and premise-to-binder mapping remain open |
| Essential-normality hypothesis | Compactness of the self-commutator makes the Calkin image normal | predicate `IsCompactOperator (T* * T - T * T*)` | Mathematical bridge is standard but has no checked Lean witness or accepted source pinpoint yet |
| Essential spectrum | Spectrum of the operator's image in the Calkin algebra | quotient/Calkin spectrum or an equivalent Fredholm definition | Encoding choice is not frozen; equality of two unequivalent surrogate spectra must not be used |
| Index function | For `\u03bb` outside the essential spectrum, `T - \u03bbI` is Fredholm and has an integer index | Fredholm predicate and index of a bounded operator | Exact sign convention and local constancy package remain open |
| Classification conclusion | Existence of a unitary whose conjugacy error is compact | existential unitary equivalence modulo compact operators | Exact binder order and compact-error orientation are deferred to statement elaboration |
| K-homology gloss in the repository source | BDF extension classes are related to odd analytic K-homology | `Ext(C(X))` / `K^1(X)` candidate formulation | This does not by itself identify the frozen operator-classification root; a sourced and machine-checked bridge would be required |

The repository's source record at `Docs/Stage0_Blueprint.md:16143` supplies only the broad name and
the gloss "operator algebras and K-homology." It does not select a unique theorem statement. This
intake therefore makes the operator-classification theorem explicit and keeps the extension and
K-homology formulations as uncredited alternates rather than conflating all of BDF theory.

Discovery links (not immutable evidence receipts):

- 1973 paper: <https://doi.org/10.1007/BFb0061021>
- 1977 paper: <https://doi.org/10.2307/1970999>

No `H0` claim is made. Source audit must acquire immutable editions, pinpoint the exact theorem and
all separability/dimension hypotheses, resolve the equivalence convention and index sign, check
errata and later corrections, map every premise to the frozen Lean binders, and receive independent
review.
