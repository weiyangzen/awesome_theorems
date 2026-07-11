# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Finite nondegenerate solutions of a linear equation in a finite-rank multiplicative group | J.-H. Evertse, H. P. Schlickewei, and W. M. Schmidt, *Linear equations in variables which lie in a multiplicative group*, Annals of Mathematics 155 (2002), 807-836, DOI 10.2307/3062133 | no accepted terminal declaration; expected deep input to the root | Primary paper and bibliographic identity located. Exact theorem number, hypotheses, page mapping, source hash, and errata review remain open, so this is not H0 evidence. |
| Finiteness/bounds for zeros of nondegenerate recurrence sequences | J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio Mathematica 53 (1984), 225-244 | `SimpleNondegenerateZeroFinitenessShape K` in the legacy discovery module | Primary application paper located, but its precise recurrence class and bound must still be checked against the selected simple-root field-valued formulation. |
| Simple exponential-polynomial formulation | Standard characteristic-root representation `u_n = sum_i c_i alpha_i^n`, with all `c_i`, `alpha_i` nonzero and all distinct-root quotients nontorsion | `ExponentialPolynomialData`, `exponentialPolynomialZeroSet`, and `SimpleNondegenerateZeroFinitenessShape` | Provisional canonical scope. The next phase must elaborate the actual declarations and test that no hypothesis was lost or strengthened. |
| Linear-recurrence formulation | Application of the same arithmetic input after characteristic-root decomposition | `LinearRecurrenceZeroFinitenessShape K` | Downstream candidate only. Its legacy `RecurrenceNondegenerateData` is an existence-of-representation interface, not yet a checked recurrence-to-roots reduction. |
| Full zero-set structure | Skolem--Mahler--Lech: a recurrence zero set is a finite union of finite sets and arithmetic progressions (formulation varies) | adjacent target `THM-M-0404` | Explicitly excluded to avoid substituting or duplicating the neighboring theorem. |

## Statement boundary

The provisional root asserts only finiteness in the simple nondegenerate branch.
It does not assert an effective numerical bound, the full repeated-root case,
or eventual periodicity of the zero set. Conversely, a proof of a finite-rank
multiplicative-group equation theorem alone would be an input, not closure of
the root, until the recurrence/exponential-polynomial reduction and finite-zero
extraction are checked.

The attribution "Schlickewei--Evertse theorem" is not itself precise enough to
identify a unique published theorem. The two primary papers above support the
intended genealogy, while the exact theorem/page/assumption crosswalk remains a
required source-audit task. No source label such as the manifest's untrusted
`已验证` is treated as proof evidence.

Discovery links (not immutable evidence receipts):

- ESS paper: <https://doi.org/10.2307/3062133>
- Evertse recurrence paper: <http://www.numdam.org/item/CM_1984__53_2_225_0/>

Required follow-up: archive immutable source files and hashes; identify exact
theorem numbers and pages; crosswalk rank, characteristic, nondegeneracy, and
index-domain assumptions; search corrections/errata; and obtain independent
review. Until then the human-source status is `H2`.
