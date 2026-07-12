# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10390`-`:10395` supplies exactly the title `Young塔`, the
attribution Lai-Sang Young, the year 1998, the gloss `非一致双曲系统的工具`, importance
"high", and status `已验证`. The six-line record was introduced in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no bibliography, definition, formula,
theorem statement, or proof.

`Docs/Stage0_Blueprint.md:38672`-`:38697` repeats those fields and explicitly leaves exact
definitions and premises, proof path, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Its generic claims that a closed result is known are planning boilerplate, not
source evidence. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

## Primary-source candidate

The inspected candidate is Lai-Sang Young, *Statistical Properties of Dynamical Systems with Some
Hyperbolicity*, *Annals of Mathematics* **147**(3) (1998), 585-650, DOI
`10.2307/120960`. Crossref metadata confirm author, title, journal, volume, issue, year, and starting
page. An author-hosted 63-page copy at
`https://cims.nyu.edu/~lsy/papers/towers-billiards.pdf` had SHA-256
`549fdc2ec536da6e4c4d83bb6454e6c808c16acd803b5543cd3536c4add69171` when inspected.

The paper's Sections 1.1-1.2 specify a hyperbolic product set, countably many branches and return
times, separation, contraction, distortion, and absolute continuity as P1-P5. Section 1.3 constructs
the Markov extension over the return map. Section 1.4 then gives three distinct main results:

- Theorem 1: return-time integrability implies existence of an SRB measure.
- Theorem 2: an exponential return-time tail and ergodicity of every positive iterate imply
  exponential decay of correlations for Holder observables.
- Theorem 3: under Theorem 2's hypotheses, centered Holder observables satisfy a central limit
  theorem, with zero variance exactly for an `L2` coboundary.

This confirms the catalog's broad subject and year, but it also exposes the blocker: the catalog
does not select the construction or one of these propositions. Intake does not claim `H0` because
no canonical root has been approved, a full definition/assumption/errata crosswalk has not been
completed, and no independent source reviewer has accepted the mapping.

## Component crosswalk

| Repository/source element | Mathematical component to freeze | Required Lean component | Intake assessment |
|---|---|---|---|
| `Young塔` | construction, theorem family, or later generalized notion | no single `Prop` follows from a construction name | not a stable proposition |
| "nonuniformly hyperbolic" | exact system class and hyperbolic product data | phase type, dynamics, invariant set, stable/unstable structures, regularity | all open |
| "tower" | Markov extension over a return map under `R` | base, branch partition, return time, level subtype/sigma type, tower map, projection | construction candidate only |
| "tool" | one derived statistical theorem or application | exact hypotheses and one conclusion | conclusion absent |
| P1-P5 | product structure, returns, separation, contraction, distortion, absolute continuity | source-faithful bundled or explicit predicates and ordered binders | candidate assumptions, not catalog-selected |
| return-time condition | integrability or exponential/other tail | measure, integral or tail inequality, constants, coercions | theorem-dependent |
| statistical conclusion | SRB existence, mixing, or CLT | exact measure/observable/rate/distribution proposition | three distinct roots |
| Lai-Sang Young / 1998 | likely paper provenance | documentation and source review only | strong candidate, no accepted mapping |
| `已验证` | untrusted inventory metadata | inspectable kernel and human-source receipts would be required | no H or M credit |

## Variant and neighbor boundary

Constructing the extension does not by itself prove that it carries a finite invariant measure.
SRB existence does not imply exponential mixing without the tail and aperiodicity conditions.
Mixing is not the central limit theorem, and the CLT introduces observable, centering, variance,
and coboundary data. Polynomial and stretched-exponential tails yield different conclusions from
Young 1998's exponential-tail result.

The Kakutani/Rokhlin towers, finite Markov partitions, general SRB-measure results, Pesin theory,
and the Pesin entropy formula have their own repository IDs. Their availability cannot choose or
close this root.

## Source gate

Before the target can leave `H5`, an accountable reviewer must approve a corrected truth-valued
root, preserve and hash an immutable primary edition, identify an exact theorem and every referenced
definition, map all ordered binders and hypotheses, check corrections and errata, resolve whether
the catalog intends Young 1998 or a later tower theorem, and obtain independent approval. The
statement phase must then encode exactly that choice without conclusion-bearing placeholder fields.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded spelling
search (including concatenated, dotted, underscored, spaced, and hyphenated variants) found no
Young-tower, Gibbs-Markov-tower, return-time-tower, or inducing-scheme occurrence in Lean sources.
`IntakeProbe.lean` verifies representative APIs for `Function.iterate`, `birkhoffSum`, set and
measure restriction, `MeasurePreserving`, and `Ergodic`. They are generic ingredients only, not a
complete formal-candidate audit and not evidence for a canonical target.

The canonical module, declaration or expression, elaborated-expression hash, checked transports,
and statement mutations remain null. No H0, M0, or readable-proof closure is claimed.
