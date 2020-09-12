#!/usr/bin/env python3
from result import Result

def iterme(arg):
    options, (p1, ident) = arg
    VERBOSE = options.verbose

    gs = []
    mx = len(ps2)
    for (p2,i) in zip(ps2, range(mx)):
        if VERBOSE: print(f"Thread {i} on iteration {i}/{mx}.")
        for p3 in ps3:
            for p4 in ps4:
                gs.append(Result(p1, p2, p3, p4))
    return gs

if __name__ == "__main__":
    from optparse import OptionParser
    from multiprocessing import Pool
    from itertools import permutations
    from collections import Counter
    from teams import pool1, pool2, pool3, pool4
    from os import sched_getaffinity

    parser = OptionParser()
    parser.add_option("-t", "--threads", dest="threads", default=len(sched_getaffinity(0)),
                      type="int", help="maximum size of thread pool to use", metavar="THREADS")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()

    teams = []
    for i in range(4):
        teams.append(pool1[i])
    for i in range(4):
        teams.append(pool2[i])
    for i in range(4):
        teams.append(pool3[i])
    for i in range(4):
        teams.append(pool4[i])

    print(f'Simulating teams: {", ".join(map(str, teams))}')

    # The group draw goes before Play-ins.  Pool 4 teams are drawn into groups after Play-ins ends.

    # Create a list of all draw order permutations, ignoring team selection
    ps1 = list(permutations(pool1))
    ps2 = list(permutations(pool2))
    ps3 = list(permutations(pool3))
    ps4 = list(permutations(pool4))

    mppool = Pool(options.threads)
    results = mppool.map(iterme, map(lambda x: (options, x), zip(ps1, range(len(ps1)))))

    result_groups = [g for gs in results for g in gs]

    with open("output.txt", "w") as out_file:
        print(f"Storing {len(result_groups)} groups into {out_file.name}")
        for result in result_groups:
            print(result, file=out_file)

    with open("raw_groups.txt", "w") as group_file:
        print(f"Storing {len(result_groups)} groups into {group_file.name}")
        for result in result_groups:
            print(result.groups, file=group_file)

    # Sort the groups so that order will not matter, reducing hash values
    for result in result_groups:
        result.sort_groups()

    with open("totals.txt", "w") as totals_file:
        totals = Counter()
        for result in result_groups:
            totals[str(result.groups)] += 1
        print(f"Storing {len(totals)} hashes into {totals_file.name}")
        for key in totals:
            print(f"{key} - {totals[key]}", file=totals_file)

