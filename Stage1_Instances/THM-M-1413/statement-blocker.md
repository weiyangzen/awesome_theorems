# Exact-statement gate: blocked

Item: `S56-M-1413-STATEMENT`

Theorem: `THM-M-1413`

Base revision: `3d1d6d3eb018f17657cae1cfd7d25fc30492a12b` (tree
`3aa3dd324b35549da6cf2c5a54183a63ed1bfff9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1413-INTAKE` has provisional worker state
`[_]`, not master-accepted state `[x]`, so the dependency gate independently prevents acceptance.
More fundamentally, the exact Lean 4 theorem target cannot be truthfully elaborated because the
pinpoint primary source confirms that the received item is a definition of a property, not a
truth-valued proposition with a conclusion.

Stephen Smale's *Differentiable dynamical systems* (1967), section 1.6, item (6.1), printed page
777, defines a compact-manifold diffeomorphism to satisfy Axiom A when its nonwandering set is
hyperbolic and its periodic points are dense in that set. The inspected source PDF has SHA-256
`759e0601e50ceebc812c4a4c67e5b9ed59534848c6d342a2e2cf56871db19551`. The repository record
adds only the title `Axiom A系统` and the gloss `双曲系统的公理` ("axioms for hyperbolic systems"). It
does not assert an equivalence, existence result, consequence, or any other theorem-grade claim.

Formalizing the two clauses as a new predicate would encode the historical definition, but it would
not prove a theorem. Projecting those clauses from assumed structure fields would likewise assume
the intended content rather than close it. Choosing a robustness or structural-stability result
would be an unapproved redirection. Smale's adjacent spectral-decomposition theorem (6.2) is
separately scheduled as `THM-M-1414`; the Anosov and Markov-partition topics are separately
scheduled as `THM-M-1412` and `THM-M-1415`. None may be substituted here.

Consequently there is no canonical human theorem proposition to encode, no exact Lean expression to
hash, and no truthful basis for a minimal-import claim, checked alternate transports, or the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. No
theorem declaration, axiom, placeholder, broadened interface, or convenient consequence was added.
The first failed substantive gate is exact truth-valued source-statement identity, and machine debt
remains `M4`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Geometry.Manifold.Diffeomorph`,
`Mathlib.Geometry.Manifold.MFDeriv.Basic`, `Mathlib.Dynamics.OmegaLimit`, and
`Mathlib.Dynamics.PeriodicPts.Defs`. It re-elaborates `Diffeomorph`, `tangentMap`, `omegaLimit`,
`Function.IsPeriodicPt`, `Function.periodicPts`, and `Dense`. These are generic substrate APIs only.
The probe states no Axiom A proposition, and its four imports are not claimed to be minimal for an
unknown canonical target.

A bounded exact-topic search of pinned `Mathlib/Dynamics` and `Mathlib/Geometry/Manifold` found no
obvious declaration for Axiom A, a nonwandering set, differentiable hyperbolicity, or a stable and
unstable splitting. This is discovery-only feasibility evidence, not the later immutable anchor
audit and not a claim that no differently named or external formalization exists.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`75827f78a8ca003a58af38c8f8f468186ff6cfebb049ab7a5e8eec226a394d39`.

The pre-existing `Formalizations/Lean/.lake` link points to the canonical pinned artifacts and was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1413` | 0 | rank 912, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short && git rev-parse HEAD && git rev-parse HEAD^{tree} && readlink Formalizations/Lean/.lake` | 0 | before statement edits, only the automation-provided untracked `.lake` link was present; base revision and tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1413/IntakeProbe.lean` | 0 | hashes agree with the pinned fingerprint above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1413/IntakeProbe.lean` | 0 | all six generic candidate interfaces elaborated; no canonical target was stated |
| `rg -n -i 'axiom[ _-]?a\|non[- ]?wandering\|nonwandering\|hyperbolic (set\|diffeomorphism\|dynamical)\|hyperbolic.*splitting\|stable.*unstable.*splitting' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold --glob '*.lean'` | 1 | expected no-match exit; discovery-only observation, not an anchor audit |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque\|constant)[[:space:]]' Stage1_Instances/THM-M-1413` | 1 | expected no-match exit; no prohibited proof escape in target Lean source |
| `curl -L --fail --max-time 60 -sS 'https://www.ams.org/journals/bull/1967-73-06/S0002-9904-1967-11798-1/S0002-9904-1967-11798-1.pdf' -H 'User-Agent: Mozilla/5.0' -H 'Referer: https://www.ams.org/' -o /tmp/thm-m-1413-smale1967.pdf -w '%{http_code} %{content_type} %{size_download}\n'` | 22 | HTTP 429; no new source copy was used, and this does not invalidate the intake's recorded immutable locator and inspected-PDF hash |
| `python3 -m json.tool Stage1_Instances/THM-M-1413/statement-blocker.json >/dev/null` | 0 | structured blocker is valid JSON |
| `python3 -c 'import json; from pathlib import Path; d=json.load(open("Stage1_Instances/THM-M-1413/statement-blocker.json")); assert d["item_id"] == "S56-M-1413-STATEMENT" and d["state"] == "[ ]" and d["canonical_statement"] is None and d["canonical_formal_target"] is None and d["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"} and not d["statement_elaborated"] and not d["audit_complete"] and not d["theorem_complete"] and not Path(".stage1-worker-selftest.json").exists(); print("statement blocker invariant check: ok")'` | 0 | item identity, `[ ]` state, null target, `[H5, M4, R4]` boundary, false completion flags, and absent worker self-test agree |
| `python3 Stage1_Instances/THM-M-1413/check_intake.py` | 1 | known phase-evolution failure: the intake-only checker freezes the original nine-file directory set, so it rejects the two later statement-blocker artifacts; the intake receipt was not rewritten to conceal this mismatch |
| `for f in Stage1_Instances/THM-M-1413/statement-blocker.json Stage1_Instances/THM-M-1413/statement-blocker.md; do git diff --no-index --check -- /dev/null "$f"; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done; git diff --check -- Stage1_Instances/THM-M-1413; exit 0` | 0 | no whitespace diagnostics; expected add-file diff status 1 was accepted for each untracked blocker artifact |

## Retry condition and status boundary

First obtain master acceptance of the intake. An accountable reviewer must then approve either a
definition-only target decision or one exact source-backed truth-valued redirection, independently
review the source and errata boundary, and freeze every incorporated definition, domain, universe,
ordered binder, hypothesis, conclusion, and degenerate case. The decision must explain why the
selected claim represents `THM-M-1413` rather than a neighboring target. A later statement worker
can then encode that same claim using real Lean definitions, minimize imports, serialize and hash
the elaborated expression and environment, compile every credited transport, and execute all four
required statement mutations.

The root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. This is blocked-attempt evidence, not completion of the statement node or any
downstream node. Because the phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]`, receipt, proof, or master acceptance
is claimed.
