# THM-M-0861 intake validation

Validation date: 2026-07-13 (Asia/Shanghai). This is nonrelease evidence from an isolated dirty
worker clone at base commit `464759128569180ab640c412cd80bc5dd2c3b44a`, tree
`8da3c9130640d08d4e179450a0418368d0454745`. The initial worktree contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. It was reused read-only; no
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Commands and results

| Command | Exit | Result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, exactly 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0861` | 0 | rank 1415; planned; no legacy slot; legacy artifacts unaccepted; theorem-complete false |
| `git status --short --untracked-files=all` | 0 | initial status contained only `Formalizations/Lean/.lake`; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | recorded base commit and tree above |
| `git blame --line-porcelain -L 6313,6318 Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact source-discovery commands below | 0 | bibliographic identity, 13-page source scan, finite multigraph definitions, Satz C, and proof inspected; PDF SHA-256 `46ad3d33fd7dc835ea0e1d1f12b56302988bff0e2ac898bfa72549d0560bb7eb`; external bytes retained only temporarily and not admitted as H0 evidence |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| exact bounded-search command below | 0 | only the `EdgeLabeling.lean` documentation boundary matched; no exact target found; bounded intake discovery, not exhaustive absence evidence |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0861/IntakeProbe.lean` | 0 | 14 adjacent pinned APIs elaborated, including four multigraph representation APIs; two API axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `a3fb0506e64adb4971306e21de98c0a70461a18c86a6d517c5c3918d956f58d3`; no target declaration or proof body |
| four exact `python3 -m json.tool FILE` invocations below | 0 | structured instance, open DAG, provisional receipt, and packet parse after finalization |
| `python3 -B Stage1_Instances/THM-M-0861/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, pins and hashes, source boundary, H1/M4/R4 null target, exact inventory, packet agreement, probe replay, and six open tasks agree |
| exact fail-on-match `rg` command below | 0 | inner `rg` returned 1 as expected and the wrapper passed; no `sorry`, `admit`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| exact whitespace-check commands below | 0 | no whitespace diagnostics; no-index exit 1 values denote expected new-file differences only |

## Exact discovery and finalization commands

These networked commands were bounded source discovery, not denied-network validation recipes:

```bash
curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1007%2FBF01456961' | jq '.message | {title,author,published,page,volume,issue,DOI,URL,resource,link,reference}'
curl -L --fail --silent --show-error 'https://zenodo.org/api/records/2395248' | jq '{id,doi,metadata,files,links}'
tmp=$(mktemp -d); curl -L --fail --silent --show-error 'https://zenodo.org/api/records/2395248/files/article.pdf/content' -o "$tmp/article.pdf"; sha256sum "$tmp/article.pdf"; pdfinfo "$tmp/article.pdf"; pdftotext -layout "$tmp/article.pdf" "$tmp/article.txt"; rg -n -C 8 'Satz A|Satz B|Satz C|Grades|ungeraden|Faktor|paar|Knoten|Linien|Graph' "$tmp/article.txt"; rm -rf "$tmp"
rg -n -i 'k[öőo]nig.*(edge|line|colour|color)|edge[-_ ]?colou?r|chromatic[-_ ]?index|chromaticIndex|edgeChrom|line chromatic|bipartite.*maxDegree|maxDegree.*bipartite' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

The final local self-test used these exact compound commands in addition to the preflight, Lean,
and checker commands in the table:

```bash
python3 -m json.tool Stage1_Instances/THM-M-0861/instance.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0861/task-dag.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0861/intake-receipt.json >/dev/null && python3 -m json.tool .stage1-worker-selftest.json >/dev/null
if rg -n --glob '*.lean' '\b(sorry|admit|axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0861; then exit 1; else echo 'prohibited Lean construct scan: no matches'; fi
git diff --check
for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0861/README.md Stage1_Instances/THM-M-0861/instance.json Stage1_Instances/THM-M-0861/scope-map.md Stage1_Instances/THM-M-0861/source-statement-crosswalk.md Stage1_Instances/THM-M-0861/task-dag.json Stage1_Instances/THM-M-0861/IntakeProbe.lean Stage1_Instances/THM-M-0861/check_intake.py Stage1_Instances/THM-M-0861/validation.md Stage1_Instances/THM-M-0861/intake-receipt.json; do out=$(git diff --no-index --check /dev/null "$f" 2>&1); rc=$?; test -z "$out" && test "$rc" -eq 1 || { printf '%s\n' "$out"; exit 1; }; done
```

## Source and machine boundary

The source scan materially identifies the intended finite bipartite multigraph theorem and its
proof, but no independent review, accepted translation, equality bridge, corrections audit, or
immutable repository admission exists. The source therefore supports provisional `H1`, not `H0`.
The Lean probe checks only simple-graph substrate and exposes the source/domain mismatch; it does
not elaborate the canonical target and gives no machine-proof credit. Root status is `[H1,M4,R4]`.

## Status boundary

This validation covers only a `planned` intake proposal. The receipt is unsigned, provisional, and
not content-addressed validation authority. All downstream tasks, audit completion, theorem
completion, and master acceptance remain open. The execution DAG gives the dependent `STATEMENT`
node responsibility for exact Lean elaboration. Consequently the planned intake freezes the
source-backed theorem family and all proposition-changing decisions as blockers, while leaving the
section-5 canonical statement/expression/fingerprint fields null instead of fabricating a target.
