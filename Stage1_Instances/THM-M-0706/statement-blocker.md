# Exact-statement gate: blocked

Item: `S56-M-0706-STATEMENT`

Theorem: `THM-M-0706`

Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
mathematics inventory says only `可计算性的等价定义` ("equivalent definitions of
computability"), while the computer-science inventory gives the philosophical claim that every
intuitively computable function is computable by a Turing machine. The intake correctly preserves
this conflict and leaves the canonical formal target open.

The first wording is a family of inequivalent formal results. It does not identify the two models,
their syntax and semantics, input and output domains, totality or partiality, number and tuple
encodings, treatment of divergence, or whether "equivalent" means pointwise representability,
equality of function classes, or effective translations in both directions. The second wording has
no fixed formal extension for "intuitively computable". Defining that phrase to mean Turing-
computable would make the result circular; postulating its relationship to Turing computability
would make the desired conclusion an assumption.

Church's and Turing's 1936 work gives historically relevant boundaries, but this dossier does not
contain an accepted immutable edition, pinpoint proposition, incorporated definitions and
assumptions, errata disposition, or independent source review selecting one exact formal theorem.
Choosing a convenient partial-recursive/Turing-machine simulation, lambda-calculus equivalence, or
another model pair would therefore substitute mathematics. There is no canonical expression to
serialize or hash and no sound removed-hypothesis, changed-domain, changed-binder-scope, or boundary
mutation test. The rev-5.6 section 5.1 statement gate fails before proof evidence may be inspected.

## Pinned Lean boundary

`StatementProbe.lean` minimally imports
`Mathlib.Computability.TuringMachine.ToPartrec` and checks
`Turing.PartrecToTM2.tr_eval`. That declaration is a genuine formal simulation result available in
the pinned environment, but it is only feasibility evidence. It neither supplies a definition of
intuitive computability nor decides that this particular model relationship is the repository's
canonical claim. The probe receives no statement or proof credit and contains no `sorry`, `admit`,
or `axiom`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The worker used the existing canonical `.lake` link
read-only; no update, build, fetch, clone, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0706` | 0 | rank 747, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `rg` over the theorem ID and both repository wordings in the two research inventories and Stage0 blueprint | 0 | found only the two conflicting, underspecified claims and open Stage0 fields |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0706/StatementProbe.lean` | 0 | elaborated the `Turing.PartrecToTM2.tr_eval` feasibility check |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0706 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0706/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| scoped `git diff --no-index --check /dev/null <new-file>` loop accepting the ordinary diff exit | 0 | no whitespace errors in any new artifact |

## Retry condition and boundary

An accountable reviewer must preserve and hash an immutable primary source, select and transcribe
one exact formal proposition with all incorporated definitions and assumptions, resolve its
relationship to the informal thesis, audit errata, and independently approve the mapping. Only
then can a statement worker encode that same claim, minimize imports, fingerprint the elaborated
expression, check alternate transports, and run all four mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The root
remains `[H3, M4, R4]`; `audit_complete` and `theorem_complete` remain false. The assigned phase is
not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
