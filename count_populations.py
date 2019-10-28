#Bruno Iochins Grisci and Marcelo D. Poleto
#APRIL/2019
#http://sbcb.inf.ufrgs.br/confid
# -*- coding:utf-8 -*-

import os
import sys
import pprint
import numpy as np
import operator
from collections import Counter
try:
    from itertools import imap
except ImportError:
    #print("WARNING: Could not import imap from itertools, if using Python 3.x ignore this warning.")
    imap=map

from populations import pops

################################################################
################################################################

class region:
    def __init__(self, reg, peak, points_file):
        self.reg   = reg
        self.peak  = peak
        self.points_file = points_file
        self.points = []
    def get_count(self):
        return len(self.points)
    def get_freq(self):
        total_points = 0.0
        with open(self.points_file, 'r') as pf:
            for line in pf:
                if '#' in line or '@' in line:
                    pass
                else:
                    total_points += 1.0
        return float(len(self.points)/total_points)
    def get_mean(self):
        m = np.mean(np.array(self.points))
        if m > 180.0:
            m = m - 360.0
        elif m < -180.0:
            m = m + 360.0
        return m
    def get_std(self):
        return np.std(np.array(self.points))
    def get_median(self):
        med = np.median(np.array(self.points))
        if med > 180.0:
            med = med - 360.0
        elif med < -180.0:
            med = med + 360.0
        return med
    def __repr__(self):
        return '{:24s} # count: {:6d} # freq: {:6.3f} # peak: {:4d} # mean: {:8.3f} # std: {:6.3f} # median: {:8.3f}'.format(str(self.reg), self.get_count(), self.get_freq(), self.peak, self.get_mean(), self.get_std(), self.get_median())

################################################################
################################################################

def show_graph(nodes, edges, first_node, last_node, cutoff, filename, plot_graph, POP_ID=None):

    sorted_nodes = sorted(nodes.items(), key=operator.itemgetter(1), reverse=True)
    sorted_edges = sorted(edges.items(), key=operator.itemgetter(1), reverse=True)

    total_weight = 0.0
    for edge in sorted_edges:
        total_weight += edge[1]

    total_size = 0.0
    for node, size in sorted_nodes:
        total_size += size

    max_size = sorted_nodes[0][1]
    if len(sorted_edges) > 0:
        max_weight = sorted_edges[0][1]
    else:
        max_weight = 0.0

    node_key_len = max([len(str(l)) for l in nodes])
    if len(edges) > 0:
        edge_key_len = max([len(str(l)) for l in edges])
    else:
        edge_key_len = 0

    with open(filename, 'w') as f:
        f.write('# NODES\n\n')
        f.write('Start node: {}\nEnd node:   {}\n\n'.format(first_node, last_node))
        for n, s in sorted_nodes:
            f.write('{:{l}s}: {:9.1f}\n'.format(str(n), s, l=node_key_len))

        f.write('\n# EDGES\n\n')
        for e, w in sorted_edges:
            f.write('{:{l}s}: {:9.1f}\n'.format(str(e), w, l=edge_key_len))

    if POP_ID != None:
        with open(filename.replace('txt', 'gml'), 'w') as gml:
            gml.write('Creator "ConfID"\ngraph\n[\n  directed 1\n')
            for n, v in sorted_nodes:
                line = '  node\n  [\n    id {}\n    label "{}"\n    value {}\n  ]\n'.format(POP_ID[n], 'P#{}'.format(POP_ID[n]), v/total_size)
                gml.write(line)
            for e, w in sorted_edges:
                line = '  edge\n  [\n    source {}\n    target {}\n    value {}\n    label "{}"\n  ]\n'.format(POP_ID[e[0]], POP_ID[e[1]], w/total_weight, w/total_weight)
                gml.write(line)
            gml.write(']')
    else:
        with open(filename.replace('txt', 'gml'), 'w') as gml:
            sn = [n[0] for n in sorted_nodes]
            gml.write('Creator "ConfID"\ngraph\n[\n  directed 1\n')
            for n, v in sorted_nodes:
                line = '  node\n  [\n    id {}\n    label "{}"\n    value {}\n  ]\n'.format(sn.index(n)+1, n, v/total_size)
                gml.write(line)
            for e, w in sorted_edges:
                line = '  edge\n  [\n    source {}\n    target {}\n    value {}\n    label "{}"\n  ]\n'.format(sn.index(e[0])+1, sn.index(e[1])+1, w/total_weight, w/total_weight)
                gml.write(line)
            gml.write(']')

    if plot_graph:

        if len(nodes) > 200:
            print('WARNING: Did not plot network with more than 200 nodes.')
            return None

        import graphviz

        dot = graphviz.Digraph()
        dot.format = 'eps'
        dot.attr('node', shape='circle')
        dot.attr('node', fixedsize='true')
        dot.attr('node', labelfontsize='10')
        dot.attr('node', style='filled')

        show = set()
        for n1, n2 in edges.keys():
            w = edges[(n1,n2)]/total_weight
            if w >= cutoff:
                dot.edge(str(n1), str(n2), label=str(round(w, 3)), constraint='true', fixedsize='true', penwidth=str(w*10), weight=str(1.0/w), labelfontsize='7')
                show.add(n1)
                show.add(n2)

        s = 'circle'
        c = 'gray'
        if POP_ID != None:
            rank = 1
            for node, v in sorted_nodes:
                if node == first_node:
                    c = 'green'
                if node == last_node:
                    s = 'doublecircle'
                if node in show or (node == first_node or node == last_node):
                    dot.node(str(node), 'P#'+str(rank), width=str(nodes[node]/max_size*2), height=str(nodes[node]/max_size*2), color=c, shape=s, labelfontsize='7')
                s = 'circle'
                c = 'gray'
                rank += 1
        else:
            for node, v in sorted_nodes:
                if node == first_node:
                    c = 'green'
                if node == last_node:
                    s = 'doublecircle'
                if node in show or (node == first_node or node == last_node):
                    dot.node(str(node), str(node), width=str(nodes[node]/max_size*2), height=str(nodes[node]/max_size*2), color=c, shape=s, labelfontsize='7')
                s = 'circle'
                c = 'gray'
        try:
            dot.render(filename.replace('.txt', ''), view=False)
        except Exception as e: 
            print('ERROR while rendering networks')
            print(e)

