import subprocess as sp

TEST_CASES = 7000

results = []
for case in range(TEST_CASES):
    infile = f'../inputs/input{case}.txt'
    basic_outfile = f'../outputs/basic/output{case}.txt'
    efficient_outfile = f'../outputs/efficient/output{case}.txt'
    b = int(sp.run(['python3', 'basic.py', infile, basic_outfile], capture_output=True).stdout)
    e = int(sp.run(['python3', 'efficient.py', infile, efficient_outfile], capture_output=True).stdout)
    results.append(b == e)
    print('Completed CASE #', case + 1)

with open('../outputs/results.txt', 'w') as outfile:
    outfile.writelines(map(lambda x: x+'\n', map(str, results)))

print(f'ACCURACY: {sum(list(map(int, results))) / len(results)}')
