#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Bruno Iochins Grisci e Marcelo Depolo Poleto
#OCTOBER/2019
#http://sbcb.inf.ufrgs.br/confid

header    = """
    ###########################################################################
    #                        Conformational Identifier                        #
    #                            ConfID 0.1.0 (2019)                          #
    #                                                                         #
    # Marcelo D Poleto, Bruno I Grisci, Marcio Dorn, Hugo Verli, ConfID: an   #
    # analytical method for conformational characterization of small          #
    # molecules using molecular dynamics trajectories, Bioinformatics, Volume #
    # X, Issue X, Day Month 2019, Pages XXXX-XXX, doi                         #
    #                                                                         #
    #                    http://sbcb.inf.ufrgs.br/confid                      #
    #                                                                         #
    #            In case of bugs or suggestions, please contact us:           #
    #                         marcelo.poleto@ufv.br                           #
    #                         bigrisci@inf.ufrgs.br                           #
    #                                                                         #
    # LGPL-3.0-or-later                               ® BR512019001928-8 2019 #
    ###########################################################################\n\n"""

welcome   = "Welcome to ConfID! Everything looks good so far.\nTo run ConfID, please provide the path to the input_file.inp and optionally the path to the config file.\nHave a nice \"ConfIDent\" analysis! =)"

help_text = """
    ###########################################################################

    Welcome to ConfID!

    ##

    If you installed ConfID using the snap store, you can run it on your
    terminal by typing:
    $ confid input.inp config

    ##

    input.inp is the input file and should follow this template:

        # Comment that is ignored
        Path/to/file/file1.aver.xvg
        Path/to/file/file2.aver.xvg
        Path/to/file/fileN.aver.xvg

    ##

    The config file is an optional text file you can use to modify ConfID 
    default mode. It should follow this template, with the capitalized flags
    on the left column and the desired values in the right column, separeted 
    only by white spaces: 

        RESULTS_FOLDER       Populations/
        DIH_POP_FOLDER       Dihedral_Regions/
        NETWORK_FOLDER       Networks/
        TIME_STATS_FOLDER    Time_Dependent_Stats/
        SHOW_Z               False
        NETWORK_CUTOFF       0.01
        PLOT_NETWORK         False
        CONVERGENCE_CUTOFF   0.01
        FACTOR_PEAK          50.0
        FACTOR_VALLEY        60.0
        TIME_DEPENDENT_STATS True
        DATA_1               sum
        DATA_2               aver

    Observe that the values above are the default values that ConfID will
    use if there is no config file!

    ## 

    The config file has many flags, below is the definition of each of them:

    RESULTS_FOLDER          (string)                   
    DIH_POP_FOLDER          (string)          
    NETWORK_FOLDER          (string)               
    SHOW_Z             	    (string)          [False / True]
    NETWORK_CUTOFF          (float)           [>= 0.0]      
    PLOT_NETWORK            (string)          [False / True]     
    CONVERGENCE_CUTOFF 	    (float)           [>= 0.0]                       
    FACTOR_PEAK        	    (float)           [>= 1.0, < FACTOR_VALLEY]    
    FACTOR_VALLEY      	    (float)           [>= 1.0, > FACTOR_PEAK]         
    TIME_DEPENDENT_STATS    (string)          [False / True]              
    DATA_1             	    (list of strings) [sum / max / min / aver / std / 
                                               median / count]
    DATA_2             	    (list of strings) [sum / max / min / aver / std / 
                                               median / count]

    ###

    RESULTS_FOLDER:      	- specifies the directory in which output files 
                            should be saved.
    DIH_POP_FOLDER:        	- specifies the directory in which output .xvg 
                            files should be saved.
    NETWORK_FOLDER:      	- specifies the directory in which output 
                            network files should be saved.
    SHOW_Z:             	- flag that determines if spurious regions 
                            (Z) should be represented in the results. They 
                            will be used in the internal calculations 
                            nevertheless. If this is True please consider 
                            setting PLOT_NETWORK to False, as plotting the 
                            chart may become too slow. 
    NETWORK_CUTOFF:       	- the smallest transition frequency required 
                            for an edge to appear in the networks. If equal 
                            to 0.0, all edges are considered. If this 
                            cutoff is too small please consider setting 
                            PLOT_NETWORK to False, as plotting the chart 
                            may become too slow. 
    PLOT_NETWORK:         	- if True, network figures for the transitions 
                            will be created using the graphviz library. 
                            Networks text files will be created if it is 
                            either True or False.
    CONVERGENCE_CUTOFF: 	- the smallest population frequency at the end 
                            of the simulation required for the convergence 
                            file for that population to be generated. If 
                            equal to 0.0, all populations will be 
                            represented, but for a large number of dihedral
                            angles this can take a while.
    FACTOR_PEAK         	- factor that sets the constriction for peaks 
                            selection. Larger values lessen the constriction.
                            Must be larger or equal to 1.0 and smaller than 
                            FACTOR_VALLEY.
    FACTOR_VALLEY       	- factor that sets the constriction for valleys 
                            selection. Lower values lessen the constriction. 
                            Must be larger or equal to 1.0 and larger than 
                            FACTOR_PEAK.
    TIME_DEPENDENT_STATS:	- flag that determines if the statistics of the 
                            time stayed at each population should be computed.
    DATA_1:             	- list of functions that should be used as the x
                            axis of the charts of the statistics of the time 
                            stayed at each population and how the report 
                            should be ordered.  
    DATA_2:             	- list of functions that should be used as the y
                            axis of the charts of the statistics of the time 
                            stayed at each population and how the report 
                            should be ordered.

    ###

    TIME-DEPENDENT PROPERTIES AVAILABLE:

    - sum: total time in a population
    - max: maximum time spent in a population without leaving
    - min: minimum time spent in a population without leaving
    - aver: average time spent in a population without leaving
    - std: standard deviation of the average time
    - median: median time spent in a population without leaving
    - count: amount of times of a transition event entering this population

    ###

    Are you trying to read or write files in a removable media (pendrives, 
    external HDs, etc)?
    Then you must give ConfID access to removable media after installing it by 
    running the following command in your terminal:
    $ snap connect confid:removable-media

    ###

    For more information please visit http://sbcb.inf.ufrgs.br/confid

    Have a nice "ConfIDent" analysis! =)

    ###########################################################################"""