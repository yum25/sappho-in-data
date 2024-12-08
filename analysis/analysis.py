import re
import copy
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def jaccard_similarity(setA, setB):
    # intersection of two sets
    intersection = len(setA.intersection(setB))
    # Unions of two sets

    union = len(setA.union(setB))

    if union == 0:
        return 0

    return intersection / union

def main():
    regex = re.compile('[^a-zA-Z]')
    ignore = [10, 11, 13, 14, 28, 66, 72, 75, 77, 79, 89, 90, 97, 99, 139, 171, 178]
    sets = []

    for i in range(1, 193):
        sets.append(set())
        try:
            with open('analysis/fragments/f{0}.txt'.format(i), 'r') as file:
                lines = file.readlines()

                for line in lines:
                    for word in line.split(' '):
                        
                        cleaned = regex.sub('', word).lower()

                        if len(cleaned) > 0:
                            sets[i - 1].add(cleaned)

                        
        except FileNotFoundError:
            print(f"Skipping {i}, continuing to next fragment...")
    
    matrix = []
    for i in range(0, len(sets)):
        row = []
        for j in range(0, len(sets)):
            row.append(jaccard_similarity(sets[i], sets[j]))
        
        matrix.append(row)
    

    # Create an instance of AgglomerativeClustering
    clustering = AgglomerativeClustering(n_clusters=15, linkage='ward')

    # Fit the model to the data
    clustering.fit(np.array(matrix))

    # Get the cluster labels
    labels = clustering.labels_

    clusters = {}

    for i in range(0, len(labels)):
        label = int(labels[i])

        if i + 1 not in ignore:
            if clusters.get(label, None) == None:
                clusters[label] = [i + 1]
            else:
                clusters[label].append(i + 1)

    i = 1
    hierarchy = {}
   
    while (i < 193):
        if i in ignore:
            i += 1
            continue

        fragment = { "name": i, "group": int(labels[i - 1]), "size": len(sets[i - 1])}

        if hierarchy.get(fragment["group"], None) == None:
            hierarchy[fragment["group"]] = { "name": fragment["group"], "children": [fragment]}
        else:
            hierarchy[fragment["group"]]["children"].append(fragment)

        i += 1

    with open('analysis/hierarchy.json', 'w') as f:
        hierarchy = {"name": "data", "children": list(hierarchy.values())} 
        f.write(str(hierarchy))



if __name__ == "__main__":
    main()