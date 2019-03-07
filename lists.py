## Import python modules
import ROOT

DATA_BRANCHES = [
  "CCInclusiveReco_E",
  "CCInclusiveReco_Q2",
  "CCInclusiveReco_leptonE",
  "CCInclusiveReco_nu_energy_recoil",
  "pass_canonical_cut",
  "CCInclusiveReco_vtx",
  "phys_n_dead_discr_pair_upstream_prim_track_proj",
  "CCInclusiveReco_minos_trk_qp",
  "CCInclusiveReco_minos_trk_p",
  "CCInclusiveReco_minos_trk_eqp_qp",
  "CCInclusiveReco_minos_trk_end_x",
  "CCInclusiveReco_minos_trk_end_y",
  "CCInclusiveReco_minos_trk_end_z",
  "CCInclusiveReco_minos_trk_vtx_x",
  "CCInclusiveReco_minos_trk_vtx_y",
  "CCInclusiveReco_minos_trk_vtx_z",
  "CCInclusiveReco_minos_trk_end_plane",
  "CCInclusiveReco_r_minos_trk_vtx_dcosx",
  "CCInclusiveReco_r_minos_trk_vtx_dcosy",
  "CCInclusiveReco_r_minos_trk_vtx_dcosz",
  "CCInclusiveReco_minos_trk_p_range",
  "CCInclusiveReco_minos_trk_p_curvature",
  "CCInclusiveReco_minos_used_range",
  "CCInclusiveReco_minos_used_curvature",
  "E_corr_tracker_lu",
  "E_corr_ecal_lu",
  "E_corr_hcal_lu",
  "primary_track_minerva_theta",
  "primary_track_minerva_phi",
  "primary_track_minerva_start_position",
  "primary_track_minerva_end_position",
  "muon_length_tracker",
  "muon_length_ecal",
  "muon_length_hcal",
  "plane_visible_energy",
  "plane_visible_energy_sz",
  "n_recoil_clus_id",
  "recoil_clus_id_energy",
  "recoil_clus_id_module",
  "recoil_clus_id_plane",
  "recoil_clus_id_strip",
  "recoil_clus_id_view",
  "recoil_clus_id_type",
  "recoil_clus_id_time",
  "n_recoil_clus_od",
  "recoil_clus_od_energy",
  "recoil_clus_od_frame",
  "recoil_clus_od_tower",
  "recoil_clus_od_story",
  "recoil_clus_od_time",
]

MC_BRANCHES = [
  "mc_vtx",
  "mc_current",
  "mc_targetNucleon",
  "mc_intType",
  "mc_targetZ",
  "mc_targetA",
  "mc_w",
  "mc_nFSPart",
  "mc_FSPartPDG",
  "mc_FSPartE",
  "mc_incoming",
  "mc_incomingE",
  "mc_primFSLepton",
  "mc_incomingPartVec",
  "mc_Bjorkenx",
  "mc_Bjorkeny",
  "mc_Q2",
  "wgt",
  "truth_pass_CCInclusiveReco",
  "truth_pass_fiducial",
  "truth_pass_Canonical",
  "truth_genie_wgt_Rvn1pi",
  "truth_genie_wgt_Rvp1pi",
  "pass_canonical_cut",
  "phys_n_dead_discr_pair_upstream_prim_track_proj",
  "E_corr_ecal_lu",
  "E_corr_hcal_lu",
  "E_corr_tracker_lu",
  "muon_length_ecal",
  "muon_length_hcal",
  "muon_length_tracker",
  "primary_track_minerva_phi",
  "primary_track_minerva_theta",
  "n_recoil_clus_id",
  "recoil_clus_id_module",
  "recoil_clus_id_plane",
  "recoil_clus_id_type",
  "recoil_clus_id_view",
  "n_recoil_clus_od",
  "recoil_clus_od_frame",
  "recoil_clus_od_story",
  "recoil_clus_od_tower",
  "plane_visible_energy_sz",
  "plane_visible_energy",
  "primary_track_minerva_end_position",
  "primary_track_minerva_start_position",
  "recoil_clus_id_energy",
  "recoil_clus_id_strip",
  "recoil_clus_id_time",
  "recoil_clus_od_energy",
  "recoil_clus_od_time",
  "CCInclusiveReco_E",
  "CCInclusiveReco_leptonE",
  "CCInclusiveReco_vtx",
  "CCInclusiveReco_minos_used_range",
  "CCInclusiveReco_minos_used_curvature",
  "CCInclusiveReco_minos_trk_end_plane",
  "CCInclusiveReco_minos_trk_end_x",
  "CCInclusiveReco_minos_trk_end_y",
  "CCInclusiveReco_minos_trk_end_z",
  "CCInclusiveReco_minos_trk_eqp_qp",
  "CCInclusiveReco_minos_trk_p",
  "CCInclusiveReco_minos_trk_p_curvature",
  "CCInclusiveReco_minos_trk_p_range",
  "CCInclusiveReco_minos_trk_qp",
  "CCInclusiveReco_minos_trk_vtx_x",
  "CCInclusiveReco_minos_trk_vtx_y",
  "CCInclusiveReco_minos_trk_vtx_z",
  "CCInclusiveReco_nu_energy_recoil",
  "CCInclusiveReco_r_minos_trk_vtx_dcosx",
  "CCInclusiveReco_r_minos_trk_vtx_dcosy",
  "CCInclusiveReco_r_minos_trk_vtx_dcosz"
]

TRUTH_BRANCHES = [
  "truth_pass_CCInclusiveReco",
  "truth_pass_fiducial",
  "truth_pass_Canonical",
  "truth_genie_wgt_Rvn1pi",
  "truth_genie_wgt_Rvp1pi",
  "genie_wgt_n_shifts",
  "mc_intType",
  "mc_current",
  "mc_incoming",
  "mc_targetZ",
  "mc_targetA",
  "mc_incomingE",
  "mc_Bjorkenx",
  "mc_Bjorkeny",
  "mc_Q2",
  "mc_w",
  "mc_vtx",
  "mc_primFSLepton",
  "mc_incomingPartVec",
  "mc_nFSPart",
  "mc_FSPartE",
  "mc_FSPartPDG",
  "wgt"
]

PLAYLIST_COLORS = {
  # colors taken from Phil's 'plot.h' implementation, explained in DocDB entry #12618
  "minerva13C": "#e41a1c",
  "minervame1A": "#377eb8",
  "minervame1F": "#4daf4a",
  "minervame1L": "#984ea3"
}
