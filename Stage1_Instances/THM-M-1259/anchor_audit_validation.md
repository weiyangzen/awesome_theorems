# Anchor-audit validation record

Base revision: `4d48a3c5fbec6d005a64a99338e40c001656264c`.

| Command | Exit | Exact result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1259/AnchorAudit.lean` | 0 | Printed types for `VectorField.lieBracket`, `ContDiff.lieBracket_vectorField`, `Distribution`, `MeasureTheory.eLpNorm`, and `MeasureTheory.eLpNorm_le_eLpNorm_fderiv`; no diagnostics |
| `python3 -m json.tool Stage1_Instances/THM-M-1259/anchor_audit.json` | 0 | Parsed and pretty-printed the complete audit JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | rank 161, lifecycle `planned`, theorem incomplete |
| pinned-package negative search (below) | 0 | no matching Lean source in the complete pinned package tree |
| repository candidate-set assertion (below) | 0 | exactly the legacy module, `Statement.lean`, and this audit check matched |
| `git diff --check -- Stage1_Instances/THM-M-1259` | 0 | no whitespace errors |

Pinned-package negative search:

```bash
test -z "$(rg -l -i 'h[oö]rmander|hormander|hypoellipt|subellipt' \
  Formalizations/Lean/.lake/packages --glob '*.lean')"
```

Repository candidate-set assertion:

```bash
test "$(rg -l -i 'h[oö]rmander|hormander|hypoellipt|subellipt' --glob '*.lean' . \
  | sort | tr '\n' ' ')" = \
  './Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_161.lean ./Stage1_Instances/THM-M-1259/AnchorAudit.lean ./Stage1_Instances/THM-M-1259/Statement.lean '
```

Artifact SHA-256 values:

- `AnchorAudit.lean`: `5a8b87930b9d7c44c1baebe9f6307de93ad3afb03dacf555f98add49aad0ba0d`
- `anchor_audit.json`: `ac668a1aee1297b698c01d328b809eff8094acac21a955763e6ac5ab92a9434d`

External discovery used GitHub's REST repository-search endpoint and returned zero repositories for
each query recorded in `anchor_audit.json`. The attempted secondary grep.app searches returned HTTP
429. No network result is proof evidence and no dependency was fetched; these results only delimit
the candidate audit. The successful Lean run validates names and types of supporting anchors, not
the frozen root theorem.

