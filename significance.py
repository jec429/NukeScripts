import ROOT
from nukeFunctions import *
from array import array
import time,math,random

def pass_neutron_cuts(e):
   if oneNeutron and e.neutron3d_N != 1: return False
   if moreOneNeutron and e.neutron3d_N == 0: return False
   if moreOneNeutron and e.neutron3d_N > 3: return False
   return True

def pass_test_cut(val, cut):
    if val > cut:
        return True
    else:
        return False

oneNeutron = 0
moreOneNeutron = 1

short_run = 1
playlist = '6A'

def main():
    xs = [ array( 'd' ) for x in range(7) ]
    ns = [ array( 'd' ) for x in range(7) ]
    ds = [ array( 'd' ) for x in range(7) ]
    rs = [ array( 'd' ) for x in range(7) ]

    n_cutv = 10
    for x,n,d in zip(xs,ns,ds):
        for i in range(n_cutv+1):
            x.append(float(i)*3.15/float(n_cutv))
            n.append(0)
            d.append(0)
    
    if short_run: print "Short Run"
    else: print "Full Run"

    t_mc_0 = ROOT.TChain("NukeCCQETwoTrack")
    t_mc_0.Add("/minerva/data/users/jchaves/googoo/pruned_6A_NukeCCQETwoTrack_mc_AnaTuple_run00126*_Playlist.root")
    
    print 'Entries MC=',t_mc_0.GetEntries()
    pass_entries = 0

    entry = 0
    nentries = t_mc_0.GetEntries()
    timeNow = time.time()

    for e in t_mc_0:
        if entry%10000 == 0:
            print "%d/%d"%(entry,nentries)
            #print time.time() - timeNow 
            timeNow = time.time()

        entry += 1
        if entry > 10000 and short_run: break

        if not pass_cuts(e): continue
        if not pass_neutron_cuts(e): continue
        
        pass_entries += 1
            
        single_sample = e.SingleTrackSample

        muon_theta = e.NukeCCQETwoTrack_muon_theta
        muon_p     = e.NukeCCQETwoTrack_muon_p
      
        muon_pt_beam = math.sin(muon_theta)*muon_p;
        muon_pz_beam = math.cos(muon_theta)*muon_p;

        #print muon_pt_beam,muon_pz_beam
            
        target = -1
        if target1_cut(e.vtx[2]): target = 0
        elif target2_cut(e.vtx[2]): target = 1
        elif target3_cut(e.vtx[2]): target = 2
        elif target4_cut(e.vtx[2]): target = 3
        elif target5_cut(e.vtx[2]): target = 4
        elif targetW_cut(e.vtx[2]): target = 6
        else: continue
    
        for i,c in enumerate(xs[target]):
            val = random.uniform(0,3.15) # ANGLE here
            signal = True
            for can in e.neutron3d_ancestor:
                if can != 2112:
                    signal = False                
            if pass_test_cut(val,c):
                if signal:
                    ns[target][i] += 1
                else:
                    ds[target][i] += 1

    for i in range(7):
        for n,d in zip(ns[i],ds[i]):
            if d > 0:
                rs[i].append(n/math.sqrt(d))
            else:
                rs[i].append(0.0)
                
    print xs[1],ds[1],ns[1],rs[1]

    for i in range(7):
        can = ROOT.TCanvas('can')
        gr = ROOT.TGraph( len(xs[i]), xs[i], rs[i] )
        gr.SetLineColor( 2 )
        gr.SetLineWidth( 4 )
        gr.SetMarkerColor( 4 )
        gr.SetMarkerStyle( 21 )
        gr.SetTitle( 'a simple graph' )
        gr.GetXaxis().SetTitle( 'Angle' )
        gr.GetYaxis().SetTitle( 'Significance' )
        gr.Draw( 'ACP' )
        can.Print('significance_'+str(i)+'.pdf')
        can.Print('significance_'+str(i)+'.C')
    
if __name__ == "__main__":
   main()