################################################################
################################################################

def main(input_files, output_folder, xvgs_folder, time_folder, graphs_folder, show_z, cutoff, plot_graph, convergence_cutoff, fp, fv):

    alias = output_folder + os.path.basename(input_files).replace('.inp', '')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(xvgs_folder):
        os.makedirs(xvgs_folder)
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)
    if not os.path.exists(time_folder):
        os.makedirs(time_folder)


    DATA       = {}
    peaksXtime = {}
    ANGLES     = []
    TIMES      = []
    reading_order = []

    with open(input_files, 'r') as infs:
        print('\n>>> Input files in {}'.format(input_files))
        for line in infs:
            if line.strip()[0] == '#':
                pass
            elif not line.strip():
                pass
            else:
                files = line.split(',')
                files[0] = files[0].rstrip().replace(' ', '')
                files[1] = files[1].rstrip().replace(' ', '')

                if '/' in files[0]:
                    s = files[0][0:files[0].rindex('/')+1]
                    if not os.path.exists(graphs_folder + s):
                        os.makedirs(graphs_folder + s)
                    if not os.path.exists(time_folder + s):
                        os.makedirs(time_folder + s)

                p = pops(files[0], xvgs_folder, fp, fv)
                rs = []
                for r, pk in zip(p.regions, p.peaks):
                    rs.append(region(r, pk, files[1]))
                DATA[files[0]]        = rs
                reading_order.append(files[0])
                peaksXtime[files[0]]  = []

    ################################################################

    keys = reading_order
    for k in keys:
        with open(DATA[k][0].points_file, 'r') as points:
            print(k, DATA[k][0].points_file)
            a = []
            t = []
            t0 = 0.0
            td = 1.0
            locked2 = False
            locked1 = False
            for line in points:
                if '#' in line or '@' in line:
                    pass
                else:
                    line_split = line.replace(',', ' ').split()
                    if len(line_split) == 2:
                        angle = float(line_split[1])
                        time  = float(line_split[0])
                        locked2 = True
                        if locked1:
                            raise Exception('ERROR: extra value in the dihedral file {}!\n{}\nConfID only reads files with one (average angle) or two columns (time and average angle).'.format(DATA[k][0].points_file, line_split))
                    elif len(line_split) == 1:
                        angle = float(line_split[0])
                        time  = t0 + td
                        t0    = time
                        locked1 = True
                        if locked2:
                            raise Exception('ERROR: missing value in the dihedral file {}!\n{}\nConfID only reads files with one (average angle) or two columns (time and average angle).'.format(DATA[k][0].points_file, line_split))
                    else:
                        raise Exception('ERROR: wrong number of columns ({}) in the dihedral file {}!\n{}\nConfID only reads files with one (average angle) or two columns (time and average angle).'.format(len(line_split), DATA[k][0].points_file, line_split))
                    t.append(time)
                    found = False
                    for r in DATA[k]:
                        if len(r.reg) == 2:
                            if angle > r.reg[0] and angle <= r.reg[1]:
                                r.points.append(angle)
                                a.append(r.peak)
                                peaksXtime[k].append((time, r.peak))
                                found = True
                        elif len(r.reg) == 4:
                            if angle > r.reg[0] and angle <= r.reg[1]:
                                r.points.append(angle+360.0)
                                a.append(r.peak)
                                peaksXtime[k].append((time, r.peak))
                                found = True
                            elif angle > r.reg[2] and angle <= r.reg[3]:
                                r.points.append(angle)
                                a.append(r.peak)
                                peaksXtime[k].append((time, r.peak))
                                found = True
                        else:
                            raise Exception('ERROR: wrong region length!\n{}\n{}\n{}'.format(DATA[k], r.reg, len(r.reg)))
                    if not found:
                        a.append('z')
                        peaksXtime[k].append((time, 'z'))
            ANGLES.append(a)
            TIMES.append(t)

    #for z in zip(ANGLES, TIMES):
    #    print(len(z[0]), len(z[1]))

    count = list(zip(*ANGLES))
    counter = Counter(count)
    regions_times = {}

    ################################################################
    print("\n#####################################\n>>>>>> DIHEDRAL POPULATIONS:\n")
    #print('>>> Dihedral populations for each torsion angle:')
    with open(output_folder+'DIHEDRAL_REGIONS.txt', 'w') as reg_file:
        ik = 1
        for k in keys:
            print('Angle #{}:  {}'.format(ik, k))
            pp = pprint.PrettyPrinter(indent=3)
            pp.pprint(DATA[k])
            reg_file.write('Angle #{}:  {}\n'.format(ik, k))
            pprint.pprint(DATA[k], stream=reg_file)
            ik+=1

    ################################################################
    print("\n#####################################\n>>>>>> CONFORMATIONAL POPULATIONS:\n")
    POP_ID = {}
    LAST_CONV = 1

    with open(output_folder+'CONFORMATIONAL_POPULATIONS.txt', 'w') as top_file:
        total_points = 0
        total_freq   = 0.0
        z_points     = 0
        z_freq       = 0.0
        major_points = 0
        major_freq   = 0.0

        if not show_z:
            top_file.write('Most common (excluding Z-regions):')
            print('Most common (excluding Z-regions):')
        else:
            top_file.write('Most common:')
            print('Most common:')
        max_rs_len = max(imap(len, imap(str, counter.elements())))

        pindex = 1
        for rs, cs in counter.most_common():
            POP_ID[rs] = pindex
            regions_times[rs] = []
            freq = round(float(cs)/float(len(ANGLES[0])), 6)
            if freq >= convergence_cutoff:
                LAST_CONV = pindex

            total_points += cs
            total_freq   += freq
            if 'z' not in rs:
                major_points += cs
                major_freq   += freq
                top_file.write('\nP#{:4d} {:{mrl}s}: {:6f} ({:6d})'.format(pindex, str(rs), freq, cs, mrl = max_rs_len))
                print('P#{:4d} {:{mrl}s}: {:6f} ({:6d})'.format(pindex, str(rs), freq, cs, mrl = max_rs_len))
                pindex += 1
            else:
                z_points += cs
                z_freq   += freq
                if show_z:
                    top_file.write('\nP#{:4d} {:{mrl}s}: {:6f} ({:6d})'.format(pindex, str(rs), freq, cs, mrl = max_rs_len))
                    print('P#{:4d} {:{mrl}s}: {:6f} ({:6d})'.format(pindex, str(rs), freq, cs, mrl = max_rs_len))
                    pindex += 1

        ################################################################

        top_file.write('\n===')
        #print('===')

        top_file.write("\nValid number of frames:     {:6f} ({:6d})".format(major_freq, major_points))
        print("\nValid number of frames:     {:6f} ({:6d})".format(major_freq, major_points))

        top_file.write("\nFrames in Z-region:         {:6f} ({:6d})".format(z_freq, z_points))
        print("Frames in Z-region:         {:6f} ({:6d})".format(z_freq, z_points))

        top_file.write("\nTotal number of frames:     {:6f} ({:6d})".format(total_freq, total_points))
        print("Total number of frames:     {:6f} ({:6d})".format(total_freq, total_points))
    #print('Saved file {}'.format(alias + '_TOP.txt'))

    ################################################################

    for i in range(len(list(count))):
        regions_times[count[i]].append(TIMES[0][i])

    ################################################################

    tt = 0
    for k in regions_times:
        tt += len(regions_times[k])
    #print('Total time frames: {}'.format(tt))

    ################################################################

    i = 0

    if not os.path.exists(output_folder + 'CONF_Frames/'):
        os.makedirs(output_folder + 'CONF_Frames/')

    for rs, cs in counter.most_common():
        freq = round(float(cs)/float(len(ANGLES[0])), 6)
        if freq >= convergence_cutoff:
            with open(output_folder+'CONF_Frames/Frames_Conf-'+str(i+1)+'.txt', 'w') as time_file:
                time_file.write(str(rs))
                for t in regions_times[rs]:
                    time_file.write('\n' + str(t))
        i += 1
        #print('Saved file {}'.format(alias+'_'+str(i+1)+'.txt'))

    ################################################################
    print("\n#####################################\n>>>>>> TRANSITIONS:\n")
    print('Computing dihedral transitions...')
    with open(time_folder + 'TRANSITIONS.txt', 'w') as ctran_file:
        max_k_len = max(imap(len, imap(str, keys)))
        #print(max_k_len)
        for k in keys:
            first_node = None
            last_node  = None
            nodes = {}
            edges = {}

            with open(xvgs_folder + k.replace('dist.xvg', 'peaks.xvg').replace('Dihedrals/', ''), 'w') as pt_file:
                with open(time_folder + k.replace('dist.xvg', 'transitions.txt'), 'w') as tran_file:
                    pt_file.write('@    title "Region Peak Angle: "\n@    xaxis  label "Time"\n@    yaxis  label "Peak (degrees)"\n@TYPE xy\n')
                    transitions = 0
                    p_ant = peaksXtime[k][0][1]
                    if not show_z:
                        i = 0
                        while p_ant == 'z':
                            p_ant = peaksXtime[k][i][1]
                            i += 1
                    first_node = p_ant
                    for t, p in peaksXtime[k]:
                        if p != 'z':
                            pt_file.write('{:13.5f}   {:8.3f}\n'.format(float(t), float(p)))
                        elif show_z:
                            pt_file.write('# {:13.5f}        {:12s}\n'.format(float(t), p))
                        if p != p_ant:
                            if show_z or p != 'z':
                                transitions += 1
                                tran_file.write('{:6s} -> {:6s} | t = {:9.1f}\n'.format(str(p_ant), str(p), t))
                                if (p_ant, p) in edges:
                                    edges[(p_ant, p)] += 1.0
                                else:
                                    edges[(p_ant, p)] = 1.0
                        if show_z or p != 'z':
                            p_ant = p
                            if p in nodes:
                                nodes[p] += 1.0
                            else:
                                nodes[p] = 1.0
                            last_node = p
                    if transitions == 0:
                        tran_file.write('{:6s} -> {:6s} | t = {:9.1f}\n'.format(str(p_ant), str(p_ant), peaksXtime[k][-1][0]))
                #print('Saved file {}'.format(output_folder + k.replace('dist.xvg', 'trans.txt')))

            print('{:{mkl}s} transitions: {:7d}'.format(k, transitions, mkl = max_k_len))
            #print('Saved file {}'.format(xvgs_folder + k.replace('dist.xvg', 'peaks.xvg')))
            ctran_file.write('{:{mkl}s} transitions: {:7d}\n'.format(k, transitions, mkl = max_k_len))

            show_graph(nodes, edges, first_node, last_node, cutoff, graphs_folder + k.replace('dist.xvg', 'network.txt'), plot_graph)
        #######################################################################################################

        print('\nComputing conformational transitions and convergence...')

        if not os.path.exists(output_folder + 'Convergence/'):
            os.makedirs(output_folder + 'Convergence/')

        with open(time_folder + 'CONF.transitions.txt', 'w') as alltran_file:
            with open(time_folder + 'CONF.transitions.xvg', 'w') as pta_file:
                with open(output_folder + 'Convergence/Sampling_Evolution.xvg', 'w') as popuconv_file:
                    popuconv_file.write('@    title "Convergence: "\n@    xaxis  label "Time"\n@    yaxis  label "N of populations"\n@TYPE xy\n')

                    first_node = None
                    last_node  = None
                    nodes = {}
                    edges = {}

                    pta_file.write('@    title "Region Transition: "\n@    xaxis  label "Time"\n@    yaxis  label "Trasition (1 yes | 0 no)"\n@TYPE xy\n')
                    transitions = 0
                    ziped = list(zip(*ANGLES))
                    loop_size = len(ziped)
                    a_ant = ziped[0]
                    if not show_z:
                        i = 0
                        while 'z' in a_ant and i < loop_size:
                            a_ant = ziped[i]
                            i += 1
                    first_node = a_ant
                    percent_time = 0.0
                    percent_mark = 0.0
                    zipziped = list(zip(zip(*ANGLES), zip(*TIMES)))
                    loop_size = len(zipziped)

                    #For convergence:
                    pop_freqs = {}
                    for k in POP_ID:
                        pop_freqs[k] = [(0.0, 0)]
                    find_pops = set([])
                    old_time = 0.0
                    i_time = 0
                    #################

                    for a, t in zipziped:

                        if percent_time / float(loop_size) >= percent_mark:
                            print('({:5.1f}%)'.format((percent_time / float(loop_size))*100.0))
                            percent_mark += 0.1
                        percent_time += 1.0

                        #For convergence:
                        if show_z or 'z' not in a:
                            find_pops.add(a)
                        pop_freqs[a].append((pop_freqs[a][-1][0] + (t[0] - old_time), i_time))
                        old_time = t[0]
                        popuconv_file.write('{:13.5f}   {:8.3f}\n'.format(float(t[0]), float(len(find_pops))))
                        i_time += 1
                        ################

                        if a != a_ant:
                            if show_z or 'z' not in a:
                                transitions += 1
                                alltran_file.write('{:25s} -> {:25s} | t = {:9.1f}\n'.format(str(a_ant), str(a), t[0]))
                                pta_file.write('{:13.5f}   {:8.3f}\n'.format(float(t[0]), 1.0))
                                if (a_ant, a) in edges:
                                    edges[(a_ant, a)] += 1.0
                                else:
                                    edges[(a_ant, a)] = 1.0
                            else:
                                pta_file.write('{:13.5f}   {:8.3f}\n'.format(float(t[0]), 0.0))
                        else:
                            pta_file.write('{:13.5f}   {:8.3f}\n'.format(float(t[0]), 0.0))
                        if show_z or 'z' not in a:
                            a_ant = a
                            if a in nodes:
                                nodes[a] += 1.0
                            else:
                                nodes[a] = 1.0
                            last_node = a

                print("(100.0%)")

                print('\n{:16s} transitions: {:7d}'.format('Conformational', transitions))
                print('\nCreating transitions network...')
                show_graph(nodes, edges, first_node, last_node, cutoff, graphs_folder + 'CONF_network.txt', plot_graph, POP_ID)
                ctran_file.write('{:16s} transitions: {:7d}\n'.format('Conformational', transitions))
        #print('Saved file {}'.format(alias + '_COUNT_TRAN.txt'))

    #######################################################################################################

    print('Computing conformational frequency convergence...')
    timeziped = list(zip(*TIMES))
    for k in POP_ID:
        if POP_ID[k] <= LAST_CONV:
            freqconv_file = open(output_folder + 'Convergence/Freq_Conf-{}.xvg'.format(POP_ID[k]), 'w')
            freqconv_file.write('@    title "Frequency convergence: "\n@    xaxis  label "Time"\n@    yaxis  label "Frequency"\n@TYPE xy\n')
            p_f = pop_freqs[k]
            freqs = []

            last_f = p_f[0][0]
            last_i = p_f[0][1]
            for f, i in p_f:
                for j in range(last_i, i):
                    freqs.append(last_f)
                last_f = f
                last_i = i
            for j in range(last_i, loop_size-1):
                freqs.append(last_f)

            ziptimeziped = list(zip(freqs, timeziped))
            for f, t in ziptimeziped:
                if float(t[0]) == 0.0:
                    freqconv_file.write('{:13.5f}   {:9.6f}\n'.format(float(t[0]), 0.0))
                else:
                    freqconv_file.write('{:13.5f}   {:9.6f}\n'.format(float(t[0]), f/float(t[0])))
            freqconv_file.close()

    print ('Finished.')
    return POP_ID
