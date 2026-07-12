# Exact-statement gate: blocked

Item: `S56-M-0316-STATEMENT`  
Theorem: `THM-M-0316`  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`

## Decision

No exact Lean 4 target can be truthfully selected from the authoritative repository record. Its
complete mathematical wording is "Riesz-Schauder theory" / "spectral theory of compact
operators". As the accepted intake records, this is an umbrella theory rather than one uniquely
quantified proposition.

Several inequivalent roots remain compatible with that wording: the equivalence between nonzero
spectral values and eigenvalues, finite-dimensionality of the corresponding eigenspaces, zero as
the only possible accumulation point, finiteness of the spectrum outside every neighborhood of
zero, countability, a finite algebraic-multiplicity result, or a Fredholm-alternative formulation.
The metadata also does not fix complex scalars versus mathlib's more general field assumptions,
geometric versus algebraic multiplicity, or which clauses form one conjunction. Choosing only a
convenient available declaration, or assembling a new conjunction, would broaden or substitute
the theorem.

The discovery citations in `source_statement_crosswalk.md` have not been accepted at the level of
an immutable edition, exact theorem/page, incorporated definitions, assumptions, errata, and
independent clause review. Consequently there is no canonical human claim from which to derive
minimal imports, an elaborated-expression fingerprint, checked transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. The exact-statement gate
therefore fails before proof evidence may be inspected. Machine state remains `M3`; statement and
theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` uses the narrow module
`Mathlib.Analysis.Normed.Operator.FredholmAlternative` and checks
`IsCompactOperator.hasEigenvalue_iff_mem_spectrum` and
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet`. This confirms that the pinned environment
contains two intake-listed candidate components. It neither selects the Riesz-Schauder root nor
credits either declaration as closure. The finite-dimensionality, accumulation, countability, and
multiplicity choices remain unresolved.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used read
only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0316` | 0 | rank 818; planned; legacy artifacts unaccepted; theorem incomplete |
| repository search for `THM-M-0316`, the Chinese title, and the English gloss | 0 | found only the umbrella metadata and intake discovery record; no source-frozen proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0316/StatementProbe.lean` | 0 | both candidate APIs elaborated; no canonical target asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0316/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0316 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0316` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary source, select and
transcribe the exact root proposition, fix every scalar, space, compactness, multiplicity,
topological, and boundary convention, dispose of errata, and independently approve the mapping.
Only then can a statement worker encode that same claim, minimize imports, fingerprint the
elaboration, check alternate transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
