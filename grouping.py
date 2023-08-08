from collections import defaultdict

foos = [
    ["Bydel1", ["foo", "hei på deg"]],
    ["Bydel2", ["bar", "hei hei"]],
    ["Bydel1", ["baz", "hallo"]],
    # ... andre data
]

# Group by 'bydel'
grouped_by_bydel = defaultdict(list)
for foo in foos:
    grouped_by_bydel[foo[0]].append(foo)

# Group by 'kommentar' and count
grouped_and_counted = defaultdict(int)
for foo in foos:
    words = foo[1][1].split()
    for word in words:
        grouped_and_counted[word] += 1

print(dict(grouped_by_bydel))
print(dict(grouped_and_counted))
