# Anchor-audit validation record

Base revision: `f756a5a3b3e172050802423f4b98d5910b56dbb5`.

| Command | Exit | Exact result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1245/AnchorAudit.lean` | 0 | Printed four candidate types; the full Euclidean scalar specialization elaborated; both axiom probes reported `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool Stage1_Instances/THM-M-1245/anchor-audit.json` | 0 | audit JSON parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1245` | 0 | rank 326, `L0/rework_required`, lifecycle `planned`, theorem incomplete |
| `test "$(git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD)" = 8a178386ffc0f5fef0b77738bb5449d50efeea95` | 0 | checked the dependency worktree is at the manifest revision |
| `! rg -n '\bsorry\b\|\badmit\b\|^\s*axiom\b\|\bunsafe\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean` | 0 | no prohibited placeholder or unsafe marker in the terminal candidate module |
| `git diff --check -- Stage1_Instances/THM-M-1245` | 0 | no whitespace errors |

External discovery queried GitHub repository search for `Sobolev inequality Lean4`,
`Gagliardo Nirenberg Sobolev Lean`, `Sobolev language:Lean`, and `Gagliardo language:Lean` on
2026-07-12. Immutable tar archives of `grunweg/SobolevSlobodeckij` at
`88d0535ecf0d2c31dd7f53674919da0aa7c40c7b` and `abenenson/rellich-kondrachov` at
`70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23` were inspected in `/tmp` and deleted. The former
delegates the still-planned embedding to mathlib and contains `sorry`; the latter proves a
different compact-embedding theorem and had no placeholder hits. No dependency was installed or
fetched into `.lake`.

Artifact SHA-256 values:

- `AnchorAudit.lean`: `cd0f09561941d7ceeba7d24bcd3c1e3a2d6e23ab0470ec2438a9dcef9666e5da`
- `anchor-audit.json`: `5837333f3a56b9989e69c8cc2207779b1e8f2c4f94b5cc313bdcdb32106bff2f`
- `anchor-audit.md`: `36ffe7952314e48a73ce7905288c2762bdfaf4054aab3327f22093096bb6107d`

Known failures are downstream rather than hidden: this node does not create the named root proof,
pin a new external dependency, establish H0 or R0, perform hermetic replay, or independently verify
a release. GitHub's core API rate limit also prevented immutable revision retrieval for the
clearly non-equivalent Fourier-torus discovery result.
