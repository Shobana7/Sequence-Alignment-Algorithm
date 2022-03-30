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

def compute_memo(str1, str2, gamma, penalty):  
    m = len(str1)
    n = len(str2)
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
    memo = compute_memo(str1, str2, gamma, penalty)
    # print('COST:', memo[-1][-1])
    alignment = track_memo(memo, str1, str2, gamma, penalty)
    return memo[-1][-1], alignment

def generate_output(filename, alignment, time, space):
    with open(filename, 'w') as outfile:
        outfile.write(f'{alignment[0][:50]} {alignment[1][:50]}\n')
        outfile.write(f'{alignment[0][-50:]} {alignment[1][-50:]}\n')
        outfile.write(f'{time}\n')
        outfile.write(f'{space}\n')   
         

def main(infile, outfile, gamma, penalty):
    start = perf_counter()
    bases, indices = parse_input(infile)
    str1, str2 = tuple(map(generate_string, bases, indices))
    for s, b, i in zip([str1, str2], bases, indices):
        check_string_length(s, b, i)
    cost, alignment = compute_alignment(str1, str2, gamma, penalty)
    end = perf_counter()
    space = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    time = end-start
    generate_output(outfile, alignment, time, space)
    return cost


if __name__ == '__main__':
    GAMMA = 30
    PENALTY = {
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
    }
    print(main(argv[1], argv[2], GAMMA, PENALTY))