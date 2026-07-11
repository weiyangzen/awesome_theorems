# Statement validation record

Item: `S56-M-0402-STATEMENT`  
Base revision: `526ce9084300c50dce820f559d879c3e6b579060`

## Frozen target

The canonical declaration is
`Stage1Instances.THMM0402.EvertseSUnitStatement`. It specializes Theorem 1
of Evertse (1984), pages 226-227, to `(c,d)=(1,0)`. Its coordinates are
mathlib S-units over a number field, its total sum vanishes, and every
nonempty proper subsum is nonzero. Setting coordinate zero to one chooses a
unique representative of each relevant projective point.

The sole direct import is
`Mathlib.RingTheory.DedekindDomain.SInteger`; its transitive pinned interface
provides the number-field, ring-of-integers, and mathlib S-unit surfaces. The legacy
class-group, factorization, and Dirichlet-theorem imports are unnecessary for
statement elaboration.

## Commands and results

All commands ran in this worker clone. The Lean command ran from
`Formalizations/Lean` and reused the pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0402/Statement.lean` | 0 | canonical declaration, membership unfolding, and exact-type fixture elaborated; `#print` emitted the fully explicit target |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository assurance structure passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0402` | 0 | rank 15, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0402/instance.json Stage1_Instances/THM-M-0402/statement.json` | 0 | both structured artifacts are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0402 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

The two-variable equation `x+y=1` is only the `n=2` projective specialization,
not the frozen root. Removing positivity admits a zero-dimensional boundary;
removing the proper-subsum condition admits degenerate infinite families;
removing support finiteness changes Evertse's hypothesis. No such mutation is
credited. This receipt establishes statement elaboration only and does not
advance theorem completion.
