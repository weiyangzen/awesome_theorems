# Statement validation record

Base revision: `2c6761e363b5a57450403b79966a76702e940c3b`.

The canonical declaration is `Stage1Instances.THM_M_1010.Target` in `Statement.lean`. It quantifies
over a Polish Borel space and probability measures, uses convergence in the pinned topology on
`ProbabilityMeasure`, and asks for representatives on one probability space whose laws are the
given measures and which converge almost surely. `target_iff_expanded` kernel-checks the named
target against its explicit binder form. The three imports are minimal by responsibility: `HasLaw`
provides marginal-law statements, `LevyProkhorovMetric` provides the weak topology on probability
measures, and `Polish.Basic` provides `PolishSpace`; removing each corresponding import made its
required identifier unavailable in isolated probes.

## Commands and results

All Lean commands ran from `Formalizations/Lean` and reused the existing pinned `.lake` artifacts.
No dependency operation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-1010/Statement.olean ../../Stage1_Instances/THM-M-1010/Statement.lean` | 0 | canonical target and checked expansion elaborate; transient object enables the import-based probes and is removed afterward |
| `LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-1010/PrintTarget.lean` | 0 | prints the explicit universe, topology, measurable, Borel, Polish, measure-sequence, limit-measure, weak-convergence, and representation binders |
| `LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-1010/mutations/RemovedHypothesis.lean` | 1 expected | `failed to synthesize ... BorelSpace S` |
| `LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-1010/mutations/ChangedDomain.lean` | 1 expected | `Iff.rfl` type mismatch between the all-Polish-spaces and Real-only targets |
| `LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-1010/mutations/ChangedBinderScope.lean` | 1 expected | `Iff.rfl` type mismatch after moving the limit law outside its original universal scope |
| `LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-1010/mutations/ExcludedBoundary.lean` | 1 expected | `Iff.rfl` type mismatch after excluding constant sequences with a disequality premise |
| `sha256sum Stage1_Instances/THM-M-1010/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded in `statement.json` |

The elaborated-expression hash in `statement.json` is SHA-256 of the exact stdout emitted by
`PrintTarget.lean` with its final newline. This is provisional worker evidence, not a node-specific
master receipt. The anchor audit, obligation tree, proof, validation, release, and theorem completion
remain open.
