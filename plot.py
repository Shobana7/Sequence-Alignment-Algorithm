import matplotlib.pyplot as plt

TEST_CASES = 7000
memory = []
time = []

with open('../inputs/sizes.txt') as sizes:
    size = list(map(int, sizes.readlines()))

for type in ['basic', 'efficient']:
    memories, times = [], []
    for case in range(TEST_CASES):
        with open(f'../outputs/{type}/output{case}.txt') as infile:
            lines = infile.readlines()
            times.append(float(lines[2]))
            memories.append(float(int(lines[3])/1024))
    memory.append(memories)
    time.append(times)

plt.rcParams["figure.figsize"] = (20,5)

plt.subplot(121)
plt.scatter(size, memory[0], c='#f9dc5c', marker='x')
plt.scatter(size, memory[1], c='#69a197', marker='+')
plt.xlabel('SIZE')
plt.ylabel('MEMORY')

plt.subplot(122)
plt.scatter(size, time[0], c='#f9dc5c', marker='x')
plt.scatter(size, time[1], c='#69a197', marker='+')
plt.xlabel('SIZE')
plt.ylabel('TIME')

# smt = [list(zip(size, memory[0], time[0])), list(zip(size, memory[1], time[1]))]
# smt[0].sort(key=lambda x: x[0])
# smt[1].sort(key=lambda x: x[0])

# size = []
# memory = [[], []]
# time = [[],[]]
# for s, m, t in smt[0]:
#     size.append(s)
#     memory[0].append(m)
#     time[0].append(t)

# for s, m, t in smt[1]:
#     memory[1].append(m)
#     time[1].append(t)

# plt.subplot(121)
# plt.plot(size, memory[0], c='#f9dc5c')
# plt.plot(size, memory[1], c='#69a197')
# plt.xlabel('SIZE')
# plt.ylabel('MEMORY')

# plt.subplot(122)
# plt.plot(size, time[0], c='#f9dc5c')
# plt.plot(size, time[1], c='#69a197')
# plt.xlabel('SIZE')
# plt.ylabel('TIME')

plt.savefig('../plots/plot6-7000.png', bbox_inches='tight')
