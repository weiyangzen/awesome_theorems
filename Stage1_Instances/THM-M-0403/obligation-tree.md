# THM-M-0403 obligation tree

Item: `S56-M-0403-OBLIGATION_TREE`. Registry
`THM-M-0403-OBLIGATIONS-v1` freezes the semantic denominator before any
closure is credited. This is architecture evidence, not a proof receipt. The
root and every composition certificate remain open at `M4`.

## Frozen proof route

The selected route reduces recurrence zeros to nondegenerate solutions of a
linear equation in a finite-rank multiplicative group, while handling
degenerate proper subsums by induction on the number of terms.

```text
M0403-ROOT
`-- M0403-T-FINITE-ZEROSET
    |-- M0403-N-SCALAR-EXTENSION
    |-- M0403-B-TERM-INDUCTION
    |   `-- M0403-C-PROPER-SUBSUM
    |-- M0403-N-GROUP-EQUATION
    |-- M0403-B-DEGENERACY-SPLIT
    |-- M0403-L-ESS-FINITE
    `-- M0403-L-INDEX-INJECTIVE
```

The proof graph records all seven terminal requirements directly so that no
branch can disappear through a prose-only composition. Definitions,
foundation/trust, provenance, documentation, and workflow are separate typed
graphs. The source's integer-index formulation is informational and excluded
from every required denominator.

## Node boundaries

### M0403-ROOT

Exact target `Stage1.THM_M_0403.SchlickeweiEvertseStatement`. It consumes the
terminal zero-set theorem and adds no hidden premise. `[H1, M4, R3]`.

### M0403-S-DEFINITIONS

Audits `ExponentialPolynomialData`, `eval`, `zeroSet`, nonzero fields, and the
pairwise quotient nontorsion condition. These elaborated definitions are
interfaces, not finiteness evidence. `[H1, M3, R3]`.

### M0403-S-FOUNDATION

Requires the eventual root's transitive declaration, axiom, and TCB report.
It cannot close before a terminal proof body exists. `[H1, M4, R4]`.

### M0403-N-SCALAR-EXTENSION

Maps the finite coefficient/root data into an algebraic closure and must
reflect evaluation equality through an injective field homomorphism. This is
the explicit bridge from the canonical arbitrary characteristic-zero field
to the algebraically closed source formulation. `[H1, M4, R4]`.

### M0403-B-TERM-INDUCTION

The one-term branch has an empty zero set. The induction branch supplies the
finiteness hypothesis for every positive smaller arity. It is not permitted
to cite proper subsums without constructing the restricted data.
`[H1, M4, R3]`.

### M0403-N-GROUP-EQUATION

Divide by a nonzero pivot term, express each zero as a solution of a fixed
linear equation, and prove the resulting tuples lie in a finitely generated,
hence finite-rank, multiplicative subgroup. `[H1, M4, R4]`.

### M0403-B-DEGENERACY-SPLIT

Split normalized solutions into the nondegenerate case and the finite family
of nonempty proper vanishing-subsum cases. The node owns exhaustiveness and
finite-powerset recomposition. `[H1, M4, R3]`.

### M0403-L-ESS-FINITE

This is the central Evertse-Schlickewei-Schmidt Theorem 1.1 boundary:
finiteness of nondegenerate solutions in a finite-rank multiplicative group.
No matching pinned Lean declaration was found, so it is a bridge obligation,
not an imported fact. Its `100`-step budget means the theorem must be modeled
separately; it does not assert that the published proof fits in 100 steps.
`[H1, M4, R4]`.

### M0403-L-INDEX-INJECTIVE

Equality of normalized tuples at two indices would make a quotient of two
distinct characteristic roots torsion unless the indices agree. This
transfers finite solution tuples to finite indices. `[H1, M4, R3]`.

### M0403-C-PROPER-SUBSUM

Reindex a nonempty proper subset by a smaller `Fin`, restrict coefficients
and roots, inherit all structure fields, and identify the restricted
evaluation with the vanishing subsum. `[H1, M4, R3]`.

### M0403-T-FINITE-ZEROSET

Compose scalar extension, induction, the exhaustive split, ESS finiteness,
index injectivity, and the finite union of induction branches to obtain the
exact canonical `Set.Finite` conclusion. No Lean composition certificate
exists. `[H1, M4, R3]`.

### M0403-X-PROVENANCE

Requires content-addressed terminal-body, dependency, axiom, and origin
records after proof integration. The current negative candidate inventory is
not a terminal provenance closure. `[H1, M4, R4]`.

### M0403-S-INTEGER-TRANSPORT

Maps the integer-index source formulation to natural indices in the required
direction. It is a nonroot informational source mapping and cannot increase
machine, source, or readable coverage. `[H1, M4, R4]`.

## Frozen boundary

There are 13 canonical obligations: 12 root-relevant and machine-required,
9 human-source-required, 12 readable-required, and 1 informational nonroot
transport. No obligation is closed. The minimal mathematical root cut is the
absent `M0403-L-ESS-FINITE` Lean bridge, but closing it alone would not close
the other required reductions, branches, composition, provenance, trust, or
review gates. `audit_complete=false`; `theorem_complete=false`.
