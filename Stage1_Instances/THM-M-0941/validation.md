# THM-M-0941 intake validation

## Validation boundary

This is nonrelease worker evidence for a `planned` intake only. The worker clone began at revision
`fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`) with the automation-provided untracked
`Formalizations/Lean/.lake` link. That pinned link was read but not changed. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation was run.

The source-discovery download and web metadata queries were bounded discovery, not hermetic
validation recipes. The PDF remained temporary and is identified by its observed hash; it is not
an accepted durable H0 source. The two structured recipes in `intake-receipt.json` are local and
deny network use.

## Commands and observed results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` for 15 assurance groups, 41 legacy rows, 300 legacy slots, and exactly 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0941` | 0 | rank 1480, planned, no legacy slot, theorem complete false |
| `git status --short` | 0 | initial status contained only `?? Formalizations/Lean/.lake`; preserved |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision/tree recorded above |
| `lake env lean --version` in `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `lake env lean ../../Stage1_Instances/THM-M-0941/IntakeProbe.lean` in `Formalizations/Lean` | 0 | eleven adjacent APIs elaborated, including very-small-doubling structural special cases; selected axiom reports recorded; final output hash bound in the receipt; no target or proof body |
| bounded `rg` search recorded below | 0 | adjacent Freiman-map, small-doubling, Plunnecke-Ruzsa, and very-small-doubling material found; no generalized/coset progression or exact full structural theorem declaration found |
| `python3 -B Stage1_Instances/THM-M-0941/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | final manifest, source/hash, null-target, H1/M4/R4, open-DAG, receipt, packet, and pinned-probe invariants passed |
| prohibited-construct and whitespace commands below | 0 | no prohibited Lean declaration and no whitespace diagnostics |

Per-action start/end times, observed exits, input-manifest digests, output/log hashes, task coverage,
empty obligation coverage, and declaration coverage are bound in the `validation_actions` array of
`intake-receipt.json`. The structure action emitted a 74-byte line with SHA-256
`0d18973324027571e835da29b8dd227d824d19f12b501d063287a75148b395f2`; the Lean action emitted
2862 bytes with the hash bound in the receipt.

The intake has no canonical obligation registry, so the normative `covered_obligation_ids` field is
truthfully empty. `covered_task_ids` separately records that both recipes validate the assigned
intake task; it must not be interpreted as obligation or theorem-proof coverage. The two shell
checks in `commands_and_results` are explicitly supporting hygiene commands, not normative
structured replay recipes.

## Discovery commands

These networked commands were source discovery only:

```bash
curl -L --fail --silent --show-error https://arxiv.org/pdf/math/0505198 -o /tmp/green-ruzsa-freiman.pdf
sha256sum /tmp/green-ruzsa-freiman.pdf
pdfinfo /tmp/green-ruzsa-freiman.pdf
pdftotext -layout /tmp/green-ruzsa-freiman.pdf /tmp/green-ruzsa-freiman.txt
rg -n 'Freiman|Theorem 1\.1|progression|References|\[6\]' /tmp/green-ruzsa-freiman.txt
curl -L --fail --silent --show-error https://export.arxiv.org/api/query?id_list=math/0505198
curl -L --fail --silent --show-error 'https://api.crossref.org/works?query.title=Foundations%20of%20a%20structural%20theory%20of%20set%20addition&rows=10'
```

The bounded repo/pinned-library search was:

```bash
rg -n -i 'Freiman|small doubling|doubling constant|generalized arithmetic|generalised arithmetic|coset progression|Plünnecke|Pluennecke' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

This is an intake search boundary, not the later immutable discovery protocol or a global absence
claim.

## Final local checks

```bash
python3 -m json.tool Stage1_Instances/THM-M-0941/instance.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0941/task-dag.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0941/intake-receipt.json >/dev/null
python3 -m json.tool .stage1-worker-selftest.json >/dev/null
python3 -B Stage1_Instances/THM-M-0941/check_intake.py --worker-packet .stage1-worker-selftest.json
if rg -n --glob '*.lean' '\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0941; then exit 1; else echo 'prohibited Lean construct scan: no matches'; fi
git diff --check
for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0941/*; do test -f "$f" || continue; out=$(git diff --no-index --check /dev/null "$f" 2>&1); rc=$?; test -z "$out" && test "$rc" -eq 1 || { printf '%s\n' "$out"; exit 1; }; done
```

## Result

The source lead confirms a real theorem family but exposes unresolved classical-integer versus
arbitrary-group variants; it does not close H0. The Lean probe authenticates adjacent substrate but
does not elaborate the root; it gives no machine-proof credit. Root status is `[H1, M4, R4]`.

The dossier is a worker-self-tested planned intake proposal. Its provisional receipt is unsigned,
non-content-addressed, and not master-accepted. Exact statement, all downstream tasks, audit
completion, and theorem completion remain open.
