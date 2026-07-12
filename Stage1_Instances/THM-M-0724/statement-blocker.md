# Exact-statement gate: blocked

Item: `S56-M-0724-STATEMENT`  
Theorem: `THM-M-0724`  
Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title "PSPACE completeness" and the gloss "PSPACE-complete
problems". Completeness is a property of a named decision language relative to a specified class
and reduction; the record names no language and does not state either membership or hardness.

Several inequivalent propositions fit that wording: TQBF is PSPACE-complete, another named problem
is PSPACE-complete, some PSPACE-complete language exists, or multiple problems have the property.
The nearby `IP = PSPACE` entry is a separate target. Choosing TQBF, an abstract language, or that
class equality would therefore invent or substitute mathematics rather than elaborate the exact
repository claim.

Even after a subject is chosen, the source must fix the input alphabet and encoding, malformed-input
behavior, deterministic machine and halting conventions, read-only input and counted work space,
the polynomial-bound convention, and the reduction class (for example polynomial-time or logspace
many-one reductions). These choices change the domains, ordered binders, hypotheses, and conclusion.
No primary-source edition, theorem/page, incorporated definitions, or independent source approval
currently resolves them.

Consequently the section 5.1 canonical-human-claim gate fails before minimal imports, canonical
serialization, an elaborated-expression hash, checked transports, or removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations are meaningful. No Lean declaration,
abstract interface assuming completeness, axiom, placeholder, weakened special case, or broadened
target was introduced. The root vector remains `[H3, M4, R4]`; statement acceptance, audit
completion, and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Computability.Language`,
`Mathlib.Computability.TuringMachine.Computable`, and `Mathlib.Computability.Reduce`. It elaborates
generic languages, a finite Turing-machine package, time and polynomial-time predicates, and
computable many-one reducibility. This is substrate/blocker evidence only: the checked reduction
does not express a resource-bounded reduction, and the checked machine API is time-based rather
than a definition of polynomial work space. A precise bounded search found no `PSPACE` or general
space-complexity declaration in pinned mathlib's computability tree.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Existing canonical `.lake` artifacts were used read-only. No update, build, clone, fetch, or
dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0724` | 0 | rank 761, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | produced the two file hashes and mathlib revision recorded above |
| source `rg` over `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` | 0 | both duplicate inventory rows contain only the same underspecified title, gloss, attribution, and decade; Stage0 leaves definitions and premises open |
| `rg -n -i '\\bpspace\\b\|spacecomplexity\|space_complexity\|polynomialspace\|polynomial_space\|polyspace\|poly_space' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability --glob '*.lean'` | 1 | no exact PSPACE or general space-complexity name found (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0724/IntakeProbe.lean` | 0 | the six generic substrate declarations elaborated; this is not statement credit |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0724 -g '*.lean'` | 1 | no prohibited placeholder or axiom found (`rg` exit 1 means no match) |

There is no applicable `lake env lean <canonical-statement>.lean` check because the exact expression
does not exist. Manufacturing a generic completeness predicate and quantifying over an unnamed
language would not validate the assigned deliverable.

## Retry condition

An accountable source decision must preserve and hash an immutable primary source, select one exact
theorem and named decision problem, transcribe its definitions and assumptions, dispose of errata,
and independently approve the crosswalk. It must freeze all encoding, machine-space, polynomial
bound, reduction, malformed-input, and boundary conventions listed above. A later statement run can
then encode precisely that claim, minimize its pinned imports, fingerprint the elaborated expression,
check any alternate transports, and run the required semantic mutations.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
