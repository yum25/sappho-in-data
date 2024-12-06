import re
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def main():
    regex = re.compile('[^a-zA-Z]')
    ignore = [10, 11, 13, 14, 28, 66, 72, 75, 77, 79, 89, 90, 97, 99, 139]
    sets = []

    for i in range(1, 153):
        sets.append(set())
        try:
            with open('analysis/fragments/f{0}.txt'.format(i), 'r') as file:
                lines = file.readlines()

                for line in lines:
                    for word in line.split(' '):
                        cleaned = regex.sub('', word)

                        if len(cleaned) > 0:
                            sets[i - 1].add(cleaned)
        except FileNotFoundError:
            print(f"Skipping {i}, continuing to next fragment...")
    
    matrix = []
    for i in range(0, len(sets)):
        row = []
        for j in range(0, len(sets)):
            row.append(1 - jaccard_similarity(sets[i], sets[j]))
        
        matrix.append(row)
    

    # Create an instance of AgglomerativeClustering
    clustering = AgglomerativeClustering(n_clusters=15, metric="precomputed", linkage='complete')

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
    
    print(clusters)

    with open('analysis/clusters.json', 'w') as f:
        f.write(str(clusters))


    wordsets = []
    for i in range(0, len(sets)):
        wordsets.append(list(sets[i]))

    with open('analysis/sets.json', 'w') as f:
        f.write(str(wordsets))

    


def jaccard_similarity(setA, setB):
    # intersection of two sets
    intersection = len(setA.intersection(setB))
    # Unions of two sets

    union = len(setA.union(setB))

    if union == 0:
        return 0

    return intersection / union

if __name__ == "__main__":
    main()