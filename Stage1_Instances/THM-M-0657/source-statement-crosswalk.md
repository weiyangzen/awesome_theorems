# Source-statement crosswalk

## Source inventory

| Source | Pinpoint | Role and current status |
|---|---|---|
| Repository research record, `Docs/researches/math_theorems.md` | Lines 4866-4871: `莫利范畴性定理`; statement `不可数范畴理论的特征`; Michael Morley; 1965 | Establishes target identity and historical attribution only. It supplies no quantifiers, assumptions, definitions, proof, or machine evidence. |
| Michael Morley, *Categoricity in Power*, Transactions of the American Mathematical Society **114** (1965), no. 2, 514-538 | DOI `10.1090/S0002-9947-1965-0175782-0`; opening principal-result statement on p. 514 is the intended source anchor | Primary proof source identified. Full text, exact premise language, internal theorem dependencies, corrections/errata, and an independently reviewed node crosswalk are not yet archived, so the human axis remains `H1`. |

Bibliographic metadata was checked during intake against the Crossref DOI
record: author Michael Morley, title *Categoricity in power*, journal volume
114, issue 2, year 1965, pages 514-538. This live metadata lookup is discovery
evidence, not an immutable primary-source receipt.

## Claim crosswalk

| Canonical component | Source relationship | Planned Lean surface | Intake assessment |
|---|---|---|---|
| `L` is a countable first-order language and `T` is an `L`-theory | Standard scope of Morley's transfer theorem; the repository wording omits it | Language syntax, theory, satisfaction, and a countability predicate | Required root restriction; precise source convention remains open |
| `T` is categorical in some uncountable cardinal `kappa` | Antecedent of the principal result | Existence of a `T`-model of cardinality `kappa` plus uniqueness up to `L`-structure isomorphism | Existence is made explicit to prevent a vacuous antecedent |
| For every uncountable `lambda`, `T` is categorical in `lambda` | Transfer conclusion customarily called Morley's categoricity theorem | Universal cardinal binder, model existence at `lambda`, and pairwise isomorphism | Frozen human root; exact cardinal and isomorphism APIs remain open |
| Completeness of `T` | Often built into textbook formulations or derivable from categoricity plus an infinite model | Either an explicit hypothesis or a checked reduction | Must be settled against the primary source; it cannot be silently added or dropped |
| Spectrum formulation | Restates the same transfer as an all-or-none uncountable categoricity spectrum | Checked `iff`/logical transport candidate | Candidate only; no machine witness exists |

## Fidelity boundary

The repository phrase "characterization of uncountably categorical theories"
could be read more broadly than the transfer theorem, for example as a later
structural characterization. The target name, attribution, and year support
the standard Morley transfer theorem, which is therefore frozen for this
planned instance. The statement phase must stop rather than substitute a
different characterization if inspection of the primary source or upstream
target provenance contradicts that reading.

No `H0` claim is made. Acceptance still requires an archived source edition,
page-level assumption and conclusion mapping, errata/correction search,
source-to-obligation mapping after the registry exists, and independent
review.
