import Mathlib.Topology.UniformSpace.Dini

/-!
# THM-M-0292 discovery-only intake probe

These checks authenticate the pinned Dini interfaces and their classical real-valued sequence
specializations. This file does not choose a canonical source variant, declare the target theorem,
or add a proof body for THM-M-0292.
-/

open Filter Topology

#check Monotone.tendstoLocallyUniformly_of_forall_tendsto
#check Monotone.tendstoUniformly_of_forall_tendsto
#check Monotone.tendstoUniformlyOn_of_forall_tendsto
#check Antitone.tendstoLocallyUniformly_of_forall_tendsto
#check Antitone.tendstoUniformly_of_forall_tendsto
#check Antitone.tendstoUniformlyOn_of_forall_tendsto
#check ContinuousMap.tendsto_of_monotone_of_pointwise
#check ContinuousMap.tendsto_of_antitone_of_pointwise

-- Specialize the compact-set interfaces without selecting either one as the source-mapped root.
example {α : Type*} [TopologicalSpace α] {F : ℕ → α → ℝ} {f : α → ℝ} {s : Set α}
    (hs : IsCompact s) (hF_cont : ∀ i, ContinuousOn (F i) s)
    (hF_mono : ∀ x ∈ s, Monotone (F · x)) (hf : ContinuousOn f s)
    (h_tendsto : ∀ x ∈ s, Tendsto (F · x) atTop (𝓝 (f x))) :
    TendstoUniformlyOn F f atTop s :=
  Monotone.tendstoUniformlyOn_of_forall_tendsto hs hF_cont hF_mono hf h_tendsto

example {α : Type*} [TopologicalSpace α] {F : ℕ → α → ℝ} {f : α → ℝ} {s : Set α}
    (hs : IsCompact s) (hF_cont : ∀ i, ContinuousOn (F i) s)
    (hF_anti : ∀ x ∈ s, Antitone (F · x)) (hf : ContinuousOn f s)
    (h_tendsto : ∀ x ∈ s, Tendsto (F · x) atTop (𝓝 (f x))) :
    TendstoUniformlyOn F f atTop s :=
  Antitone.tendstoUniformlyOn_of_forall_tendsto hs hF_cont hF_anti hf h_tendsto
