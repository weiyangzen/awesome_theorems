# Exact-statement gate: blocked

Item: `S56-M-1403-STATEMENT`

Theorem: `THM-M-1403`

Base revision: `95073b656f2c285c788e4814325a47fdb4dc1879`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record gives the title `拓扑熵` ("topological entropy"), attributes it to
Adler/Konheim/McAndrew in 1965, and gives only the gloss `动力系统的复杂性` ("complexity of a
dynamical system"). That is a topic and invariant, not a truth-valued proposition. Stage0 leaves
the exact definitions, assumptions, proof path, equivalent forms, axioms, and formal artifact open.
The source label `已验证` is explicitly untrusted under rev-5.6.

The accepted intake records the likely bibliographic source, R. L. Adler, A. G. Konheim, and
M. H. McAndrew, "Topological entropy," *Transactions of the American Mathematical Society*
**114**(2) (1965), 309-319, DOI `10.1090/S0002-9947-1965-0175106-9`. It also records that no
immutable full text, pinpoint definition or theorem passage, incorporated assumptions, errata, or
independent source review has been accepted. Its structured fields therefore leave both the
canonical claim and formal expression null.

Several inequivalent targets remain compatible with the metadata: the historical finite-open-cover
definition, well-posedness of an asymptotic construction, equality with a Bowen-Dinaburg or
separated-net formulation, conjugacy invariance, factor monotonicity, restriction coherence, or an
entropy computation for a particular system. They differ in phase-space structure, dynamics,
continuity, subset invariance, cover and logarithm conventions, asymptotic operator, codomain,
ordered binders, hypotheses, conclusion, and boundary cases. Selecting any one would broaden or
substitute the received target rather than elaborate it exactly.

Consequently there is no canonical human proposition from which to derive a minimal import,
normalized kernel-expression fingerprint, credited alternate transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. The rev-5.6
statement gate fails at exact source-statement identity before proof evidence may be inspected.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.Dynamics.TopologicalEntropy.NetEntropy` and
`Mathlib.Dynamics.TopologicalEntropy.Semiconj`. It re-elaborates these six candidate interfaces:

- `Dynamics.coverEntropy (T : X -> X) (F : Set X) : EReal`;
- `Dynamics.coverEntropyInf (T : X -> X) (F : Set X) : EReal`;
- equality of those values when `T` maps `F` into itself;
- equality of cover entropy with a supremum of separated-net entropy;
- coherence under restriction to an invariant subset; and
- nonincrease of entropy under a uniformly continuous semiconjugacy.

Pinned mathlib explicitly documents these modules as implementing Bowen-Dinaburg entropy on a
uniform space and subset. The repository metadata instead points historically to
Adler-Konheim-McAndrew, and no checked source or formal transport presently identifies one of these
interfaces as the exact root. The probe is feasibility evidence only. It is not a canonical target,
does not establish a minimal import for an unknown target, and receives no statement or proof
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing `Formalizations/Lean/.lake` link
points to the canonical checkout's pinned artifacts and was used read-only. No update, build,
clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1403` | 0 | rank 902; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short && git rev-parse HEAD && readlink Formalizations/Lean/.lake` | 0 | base revision above; only the pre-existing untracked `.lake` link was present before this statement work; it targets the canonical pinned artifacts |
| `rg -n '拓扑熵\|动力系统的复杂性\|Adler/Konheim/McAndrew' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the topic/gloss record and Stage0 fields that leave exact theorem data open |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | toolchain hash `651c8acc...b1d2`, manifest hash `321626c8...2d81`, and mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1403/IntakeProbe.lean` | 0 | all six candidate entropy interfaces elaborated with their exact pinned types; no canonical theorem asserted |
| `rg -n -i 'Adler\|Konheim\|McAndrew' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics/TopologicalEntropy -g '*.lean'` | 1 | expected no-match exit; no historical-author crosswalk occurs in the bounded pinned modules |
| `rg -n 'Bowen-Dinaburg' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics/TopologicalEntropy -g '*.lean'` | 0 | pinned cover, net, and dynamical-entourage modules identify their formulation as Bowen-Dinaburg |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-1403 --glob '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom occurs in target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-1403/statement-blocker.json` | 0 | structured blocker is valid JSON |
| per-file `git diff --no-index --check -- /dev/null <new statement-blocker file>`, accepting exit 1 as the normal added-content difference and rejecting exit greater than 1 | 0 | both new owned-path files passed the whitespace check |

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary source, select and transcribe
one exact proposition with all incorporated definitions and a pinpoint locator, audit errata,
resolve the AKM/Bowen-Dinaburg relationship, and independently approve the source-statement
crosswalk. The selection must freeze the dynamics, phase space, subset, asymptotic and codomain
conventions, ordered binders, hypotheses, conclusion, and all relevant boundary cases. A later
statement worker can then encode that same claim with real Lean definitions, minimize the pinned
imports, serialize and hash the elaborated expression, check alternate transports, and run all four
required statement mutations.

This is the first failed gate, not completion of the statement node or any downstream node. The
provisional root remains `[H5, M3, R4]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
