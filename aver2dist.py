import numpy as np
import os

def convert(input_files, dihedral_folder='Dihedrals/'):

    if not os.path.exists(dihedral_folder):
        os.makedirs(dihedral_folder)

    n_angles = []
    files_paths = []
    with open(input_files, 'r') as infs:
        for line in infs:
            if line[0] == '#':
                pass
            elif line[0] == '\n':
                pass
            else:
                files = line.split(',')
                aver_file = input_files.replace(os.path.basename(input_files), '') + files[0].rstrip().replace(' ', '')
                name = os.path.basename(aver_file)
                name, extension = os.path.splitext(name)
                dist_file = dihedral_folder+os.path.basename(aver_file).replace(os.path.basename(aver_file), name+'.dist.xvg')
                files_paths.append([dist_file, aver_file])

                angles = []

                with open(aver_file, 'r') as af:
                    for line in af:
                        l = line.rstrip().replace(',', ' ').split()
                        if l[0][0] != "#" and l[0][0] != "@":
                            if len(l) == 2:
                                angles.append(float(l[1]))
                            elif len(l) == 1:
                                angles.append(float(l[0]))
                            else:
                                raise Exception('ERROR: wrong number of columns ({}) in the dihedral file {}:\n{}'.format(len(l), aver_file, l))

                n_angles.append(len(angles))
                if len(n_angles) >= 2:
                    if n_angles[-1] != n_angles[-2]:
                        raise Exception('ERROR: conflicting number of timesteps ({} != {}) in the dihedral file {}.\n'.format(n_angles[-1], n_angles[-2], aver_file))
                angles = np.array(angles)
                avg_angle = round(angles.mean(), 4)
                angles = np.round(angles)
                unique, counts = np.unique(angles, return_counts=True)
                dist = list(zip(unique, np.round(counts/float(len(angles)), 6)))
                zeroes = set(range(-180,180)) - set(angles)
                for z in zeroes:
                    dist.append((z, 0.0))

                header = "# Created by:\n#\t\tConfID - Conformational Identifier\n@    title \"Dihedral Distribution: {}\"\n@    xaxis label \"Degrees\"\n@    yaxis label \"Distribution\"\n@TYPE xy\n@    subtitle \"average angle: {}\\So\\N\"".format(name, avg_angle)

                with open(dist_file, 'w') as df:
                    df.write(header)
                    for a in sorted(dist):
                        df.write("\n     {:4d}    {:1.6f}".format(int(a[0]), a[1]))

    new_inputs = input_files.replace(os.path.basename(input_files), '__newinputs.inp')
    with open(new_inputs, 'w') as ni:
        ni.write('#This file was automatically created by ConfID.\n#Please do not try to use it as an input for the program, nor change or delete it while ConfID is running.\n#This file will self destruct.')
        ni.write('\n#Order: Distribution, Fluctuation')
        for fp in files_paths:
            ni.write('\n{}, {}'.format(fp[0], fp[1]))

    return new_inputs
