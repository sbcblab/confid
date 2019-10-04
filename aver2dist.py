import numpy as np

name = "DIH1"
aver_file = "Tutorials/ANA/DIH1.aver.xvg"

angles = []

with open(aver_file, 'r') as af:
    for line in af:
        l = line.rstrip()
        l = l.split()
        if l[0][0] != "#" and l[0][0] != "@":
            angles.append(float(l[1]))

angles = np.array(angles)
avg_angle = round(angles.mean(), 4)
angles = np.round(angles)
unique, counts = np.unique(angles, return_counts=True)
dist = list(zip(unique, np.round(counts/float(len(angles)), 6)))
zeroes = set(range(int(min(angles))-1, int(max(angles)+2))) - set(angles)
for z in zeroes:
    dist.append((z, 0.0))

header = "# Created by:\n#\t\tConfID - Conformational Identifier\n@    title \"Dihedral Distribution: {}\"\n@    xaxis label \"Degrees\"\n@    yaxis label \"\"\n@TYPE xy\n@    subtitle \"average angle: {}\\So\\N\"".format(name, avg_angle)

print(header)
for a in sorted(dist):
    print("     {:4d}    {:1.6f}".format(int(a[0]), a[1]))
