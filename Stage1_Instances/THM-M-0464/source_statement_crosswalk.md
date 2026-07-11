# Source-statement crosswalk

| Claim component | Primary-source anchor | Intended formal component | Intake assessment |
|---|---|---|---|
| Root counting result | J. Pila and A. J. Wilkie, *The rational points of a definable set*, Duke Math. J. 133 (2006), Theorem 1.8, pp. 591-616 | a future canonical Lean declaration | Best match for the repository gloss; exact source text and hypotheses require immutable capture and independent review |
| Definable ambient set | Definitions in sections 1-2 of the same paper | an o-minimal expansion of the real field and a definable `X` | No repo-local Lean representation has been identified or credited |
| Algebraic/transcendental split | the paper's definition of the algebraic part `X^alg`; root counts `X^trans = X \\ X^alg` | predicate defining the union of connected positive-dimensional semialgebraic subsets, then set difference | Semantic high-risk point: it must not silently become Zariski closure, isolated algebraic points, or an arbitrary exceptional locus |
| Height-bounded rational points | the paper's rational height and counting notation | finite set/count of `x in X ∩ Q^n` satisfying the source height bound | Height normalization and coercions must be checked, not assumed equivalent |
| Sub-polynomial exponent | Theorem 1.8's `epsilon` bound | `epsilon > 0`, existential constant, universal admissible `T` | Binder order, constant dependencies, and cutoff convention remain statement-phase work |

## Metadata discrepancy and scope decision

The repository discovery record says only "Pila theorem", dates it to 2011, and glosses it as
"rational-point counting in o-minimal structures". That description is not an exact mathematical
statement. The 2006 Pila-Wilkie theorem is the closest standard named result and is therefore the
provisional root identity. The date mismatch is retained as an unresolved provenance discrepancy,
not repaired by silently selecting a 2011 variant.

The statement phase must obtain a stable copy of the paper, record its content hash and exact
Theorem 1.8 wording, audit corrections/errata, decide whether the target is the individual-set or
uniform-family formulation, and then elaborate the faithful binder order and definitions in Lean.
Until that happens the machine state remains `M4`; no alternate encoding or theorem candidate has
proof credit.

Discovery link (not an immutable evidence receipt):
<https://doi.org/10.1215/S0012-7094-06-13336-7>.

No `H0` or machine-closure claim is made. The manifest's `source_status_untrusted: 已验证` is
metadata only and is explicitly not accepted as evidence.
