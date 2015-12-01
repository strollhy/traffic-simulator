# load links
f = open("data/link.csv")
f.readline()

links = {}
for line in f:
    l = line.split(",")
    links[l[0]] = l[1] if l[1] else '200'

# load link2link
f = open("data/link2link.csv")
f.readline()

link2link = []
for line in f:
    l = line.split(",")
    link_id, left, right, through = l[:4]
    if link_id in links:
        res = [link_id]
        cost = links[link_id]
        if left != "0":
            link2link.append(res + [left, cost])
        if right != "0":
            link2link.append(res + [right, cost])
        if through != "0":
            link2link.append(res + [through, cost])

fout = open("data/graph_cost", "w")
fout.write(str(len(link2link)) + "\n\n")
for l2l in link2link:
    fout.write(" ".join(l2l) + "\n")


