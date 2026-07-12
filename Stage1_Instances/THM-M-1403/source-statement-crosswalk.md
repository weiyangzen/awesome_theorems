# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:10250`-`:10255` is the sole source record. It gives the title
`拓扑熵`, attributes it to Adler/Konheim/McAndrew, dates it 1965, and states only
`动力系统的复杂性` ("complexity of a dynamical system"). It gives no definition, proposition,
hypotheses, conclusion, proof, citation, or formal artifact.

`Docs/Stage0_Blueprint.md:38159`-`:38184` repeats those fields and explicitly leaves precise
definitions and assumptions, proof path, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest consequently retains `已验证` only as
`source_status_untrusted` and starts this target at `L0 / rework_required`.

Repository history supplies no deeper source: the six inventory lines originate in the initial
research-corpus commit, and no legacy `THM-M-1403` instance exists in the repository history.

## Bibliographic candidate

The metadata aligns bibliographically with R. L. Adler, A. G. Konheim, and M. H. McAndrew,
"Topological entropy," *Transactions of the American Mathematical Society* **114**(2) (1965),
309-319, DOI `10.1090/S0002-9947-1965-0175106-9`. Crossref metadata confirms the authors, title,
journal, year, volume, issue, and page range.

This is only an `E5` discovery locator at intake. No immutable full text or pinpoint definition or
theorem passage was inspected, no assumptions or proof boundary were transcribed, no errata search
was accepted, and no independent source reviewer approved a mapping. It therefore supplies no
`H0` credit and does not select a canonical claim.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake assessment |
|---|---|---|---|
| `拓扑熵` | an invariant, construction, or theorem family | one exact declaration or expression | family identified; proposition absent |
| Adler/Konheim/McAndrew; 1965 | likely historical source locator | documentation and source review only | bibliography identified; passage open |
| "dynamical system" | a phase space and evolution | space structures, self-map/flow, continuity assumptions | domain and binders open |
| "complexity" | exponential orbit or cover growth | cover joins/minimal cardinality or separated nets, logarithm and asymptotic limit | encoding open |
| "topological" | dependence only on the topological dynamics | a source-selected invariance or factor statement, if intended | no conclusion supplied |
| entropy value | finite, infinite, or empty-case convention | exact codomain and boundary values | conventions open |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Pinned Lean boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` has a substantial
topological-entropy development:

- `Mathlib.Dynamics.TopologicalEntropy.CoverEntropy` documents a Bowen-Dinaburg construction on a
  uniform space for `T : X -> X` and `F : Set X`, valued in `EReal`. It defines
  `Dynamics.coverEntropy` using a limsup and `Dynamics.coverEntropyInf` using a liminf, assigns
  bottom to the empty set, and proves their equality when `T` maps `F` into itself.
- `Mathlib.Dynamics.TopologicalEntropy.NetEntropy` proves equality with a separated-net
  formulation.
- `Mathlib.Dynamics.TopologicalEntropy.Semiconj` proves restriction coherence and nonincrease under
  uniformly continuous semiconjugacy.
- `Mathlib.Dynamics.TopologicalEntropy.Subset` contains monotonicity, closure, and union results.

`IntakeProbe.lean` checks representative declarations at the pin. This is a bounded feasibility
inventory, not the later formal-anchor audit. In particular, the checked mathlib docs identify
their construction as Bowen-Dinaburg, while the repository metadata points to AKM. The source audit
must not equate them without an explicit theorem and convention crosswalk.

## First downstream blocker

Obtain an immutable, independently reviewed source passage that selects one proposition. Record
its exact definition/theorem and page, ordered hypotheses, conclusion, conventions, proof
boundary, and errata. Only then may the statement phase select minimal imports, elaborate and hash
the canonical expression, check any alternate encoding, and run the required mutation tests.
