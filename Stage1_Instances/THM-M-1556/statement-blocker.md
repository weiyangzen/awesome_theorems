# Exact-statement gate: blocked

Item: `S56-M-1556-STATEMENT`  
Theorem: `THM-M-1556`  
Base revision: `2471626e15270bc76934bc81b54ed509898577f6`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
manifest supplies only the title "soliton theory". The Stage0 source expands it only to "the
mathematical theory of solitons" and explicitly leaves the precise definitions, premises, proof,
dependencies, axioms, and machine artifact to be supplied. These words name a field of study, not
a proposition with domains, ordered binders, hypotheses, and a conclusion.

The accepted intake identifies two historical primary-paper anchors but deliberately selects
neither as the canonical claim. Zabusky and Kruskal's 1965 paper concerns numerical KdV recurrence
and collision observations, while Gardner, Greene, Kruskal, and Miura's 1967 paper announces the
inverse-scattering method for the KdV initial-value problem. Neither a citation nor the shared KdV
setting determines which result this repository intends. Plausible choices such as an explicit
one-soliton identity, inverse-scattering reconstruction, an N-soliton construction, or orbital or
asymptotic stability are inequivalent theorems rather than alternate encodings.

In particular, the supplied record does not fix:

- the equation (KdV, modified KdV, nonlinear Schrodinger, sine-Gordon, KP, Toda, or another model)
  and its coefficient and sign conventions;
- the meaning of soliton, the spatial and time domains, scalar field, and solution notion;
- function spaces, differentiability, decay, initial data, parameter restrictions, or time
  interval;
- whether the conclusion is an explicit solution identity, existence, uniqueness, reconstruction,
  collision behavior, stability, or completeness;
- the quantifier order or treatment of zero-amplitude, zero-speed, coincident-parameter, and other
  boundary cases.

Each choice changes the mathematical claim. Choosing a convenient KdV identity or an abstract
certificate would therefore substitute a narrower theorem and violate the rev-5.6 exact-statement
gate. No Lean declaration, axiom, placeholder, assumed certificate, or neighboring theorem was
introduced. The phase fails at canonical human-claim identity, before minimal imports, expression
serialization, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutations can be performed. Machine state remains `M4`;
statement acceptance, audit completion, and theorem completion are false.

## Pinned environment and validation

Commands were run from this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical
`.lake` artifacts were inspected read-only. No update, build, clone, fetch, or dependency mutation
was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1556` | 0 | rank 568; planned; L0/rework required; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for `THM-M-1556`, the Chinese/English titles, and the supplied gloss | 0 | only underspecified metadata, scheduling records, the owned intake dossier, and a neighboring Hirota source reference were found; no source-frozen proposition exists |
| pinned-mathlib `rg` search for `soliton`, `inverse scattering`, `reflectionless`, `Korteweg`, and `KdV` in `Mathlib/**/*.lean` | 1 | no matches; exit 1 is ripgrep's no-match result and does not establish a substitute claim |

There is no applicable `lake env lean <target>.lean` command: the required exact expression does
not exist. Elaborating an invented interface would be false positive evidence rather than the
assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact numbered or
displayed proposition, record its page and wording, audit errata, and freeze every equation,
normalization, domain, solution, regularity, decay, parameter, quantifier, conclusion, and boundary
choice listed above. It must also explain why that proposition is the intended meaning of this
repository target rather than one of the separately scheduled KdV, Hirota, Zakharov-Shabat, or
AKNS targets. A later statement run can then encode the exact claim with real definitions, minimize
the pinned imports, serialize and fingerprint the elaborated expression, check credited
transports, and run all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
