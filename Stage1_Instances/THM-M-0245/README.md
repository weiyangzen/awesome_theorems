# THM-M-0245 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `法图定理`
(Fatou's theorem). The catalog gives only the gloss `单位圆盘内全纯函数的径向极限`
("radial limits of holomorphic functions in the unit disk"), attributes it to Pierre Fatou in
1906, and marks it `已验证`. Under rev-5.6 that status is untrusted metadata, not source or proof
credit.

The gloss does not yet determine a true proposition. Holomorphicity on the open unit disk alone is
not the classical size hypothesis normally paired with an almost-everywhere boundary-limit
theorem. A source-selected version must decide bounded analytic versus a particular Hardy or other
function class, radial versus nontangential approach, ordinary versus normalized boundary measure,
finite complex versus extended limits, and the exact almost-everywhere conclusion. Adding one of
those choices from memory would broaden or substitute the repository wording.

The likely 1906 primary paper was identified bibliographically, but its theorem text was not
accessible during this intake and no pinpoint definition, assumption, theorem, proof, correction,
or erratum was reviewed. The canonical human statement and Lean target therefore remain null. The
provisional root vector is `[H1, M4, R4]`: a matching published source lead exists, no exact usable
formal artifact is credited, and no source-faithful reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the open decisions and non-substitution boundary, while
`task-dag.json` keeps all six downstream phases open. `IntakeProbe.lean` checks only adjacent
pinned APIs and states no target theorem. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
