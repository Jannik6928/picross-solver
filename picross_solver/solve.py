def generate_candidates(dim, line):
    ocandidates = []
    for i in range(dim):
        ocandidates.append([-1])

    total = sum(line)
    first = 0
    last = len(ocandidates) - (total - line[0] + len(line) - 1)

    for i in range(len(line)):
        pad = (last - first) - line[i]
        length = line[i] - pad

        for j in range(first, last):
            ocandidates[j].append(i)
        if (length > 0):
            for j in range(first + pad, first + pad + length):
                ocandidates[j] = [i]

        if (i != len(line) - 1):
            first = first + line[i] + 1
            last = last + line[i + 1] + 1

    return ocandidates


def eliminate_candidates(candidates, line):
    # removes all runs which are not long enough to fit their candidate
    for i in range(len(line)):
        run_length = 0
        for j in range(len(candidates)):
            if i in candidates[j]:
                run_length = run_length + 1
            else:
                if run_length < line[i]:
                    for k in range(run_length):
                        candidates[j - 1 - k].remove(i)
                run_length = 0

    # removes all candidate marks which are too far away from anchors and fills in gaps between anchors
    for i in range(len(line)):
        first = len(candidates)
        last = -1
        for j in range(len(candidates)):
            if candidates[j] == [i]:
                first = min(first, j)
                last = max(last, j)
        for j in range(first, last + 1):
            candidates[j] = [i]
        length = last - first + 1
        max_dist = line[i] - length
        if length > 0:
            for j in range(len(candidates)):
                if i in candidates[j] and (j - max_dist > last or j + max_dist < first):
                    candidates[j].remove(i)

    # expands run if it is too close to boundary (wall, anchor, cross)
    for i in range(len(line)):
        found = False
        left = 0
        right = len(candidates)
        for j in range(len(candidates)):
            if len(candidates[j]) == 1:
                if found:
                    if candidates[j] != [i]:
                        right = j
                        break
                else:
                    if candidates[j] == [i]:
                        found = True
                    else:
                        left = j + 1
        pad = (right - left) - line[i]
        length = line[i] - pad
        if found:
            for j in range(left + pad, left + pad + length):
                candidates[j] = [i]

    # if there is only one candidate run, will squeeze the candidates
    for i in range(len(line)):
        num_runs = 0
        run_index = -1
        run_length = 0
        for j in range(len(candidates)):
            if i in candidates[j]:
                if run_length == 0:
                    num_runs = num_runs + 1
                    run_index = j
                    run_length = 1
                else:
                    run_length = run_length + 1
        if num_runs == 1:
            pad = run_length - line[i]
            length = line[i] - pad
            if length > 0:
                for j in range(run_index + pad, run_index + pad + length):
                    candidates[j] = [i]

    # stuff
    for i in range(1, len(candidates)):
        if len(candidates[i]) == 1 and candidates[i] != [-1]:
            candidates[i - 1] = [x for x in [-1, candidates[i][0]] if x in candidates[i - 1]]
    for i in range(0, len(candidates) - 1):
        if len(candidates[i]) == 1 and candidates[i] != [-1]:
            candidates[i + 1] = [x for x in [-1, candidates[i][0]] if x in candidates[i + 1]]

    return candidates


def share_solved(orows_p, ocols_p):
    for i in range(len(orows_p)):
        for j in range(len(orows_p[i])):
            if orows_p[i][j] == [-1]:
                ocols_p[j][i] = [-1]
            if ocols_p[j][i] == [-1]:
                orows_p[i][j] = [-1]
            if -1 not in orows_p[i][j]:
                if -1 in ocols_p[j][i]:
                    ocols_p[j][i].remove(-1)
            if -1 not in ocols_p[j][i]:
                if -1 in orows_p[i][j]:
                    orows_p[i][j].remove(-1)
    return orows_p, ocols_p


if __name__ == '__main__':
    input = open('input.txt', 'r')

    dimx, dimy = input.readline().split(' ')
    dimx = int(dimx)
    dimy = int(dimy)

    rows = []
    cols = []

    input.readline()
    for i in range(dimx):
        nums = [int(n) for n in input.readline().split(' ')]
        rows.append(nums)
    input.readline()
    for i in range(dimy):
        nums = [int(n) for n in input.readline().split(' ')]
        cols.append(nums)

    orows = [generate_candidates(dimx, rows[i]) for i in range(len(rows))]
    ocols = [generate_candidates(dimy, cols[i]) for i in range(len(cols))]

    for i in range(100):
        orows = [eliminate_candidates(orows[i], rows[i]) for i in range(len(rows))]
        ocols = [eliminate_candidates(ocols[i], cols[i]) for i in range(len(cols))]

        temp = share_solved(orows, ocols)
        orows = temp[0]
        ocols = temp[1]

    print(*orows, sep='\n')
    print()

    print(*ocols, sep='\n')
    print()

    output = open('output.txt', 'w')
    for i in range(len(orows)):
        for j in range(len(orows[i])):
            if len(orows[i][j]) == 1:
                if orows[i][j] == [-1]:
                    output.write('.')
                else:
                    output.write('O')
            elif len(ocols[j][i]) == 1:
                if ocols[j][i] == [-1]:
                    output.write('.')
                else:
                    output.write('O')
            else:
                output.write('?')
        output.write('\n')
    output.write('\n')
