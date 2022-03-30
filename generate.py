import random

TEST_CASES = 7000
FILEPATH = '../inputs/'

def generate_permutations(chars, perm, perms, length):
    if length == 0:
        perms.append(perm)
        return
    for idx, char in enumerate(chars):
        generate_permutations(chars[:idx] + chars[idx+1:], char + perm, perms, length - 1)
    return perms

def write_generate_sequence(file, base, indices):
    file.write(base + '\n')
    for i in indices:
        file.write(str(i) + '\n')

chars = ['A', 'G', 'C', 'T']
perms = generate_permutations(chars, '', [], 4)
sizes = []

for case in range(TEST_CASES):
    b1, b2 = random.choice(perms), random.choice(perms)
    l1, l2 = random.randint(1, 10), random.randint(1, 10)
    s1, s2 = (2 ** l1) * 4, (2 ** l2) * 4
    i1, i2 = [random.randint(0, (4 * (2 ** l)) - 1) for l in range(l1)], [random.randint(0, (4 * (2 ** l)) - 1) for l in range(l2)]
    with open(f'{FILEPATH}input{case}.txt', 'w') as outfile:
        write_generate_sequence(outfile, b1, i1)
        write_generate_sequence(outfile, b2, i2)
    sizes.append((s1, s2))

with open(f'{FILEPATH}sizes.txt', 'w') as outfile:
    for s1, s2 in sizes:
        outfile.write(str(s1 + s2) + '\n')
    
