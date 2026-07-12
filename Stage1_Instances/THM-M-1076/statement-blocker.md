# Exact-statement gate: blocked

Item: `S56-M-1076-STATEMENT`  
Theorem: `THM-M-1076`  
Base revision: `1a19c121b34bfc2825a510958326294a95c9deb9`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository material.
That material gives only the title "Smith's key renewal theorem", attributes it to Walter Smith,
and glosses it as "limit behavior of renewal processes". It gives no mathematical formula and no
immutable primary-source theorem/page. The intake correctly records the Smith and Feller references
only as uninspected bibliographic leads.

The missing choices alter the proposition, rather than merely its notation:

- ordinary, delayed, or real-line random-walk renewal;
- nonarithmetic or lattice increments and, in the lattice case, the maximal span;
- nonnegative support, properness, and finite-positive-mean assumptions;
- whether the renewal measure includes the zeroth convolution power;
- the test-function codomain and exact direct-Riemann-integrability predicate;
- the convolution interval, translation sign, boundary mass, and integral normalization; and
- an integral limit, span-dependent lattice sum, or another mode of convergence.

Thus adopting the familiar nonarithmetic formula for a directly Riemann integrable function would
invent the variant and its premises. Substituting Blackwell's theorem would use separately scheduled
target `THM-M-1077`; substituting the elementary renewal theorem would be weaker. Encoding an
abstract predicate or assuming the desired limit would not identify the theorem.

The failure precedes minimal-import selection, elaborated-expression serialization, checked
transports, and meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutation
tests. No Lean declaration, theorem proof, machine credit, audit completion, or theorem completion
is claimed. Machine state remains `M4`.

## Pinned environment and validation

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` link was
already present and was used read-only; no update, build, clone, fetch, or dependency mutation was
run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and the 1546-target uniform-L0 check |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1076` | 0 | Confirmed rank 518, planned lifecycle, unaccepted legacy artifacts, and theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 values `651c8a...1d2` and `321626...d81` recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the ID, title, gloss, Walter Smith, and candidate paper title | 0 | Found only sparse catalogue metadata, the intake dossier, and adjacent target boundaries; no exact proposition |
| pinned-mathlib `rg` search for renewal-process, renewal-measure, key-renewal, direct-Riemann-integrability, Blackwell, and Walter Smith terms | 1 | No matches; exit 1 is the expected no-match result |

There is no applicable `lake env lean <canonical-target>.lean` command: no exact target exists.
Elaborating a chosen textbook variant would be substituted-statement evidence, not validation of
the assigned deliverable.

## Retry condition

An accountable reviewer must preserve an immutable primary-source edition, transcribe and
independently audit the exact numbered theorem and its definitions, dispose of errata, and freeze
every model, arithmetic, measure, function-class, boundary, and normalization choice above. A later
statement run can then implement that exact claim, minimize imports, serialize the expression,
check credited transports, and execute the four structural mutation classes.

This is the first failed gate. The assigned phase is not genuinely self-tested to completion, so no
`.stage1-worker-selftest.json` is emitted.
