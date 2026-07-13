# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6847-6852` supplies exactly:

| Catalog field | Verbatim value | Intake interpretation |
|---|---|---|
| title | `Vosper定理` | named theorem family, but no theorem locator |
| attribution | `A.G. Vosper` | matches the exact-topic 1956 primary papers |
| time | `1956` | matches both the original article and addendum |
| statement | `Cauchy-Davenport定理的逆` | family gloss, not a binder-complete proposition |
| importance | `高` | metadata only |
| formalization status | `已验证` | explicitly untrusted under rev-5.6 |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Their exact extract has SHA-256
`13c22cef72e670dcbb0ac0bf19ac431272d3a5b5d7e0b34e7860d35841395a8f`. The record has no citation,
formula, definition chain, assumptions, conclusion, proof boundary, errata, or formal declaration.

The stable-ID history has one material trap. Before Stage0 deduplication, the Vosper record was
`THM-M-0964`, while bare ID `THM-M-0937` denoted Caucal's theorem. Commit
`c61be3c80710c07c5f7626e3404e51f40ecb39a6` renumbered Vosper to current `THM-M-0937`.
Provenance must bind the current ID to the title, attribution, and gloss; a pre-dedup ID-only lookup
is invalid.

`Docs/Stage0_Blueprint.md:25552-25577` repeats the target and explicitly leaves the formal system,
foundation, precise definitions and premises, proof path, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Its exact current extract has SHA-256
`e5abca027c94623e9ed5d0a2d89e8bf54d986ca092108d6c88b3bb0863564696`.

## Primary-source leads

Crossref identifies two A. G. Vosper papers in the *Journal of the London Mathematical Society*:

| Source | Stable locator | Intake status |
|---|---|---|
| *The Critical Pairs of Subsets of a Group of Prime Order*, volume s1-31, issue 2 (April 1956), pp. 200-205 | DOI `10.1112/jlms/s1-31.2.200` | exact-topic primary article; bibliographic metadata confirmed, theorem text and proof not inspected |
| *Addendum to "The Critical Pairs of Subsets of a Group of Prime Order"*, volume s1-31, issue 3 (July 1956), pp. 280-282 | DOI `10.1112/jlms/s1-31.3.280` | primary correction/extension boundary; bibliographic metadata confirmed, text not inspected |

Crossref response metadata agrees on author, title, journal, date, pagination, and DOI. The
publisher DOI route returned an access challenge, its text-mining endpoint returned HTTP 400 with
an empty body, and Semantic Scholar classified the primary article as closed with no open PDF.
No primary theorem wording, proof, assumptions, or errata relation is therefore claimed from those
access attempts. The addendum is itself a mandatory correction-history input, not a reason to
assume the original article alone is current.

## Inspected exact secondary lead

T. Boothby, M. DeVos, and A. Montejano, *A New Proof of Kemperman's Theorem*,
arXiv:1301.0095v2 (16 March 2013), Theorem 1.3 ("Vosper, version I"), printed page 3. The inspected
20-page PDF is 197,059 bytes with SHA-256
`641f3122cdce22d2358ed8f079c9e1d909f92d2ab53e62c64971f256663f38e8`.

The paper defines `A + B`, deficiency `|A| + |B| - |A + B|`, and a critical pair as one with
positive deficiency. Theorem 1.3 assumes `p` prime and `A, B` nonempty subsets of `Z/pZ`, then
classifies every critical pair into the four outcomes recorded in `scope-map.md`. Its references
cite both Vosper papers above.

This is an exact, immutable, inspectable secondary restatement and supports provisional `H1`: a
complete published proof family is known. It does not support `H0`. The catalog does not cite this
paper or select its "version I" root; the primary theorem and addendum were not inspected; and no
complete primary premise/assumption/errata/proof-node map or independent source review exists.

## Phrase-to-proposition crosswalk

| Repository phrase | Source component | Prospective Lean component | Intake result |
|---|---|---|---|
| Cauchy-Davenport theorem | forward lower bound for nonempty subsets of `Z/pZ` | pinned `ZMod.cauchy_davenport` | exact adjacent theorem, not target or proof credit |
| inverse | critical/equality cases force exceptional or progression structure | implication or four-way classification over finite sumsets | exact root and logical organization open |
| Vosper theorem | original article plus addendum; later "version I" classification | one source-reviewed canonical proposition | family identified; source selection open |
| prime-order group | subsets of `Z/pZ`, `p` prime | `Finset (ZMod p)` is a likely encoding | carrier and transport not frozen |
| arithmetic progressions with common difference | fourth classification branch | an exact arbitrary-length finite progression predicate | definition, length, wraparound, and nonzero-difference policy open |
| verified | catalog status | no proposition or proof term | rejected as H/M evidence |

## Variant crosswalk

| Candidate root | Relationship to the strongest candidate | Admission boundary |
|---|---|---|
| full critical-pair four-way classification | exact secondary Theorem 1.3 | strongest inspected candidate; primary fidelity and catalog selection open |
| equality-case theorem with `|A+B| = |A|+|B|-1` | eliminates some critical-pair cases only with additional size/non-saturation hypotheses | cannot become canonical without exact hypotheses and checked derivation from/to the selected source root |
| progression-only conclusion | fourth branch after excluding saturation, complement, and singleton cases | materially stronger conclusion under materially stronger premises; never substitute silently |
| affine-normalized interval form | translate and scale progressions to consecutive residues | requires nonzero/unit difference and checked affine transports |
| statement over an arbitrary prime-order group | equivalent in ordinary mathematics to a `Z/pZ` formulation after choosing an isomorphism | choice, carrier, cardinal, and transport obligations must be explicit |

## Formal crosswalk

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies
`ZMod.cauchy_davenport` in `Mathlib.Combinatorics.Additive.CauchyDavenport`:

```text
{p : Nat} -> p.Prime -> {s t : Finset (ZMod p)} -> s.Nonempty -> t.Nonempty ->
  min p (s.card + t.card - 1) <= (s + t).card
```

The probe also authenticates finite-set, pointwise-sum, range, and image interfaces. A bounded
repo-local and pinned-mathlib search found no declaration named for Vosper and no exact inverse
classification candidate. The three-term arithmetic-progression library does not directly encode
arbitrary finite progressions appearing in the candidate theorem.

No canonical Lean statement, formal module, expression hash, environment fingerprint, or proof
body is credited. The provisional root is `[H1, M4, R4]`; no H0, M0, R0, accepted state, audit
completion, or theorem completion is claimed.

## Source gate

Before statement acceptance, accountable reviewers must obtain and lawfully preserve the primary
article and addendum, select the exact root, map every incorporated definition, binder, assumption,
exceptional branch, conclusion, proof dependency, and boundary case, audit corrections and errata,
reconcile the candidate variants, and independently approve the crosswalk. Until then the
canonical mathematical and Lean statements remain null.
