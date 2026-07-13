# Intake validation

Base revision: `b99cf0ffec59c781f8bd25309bdfa53e77372a0a` (tree
`e015394246c3919236f2c6ba1a8184c37130f1e4`).

Validation date: `2026-07-13` (`Asia/Shanghai`). This validation covers target membership, dossier
structure and fail-closed intake invariants, JSON integrity, and a narrow pinned Lean API probe. The
canonical `.lake` artifacts were reused read-only; no update, build, clone, or fetch was run. The
pre-existing untracked `Formalizations/Lean/.lake` link is outside this target and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0090` | exit 0; rank 1107, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short` before editing | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` path existed |
| `git blame -L 663,668 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error -A 'Mozilla/5.0' -o /tmp/mit-ocw.pdf 'https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf' && sha256sum /tmp/mit-ocw.pdf && pdfinfo /tmp/mit-ocw.pdf && pdftotext -layout /tmp/mit-ocw.pdf /tmp/mit-ocw.txt && rg -n -i -C 10 -e 'Weyl character formula' -e 'character formula' /tmp/mit-ocw.txt` | exit 0; Section 26 definitions on pp. 138-140, Theorem 26.4 on p. 140, and its proof on pp. 140-141 located; PDF digest `9604129911b24dc6602a263e066992df378bded27a5b30a93467ad4f2ef5b8d4`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean 4.29.0 commit `98dc76e3`; Lake 5.0.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `rg -n -i --glob '*.lean' -e 'Weyl.?character' -e 'character.?formula' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 0; no exact target declaration found; repo-local hits were different Kac-Peterson/Kazhdan-Lusztig formulas and mathlib had no target hit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0090/IntakeProbe.lean)` | exit 0; nine adjacent character, weight, root-system, and Weyl-group APIs elaborated; stdout SHA-256 `908889696cb550ba89898ce037db12b2fc5dbf96f9696b224b5206b1c9fab709`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0090-pycache python3 -m py_compile Stage1_Instances/THM-M-0090/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0090/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source and dependency pins, artifact hashes, provisional receipt and worker packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-0090 --glob '*.lean'; test $? -eq 1` | exit 0; the search returned its expected no-match status; no prohibited Lean construct found |
| `git diff --check -- Stage1_Instances/THM-M-0090 .stage1-worker-selftest.json && for f in Stage1_Instances/THM-M-0090/* .stage1-worker-selftest.json; do git diff --no-index --check /dev/null "$f" >/dev/null \|\| test $? -eq 1 \|\| exit $?; done` | exit 0; no whitespace errors; no-index exit 1 per untracked file was the expected new-file difference |

## Known open gates

An accepted immutable source edition and exact proposition, the group or Lie-algebra domain,
representation and highest-weight hypotheses, root data, character and denominator encoding,
ordered binders, boundary cases, corrections audit, and independent source review remain open. So
do the canonical Lean expression and environment fingerprints, checked transports, statement
mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof
and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
