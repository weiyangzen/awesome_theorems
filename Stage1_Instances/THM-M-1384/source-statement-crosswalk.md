# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10083-10088` supplies exactly the title
`Sturm-Liouville理论`, attribution `Jacques Sturm/Joseph Liouville`, date 1836, gloss
`二阶线性边值问题`, importance `high`, and status `已验证`. Git history places all six uncited
lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37641-37666` repeats that metadata but explicitly leaves background,
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked state, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The catalog supplies no bibliography, equation, interval, coefficients, boundary conditions,
binders, hypotheses, theorem conclusion, proof boundary, correction history, or reviewer. It does
not identify a stable proposition.

## Literal crosswalk

| Repository element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `Sturm-Liouville理论` | equation family, regular or singular BVP, operator theory, spectral or oscillation results | source-selected structures and a precise `Prop` | a theory name is not truth-valued |
| `二阶线性` | classical scalar ODE, weak equation, weighted self-adjoint expression, first-order system | derivative predicates, `IsIntegralCurve`, source-defined operator | sign, weight, regularity, and equality semantics absent |
| `边值问题` | separated, mixed, periodic, coupled, regular, or singular endpoint data | endpoint evaluation and a source-defined boundary predicate | interval and all boundary forms absent |
| Sturm/Liouville, 1836 | historical family or publication milestone | immutable edition, theorem/page, proof and errata map | joint attribution and exact event need review |
| `已验证` | untrusted inventory label | H0 review and kernel receipt would be required | no H or M credit |

## Inspected source-family leads

### Historical primary lead

C. Sturm, *Memoire sur les Equations differentielles lineaires du second ordre*, *Journal de
Mathematiques Pures et Appliquees*, series 1, volume 1 (1836), pages 106-186, was inspected from
the stable NUMDAM record `JMPA_1836_1_1__106_0`. The 82-page PDF has SHA-256
`dac79254915e753884f6dd68865ef5c7165043599ac611558c6c4d6045feac96`. The volume's linked errata
scan has SHA-256 `ed7f4db1783207a385546e47c43f8c952352ebedda823e62e0e611918a962cd7`
and includes corrections keyed to pages of the memoir. The article studies qualitative properties
of second-order linear equations, but the catalog does not cite a passage. The inspected article is
Sturm-authored and reports an earlier Academy reading; it does not by itself validate the catalog's
joint attribution/date genealogy. Exact passage, translation, proof-node, and errata mapping and an
independent review remain open.

### Modern discriminators

NIST DLMF Section 1.13(viii), `Eigenvalues and Eigenfunctions: Sturm-Liouville and Liouville
forms`, equations 1.13.26-1.13.31, was inspected in release 1.2.7 dated 2026-06-15; the page records
that this subsection was added effective with version 1.2.0 on 2024-03-27. It presents a
finite-interval regular system, coefficient sign assumptions, unmixed or periodic boundary
conditions, eigenvalues, and a Liouville normal-form transformation. The captured HTML has SHA-256
`7f26b662c796979362e9f4cffeb56f0efa549ae6f4d811bca31d6fd289fb0386`.

The Encyclopedia of Mathematics entry `Sturm-Liouville problem`, immutable revision 55171, was
also inspected. It begins with a weighted equation plus unspecified boundary conditions, explicitly
splits regular from singular problems, and then treats finite, half-line, and whole-line regimes.
Its regular separated-boundary discussion includes several distinct spectral and completeness
claims. The captured revision has SHA-256
`61825440e21804c2532727f3fda8f8936e3493856fd96b955a5e0c4478357523`.

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, AMS GSM 140 (2012),
Sections 5.3-5.6, was inspected in the author-hosted publisher-permitted preliminary edition. Its
SHA-256 is `362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`;
the official errata captured during intake has SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`.
The sections distinguish the equation, regular operator/domain and boundary forms, Green
resolvent, a multi-clause spectral theorem, lower bounds, oscillation, and periodic problems.

These sources establish a serious family and demonstrate its ambiguity. The repository cites and
selects none of them, and no source has an accepted independent review. They supply no canonical
statement or H0 credit.

## Candidate component crosswalk

| Candidate component | Source-family evidence | Prospective pinned Lean surface | Missing decision |
|---|---|---|---|
| differential expression | weighted second-order expressions occur in every modern lead | `HasDerivAt`, `deriv`, ODE or source-defined operator | exact derivative and operator-domain encoding |
| interval/endpoints | regular finite and multiple singular regimes occur | real intervals, filters, measures | one domain and endpoint classification |
| boundary conditions | separated and periodic examples occur | endpoint equality predicates | exact form and self-adjointness constraints |
| solution/eigenfunction | classical nonzero solutions and operator vectors occur | functions, `IsIntegralCurve`, `HasEigenvalue` after modeling | regularity, equality, and nonzero conventions |
| theorem conclusion | solvability, spectral, basis, oscillation, and transport claims occur | a source-defined `Prop` | one root or delimited conjunction |
| abstract substrate | compact symmetric spectral tools are pinned | symmetric maps, spectrum, eigenspaces, Rayleigh APIs | checked bridge from differential problem |

No row is a canonical statement, checked transport, formal anchor, or proof body.

## Source and statement gate

Because the received root is H5, the integration lane must first approve a corrected stable
proposition or redirect the record to another rev-5.6-permitted target form. Accountable reviewers
must then preserve an immutable primary or authoritative source and transcribe every incorporated definition, binder, hypothesis, conclusion,
boundary convention, proof boundary, historical attribution, and correction, reconcile the
neighboring target scopes, and independently approve the mapping. The statement phase must then
elaborate the exact Lean expression with minimal pinned imports, fingerprint the expression and
environment, add checked transports, and run all four required mutation classes.

Until then the root remains `[H5, M4, R4]`; the canonical mathematical and Lean targets are null,
and ordinary proof execution is blocked without implying that established Sturm-Liouville results
are false or mathematically open.
