# Exact-statement gate: blocked

Item: `S56-M-0332-STATEMENT`  
Theorem: `THM-M-0332`  
Base revision: `106084d7f6343f3046dfb9e108503edbcdc86191`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
only mathematical wording is `全纯函数演算的谱` ("the spectrum of the holomorphic functional
calculus"). This identifies a theorem family, but it is not a proposition and does not freeze the
ambient algebra, element or operator, function domain, notion of holomorphicity, functional
calculus construction, hypotheses, conclusion, or boundary conventions. The record supplies no
primary or authoritative edition, theorem/page, incorporated definitions, assumptions, errata
disposition, or independent source mapping.

Several materially different statements remain compatible with the gloss: the equality
`spectrum (f(a)) = f '' spectrum(a)` for an element of a complex unital Banach algebra; an operator
version on a complex Banach space; a nonunital version through unitization; or only one inclusion
under weaker hypotheses. Even the conventional equality leaves open whether `f` is defined on an
explicit open neighborhood or only near the spectrum, how the calculus value is represented, and
how constant functions, the zero algebra, empty spectra, and disconnected neighborhoods are
handled. Selecting those choices from memory would invent missing mathematics or substitute a
narrower continuous or polynomial calculus theorem.

Consequently there is no canonical human claim from which to select minimal imports, serialize and
hash an elaborated expression, prove checked transports, or perform sound removed-hypothesis,
changed-domain, binder-scope, and boundary mutation tests. The rev-5.6 exact-statement gate fails
before formal-anchor or proof evidence may receive credit. The machine state remains `M4`;
statement elaboration, audit completion, and theorem completion are false.

## Pinned Lean boundary

`IntakeProbe.lean` was re-elaborated in the pinned environment. It confirms the generic `spectrum`
API, the continuous-functional-calculus theorem `cfc_map_spectrum`, and two polynomial spectral
mapping theorems. None encodes a source-selected holomorphic functional calculus, so the probe is
substrate evidence only and receives no canonical-statement or proof credit. A repository search of
the pinned mathlib source found polynomial and continuous spectral mapping implementations but no
holomorphic-functional-calculus construction that could silently resolve the missing source
choices.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0332` | 0 | rank 825; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -i 'THM-M-0332\|谱映射定理\|全纯函数演算的谱\|holomorphic functional calculus' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | only the topic/gloss and open Stage0 fields were found; no exact proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0332/IntakeProbe.lean` | 0 | hashes `651c8a...b1d2`, `321626...2d81`, and `d26b5c...46f` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `rg -n -i 'holomorphic.*(calculus\|spectrum)\|functional calculus.*holomorphic\|spectral mapping' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only nearby polynomial and continuous spectral mapping implementations; no exact holomorphic target |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0332/IntakeProbe.lean` | 0 | five nearby spectrum/CFC/polynomial API checks elaborated; no canonical target asserted |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0332 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in target Lean files |
| `python3 -m json.tool Stage1_Instances/THM-M-0332/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0332` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary or authoritative source,
transcribe one exact theorem with all incorporated definitions and assumptions, resolve the domain
and functional-calculus choices and boundary cases above, dispose of errata, and obtain independent
approval of the mapping. A later statement run can then encode that same claim, minimize pinned
imports, fingerprint the elaborated expression, check alternate transports, and execute all four
required statement mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
