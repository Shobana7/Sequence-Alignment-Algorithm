import resource
from time import perf_counter
from sys import argv

def parse_input(filename):
	bases = []
	indices = [[], []]
	with open(filename) as infile:
		lines = infile.readlines()
		idx = -1
		for line in lines:
			line = line.strip()
			if line.isnumeric():
				indices[idx].append(int(line))
			else:
				bases.append(line)
				idx += 1
	return bases, indices

def generate_string(base, indices):
    for i in indices:
	    base = base[:i+1] + base + base[i+1:]
    return base

def check_string_length(s, b, i):
    assert len(s) == (2 ** len(i)) * len(b)

def compute_memo(str1, str2, gamma, penalty, efficient=True):
    m = len(str1)
    n = len(str2)        
    if efficient:
        memo = [[0 for _ in range(n + 1)] for _ in range(2)]
        for i in range(n + 1):
            memo[0][i] = gamma * i
        for i in range(1, m + 1):
            memo[1][0] = gamma * i
            for j in range(1, n + 1):
                memo[1][j] = min(
                    penalty[str1[i-1]][str2[j-1]] + memo[0][j-1],
                    gamma + memo[0][j],
                    gamma + memo[1][j-1]
                )
            if i < m:
                memo[0] = [m for m in memo[1]]
    else:
        memo = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(m + 1):
            memo[i][0] = gamma * i
        for i in range(n + 1):
            memo[0][i] = gamma * i
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                memo[i][j] = min(
                    penalty[str1[i-1]][str2[j-1]] + memo[i-1][j-1],
                    gamma + memo[i-1][j],
                    gamma + memo[i][j-1]
                )
    return memo

def track_memo(memo, str1, str2, gamma, penalty):
    i, j = len(memo) - 1, len(memo[0]) - 1
    trace1 = ''
    trace2 = ''
    while i > 0 or j > 0:
        if memo[i][j] == gamma + memo[i-1][j]:
            trace1 = str1[i-1] + trace1
            trace2 = '_' + trace2
            i -= 1
        elif memo[i][j] == gamma + memo[i][j-1]:
            trace2 = str2[j-1] + trace2
            trace1 = '_' + trace1
            j -= 1
        elif memo[i][j] == penalty[str1[i-1]][str2[j-1]] + memo[i-1][j-1]:
            trace1 = str1[i-1] + trace1
            trace2 = str2[j-1] + trace2
            i -= 1
            j -= 1
    return trace1, trace2

def compute_alignment(str1, str2, gamma, penalty):
    if len(str1) <= 2 or len(str2) <= 2:
        memo = compute_memo(str1, str2, gamma, penalty, efficient=False)
        alignment = track_memo(memo, str1, str2, gamma, penalty)
        
        return alignment

    brk1 = len(str1) // 2
    forward = compute_memo(str1[:brk1], str2, gamma, penalty)[1]
    backward = compute_memo(str1[-1:brk1-1:-1], str2[-1::-1], gamma, penalty)[1][-1::-1]
    brk2, _ = min(enumerate([f + b for f, b in zip(forward, backward)]), key=lambda x: x[1])

    l_alignment = compute_alignment(str1[:brk1], str2[:brk2], gamma, penalty)
    r_alignment = compute_alignment(str1[brk1:], str2[brk2:], gamma, penalty)
    return l_alignment[0] + r_alignment[0], l_alignment[1] + r_alignment[1]
    
def generate_output(filename, alignment, time, space):
    with open(filename, 'w') as outfile:
        outfile.write(f'{alignment[0][:50]} {alignment[1][:50]}\n')
        outfile.write(f'{alignment[0][-50:]} {alignment[1][-50:]}\n')
        outfile.write(f'{time}\n')
        outfile.write(f'{space}\n')

def compute_cost(str1, str2, gamma, penalty):
    cost = 0
    for i, j in zip(str1, str2):
        if i == '_' or j == '_':
            cost += gamma
        else:
            cost += penalty[i][j]
    return cost  

def main(infile, outfile, gamma, penalty):
    start = perf_counter()
    bases, indices = parse_input(infile)
    str1, str2 = tuple(map(generate_string, bases, indices))
    for s, b, i in zip([str1, str2], bases, indices):
        check_string_length(s, b, i)
    alignment = compute_alignment(str1, str2, gamma, penalty)
    # print('COST:', compute_cost(alignment[0], alignment[1]))
    end = perf_counter()
    space = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    time = end-start
    generate_output(outfile, alignment, time, space)
    return compute_cost(alignment[0], alignment[1], gamma, penalty)

if __name__ == '__main__':
    GAMMA = 30
    PENALTY = {
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
    }
    print(main(argv[1], argv[2], GAMMA, PENALTY))