# Source-statement crosswalk

## Repository record and source boundary

The repository inventory gives the Chinese title "Holder's inequality", Otto Holder, 1889, and
the gloss "duality of L^p spaces". It supplies no primary citation, theorem number, page, exact
statement, or hypotheses. Its `已验证` value is explicitly untrusted under rev-5.6.

The title and gloss conflict. Holder's integral inequality supplies the bounded pairing used in
the easy direction of `L^p` duality, but it does not by itself prove that every continuous linear
functional is represented by an `L^q` function. Moreover, `THM-M-0279` is the repository's
separate real-analysis entry with the gloss "product integral in L^p spaces". This dossier therefore
preserves the functional-analysis gloss as its provisional family while requiring a later source
review to correct the attribution and select the exact representation theorem.

Standard functional-analysis texts are discovery leads, not primary `H0` evidence. The statement
phase must select an immutable edition and pinpoint theorem, inspect its conventions and errata,
and obtain independent approval. No edition or locator is invented here.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "duality of L^p spaces" | identify `(L^p(μ))'` with conjugate `L^q(μ)` | `MeasureTheory.Lp`, continuous dual, linear isometry equivalence | family included; exact theorem open |
| "Holder's inequality" | boundedness of the integral pairing | integrability/product bound and operator norm estimate | supporting lemma only; not the root |
| conjugate exponents | `1/p + 1/q = 1` with endpoint policy | exponent types and conjugacy predicate | encoding and range open |
| representation | every bounded functional arises by integration | surjectivity and representing function | root conclusion; hypotheses open |
| isometry | norm of functional equals norm of representative | norm-preserving equivalence | included provisionally |
| Otto Holder / 1889 | historical attribution for the inequality | no machine-proof credit | conflicts with duality gloss; review required |

## Human and machine boundary

No formal candidate receives credit at intake. Repository-local files and pinned mathlib may
contain Holder bounds or `L^p` infrastructure, but only the later anchor audit may record exact
modules, declaration types, immutable revisions, proof-body provenance, and whether a candidate
closes the selected root. An inequality theorem, an embedding, or the `p = 2` case must not be
reported as the full duality theorem.

Before `H0`, an independent reviewer must approve the selected source edition and locator, all
measure and exponent hypotheses, scalar/conjugation conventions, endpoint treatment, norm and
uniqueness conclusions, corrections, and the row-by-row source-to-Lean mapping.
