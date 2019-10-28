#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Bruno Iochins Grisci e Marcelo Depolo Poleto
#APRIL/2019
#http://sbcb.inf.ufrgs.br/confid

import timeit
import sys
import os

import check_dep
import count_populations
import count_stay
import aver2dist
import confid_help

if __name__ == '__main__':

    print(confid_help.header)    

    try:
        print('You are running Python {}'.format(sys.version))
    except:
        pass
    start = timeit.default_timer()
    check_dep.check()

    DIST_DIR = "Dihedrals/"

    output_folder = 'Output/Populations/'
    xvgs_folder   = 'Output/Dihedral_Regions/'
    graphs_folder = 'Output/Networks/'
    time_folder   = 'Output/Time_Dependent_Stats/'
    show_z        = False
    cutoff        = 0.01
    plot_graph    = False
    convergence_cutoff = 0.01
    fp            = 50.0
    fv            = 60.0
    show_kinetic  = True
    fun1          = ['sum']
    fun2          = ['aver']

    if len(sys.argv) == 1:
        print(confid_help.welcome)
        sys.exit(0)
    
    elif len(sys.argv) == 3:
        input_files = sys.argv[1]
        config_file = sys.argv[2]
        print(">>>>>> READING INPUT:")
        print('\n>>> Parameters in {}:'.format(config_file))

        try:
            with open(input_files, 'r') as ti:
                pass
        except PermissionError:
            raise Exception("\n\nIMPORTANT! Are you trying to read or write files in a removable media (pendrives, external HDs, etc)?\nThen you must give ConfID access to removable media after installing it by running the following command in your terminal:\nsnap connect confid:removable-media")

        try:
            with open(config_file, 'r') as tc:
                pass
        except PermissionError:
            raise Exception("\n\nIMPORTANT! Are you trying to read or write files in a removable media (pendrives, external HDs, etc)?\nThen you must give ConfID access to removable media after installing it by running the following command in your terminal:\nsnap connect confid:removable-media")

        with open(config_file, 'r') as cf:
            for line in cf:
                l = line.rstrip()
                l = l.split()
                if l[0].upper() == 'RESULTS_FOLDER':
                    if l[1][-1] == '/':
                        output_folder = l[1]
                    else:
                        output_folder = l[1]+'/'
                    print('{} = {}'.format(l[0], output_folder))
                elif l[0].upper() == 'DIH_POP_FOLDER':
                    if l[1][-1] == '/':
                        xvgs_folder = l[1]
                    else:
                        xvgs_folder = l[1]+'/'
                    print('{} = {}'.format(l[0], xvgs_folder))
                elif l[0].upper() == 'TIME_STATS_FOLDER':
                    if l[1][-1] == '/':
                        time_folder = l[1]
                    else:
                        time_folder = l[1]+'/'
                    print('{} = {}'.format(l[0], time_folder))
                elif l[0].upper() == 'NETWORK_FOLDER':
                    if l[1][-1] == '/':
                        graphs_folder = l[1]
                    else:
                        graphs_folder = l[1]+'/'
                    print('{} = {}'.format(l[0], graphs_folder))
                elif l[0].upper() == 'SHOW_Z':
                    show_z = l[1].lower() == 'true'
                    print('{} = {}'.format(l[0], show_z))
                elif l[0].upper() == 'NETWORK_CUTOFF':
                    cutoff = float(l[1])
                    print('{} = {}'.format(l[0], cutoff))
                elif l[0].upper() == 'PLOT_NETWORK':
                    plot_graph = l[1].lower() == 'true'
                    print('{} = {}'.format(l[0], plot_graph))
                    if plot_graph:
                        try:
                            import graphviz
                        except:
                            raise Exception("\n\nERROR: graphviz package needs to be installed if PLOT_NETWORK is True, but it couldn't be imported.")
                elif l[0].upper() == 'CONVERGENCE_CUTOFF':
                    convergence_cutoff = float(l[1])
                    print('{} = {}'.format(l[0], convergence_cutoff))
                elif l[0].upper() == 'FACTOR_PEAK':
                    fp = float(l[1])
                    if fp < 1.0:
                        raise Exception('\n\nERROR: FACTOR_PEAK ({}) must be larger or equal to 1.0.\n'.format(fp))
                    print('{} = {}'.format(l[0], fp))
                elif l[0].upper() == 'FACTOR_VALLEY':
                    fv = float(l[1])
                    if fv < 1.0:
                        raise Exception('\n\nERROR: FACTOR_VALLEY ({}) must be larger or equal to 1.0.\n'.format(fv))
                    print('{} = {}'.format(l[0], fv))
                elif l[0].upper() == 'TIME_DEPENDENT_STATS':
                    show_kinetic = l[1].lower() == 'true'
                    print('{} = {}'.format(l[0], show_kinetic))
                    if show_kinetic:
                        try:
                            import matplotlib.pyplot
                        except:
                            raise Exception("\n\nERROR: matplotlib.pyplot package needs to be installed if TIME_DEPENDENT_STATS is True, but it couldn't be imported.")
                elif l[0].upper() == 'DATA_1':
                    fun1 = []
                    for i in range(1, len(l)):
                        fun1.append(l[i].lower())
                    print('{} = {}'.format(l[0], fun1))
                elif l[0].upper() == 'DATA_2':
                    fun2 = []
                    for i in range(1, len(l)):
                        fun2.append(l[i].lower())
                    print('{} = {}'.format(l[0], fun2))
                else:
                    print('\nWARNING: Unidentified parameter ignored: {} {}\n'.format(l[0], l[1]))
    
    elif len(sys.argv) == 2:
        input_files = sys.argv[1]

        if input_files in ['-h', '-H', '-help', '--h', '--H', '--help']:
            print(confid_help.help_text)
            sys.exit(0)

        try:
            with open(input_files, 'r') as ti:
                pass
        except PermissionError:
            raise Exception("\n\nIMPORTANT! Are you trying to read or write files in a removable media (pendrives, external HDs, etc)?\nThen you must give ConfID access to removable media after installing it by running the following command in your terminal:\nsnap connect confid:removable-media")


        print('USING DEFAULT CONFIG PARAMETERS:\n')
        print('RESULTS_FOLDER       = {}'.format(output_folder))
        print('DIH_POP_FOLDER       = {}'.format(xvgs_folder))
        print('TIME_STATS_FOLDER    = {}'.format(time_folder))
        print('NETWORK_FOLDER       = {}'.format(graphs_folder))
        print('SHOW_Z               = {}'.format(show_z))
        print('NETWORK_CUTOFF       = {}'.format(cutoff))
        print('PLOT_NETWORK         = {}'.format(plot_graph))
        print('CONVERGENCE_CUTOFF   = {}'.format(convergence_cutoff))
        print('FACTOR_PEAK          = {}'.format(fp))
        print('FACTOR_VALLEY        = {}'.format(fv))
        print('TIME_DEPENDENT_STATS = {}'.format(show_kinetic))
        print('DATA_1               = {}'.format(fun1))
        print('DATA_2               = {}\n'.format(fun2))

    else:
        raise Exception('\n\nERROR: wrong number of parameters given to ConfID: {} {}\nTo run ConfID, please provide the path to the input_file.inp and optionally the path to the config file.'.format(len(sys.argv[1:]), sys.argv[1:]))

    if fp >= fv:
        raise Exception('\n\nERROR: FACTOR_VALLEY ({}) must be larger than FACTOR_PEAK ({}).\n'.format(fv, fp))

    if show_z and plot_graph:
        print('\nWARNING: plotting the graph figures may become too slow if the Z populations are to be shown, please consider setting either SHOW_Z or PLOT_NETWORK to False, or to use a large NETWORK_CUTOFF.\n')


    new_inputs = aver2dist.convert(input_files, dihedral_folder=DIST_DIR)

    POP_ID = count_populations.main(new_inputs, output_folder, xvgs_folder, time_folder, graphs_folder, show_z, cutoff, plot_graph, convergence_cutoff, fp, fv)

    if show_kinetic:
        print("\n#####################################\n>>>>>> CONFORMATIONAL TIME-DEPENDENT STATISTICS:")

        if (not show_z):
            print('\nWARNING: the frequency of the conformational populations in the stay stats may vary slightly from the previous results if Z populations are disregarded.\n')

        path = time_folder + 'CONF.transitions.txt'
        for f1 in fun1:
            for f2 in fun2:
                print('==')
                print('First  axis: ' + f1)
                print('Second axis: ' + f2)
                print(path)
                count_stay.main(path, f1, f2, POP_ID)

        with open(new_inputs, 'r') as infs:
            files_paths = []
            for line in infs:
                if line[0] == '#':
                    pass
                elif line[0] == '\n':
                    pass
                else:
                    files = line.split(',')
                    files[0] = files[0].rstrip().replace(' ', '')
                    path = time_folder + files[0].replace('dist.xvg', 'transitions.txt')
                    files_paths.append(path)

        print("\n#####################################\n>>>>>> DIHEDRAL TIME-DEPENDENT STATISTICS:")

        for fp in files_paths:
            for f1 in fun1:
                for f2 in fun2:
                    print('==')
                    print('First  axis: ' + f1)
                    print('Second axis: ' + f2)
                    print(fp)
                    count_stay.main(fp, f1, f2)

    try:
        if os.path.exists(new_inputs):
            os.remove(new_inputs)
    except:
        print('\nWARNING: Could not remove file {}.\n'.format(new_inputs))
        pass

    try:
        if os.path.exists(DIST_DIR):
            os.rename(DIST_DIR, xvgs_folder+"Dihedrals_Dist/")
    except:
        print('\nWARNING: Could not move folder {} to {}.\n'.format(DIST_DIR, xvgs_folder+"Dihedrals_Dist/"))
        pass

    print ('==\nFinished.\n')

    stop = timeit.default_timer()

    print('Runtime: {} sec'.format(round(stop - start,2)))