# THM-M-1422 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Young塔`
(`Young tower`). The catalog attributes it to Lai-Sang Young in 1998 and describes it only as
`非一致双曲系统的工具` (`a tool for nonuniformly hyperbolic systems`). That wording names a
construction and its use, not a truth-valued proposition with ordered binders, hypotheses, and a
conclusion. The catalog status `已验证` is untrusted metadata under rev-5.6.

Young's 1998 paper *Statistical Properties of Dynamical Systems with Some Hyperbolicity* is a
strong primary-source candidate. It defines a Markov extension over a variable return-time map and
then states several different results: existence of an SRB measure, exponential decay of
correlations, and a central limit theorem. Selecting any one of them, or merely asserting the
existence or correctness of the tower construction, would add mathematics that the catalog does not
choose.

This intake therefore freezes the ambiguity rather than substituting a familiar result. The
provisional root vector is `[H5, M4, R4]`. `H5` classifies the received catalog target as not yet a
stable proposition; it does not refute Young's construction or the published theorems that use it.
No exact Lean target, proof body, or readable proof reconstruction can attach to the unidentified
root.

The structured authority is `instance.json`. `scope-map.md` records the permitted scope and
prohibited substitutions, while `source-statement-crosswalk.md` maps the catalog wording to the
primary-source and Lean decisions still required. All six downstream phases remain open in
`task-dag.json`. `IntakeProbe.lean` checks only adjacent pinned Lean APIs and states no target
theorem. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
