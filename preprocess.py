from glob import glob
import os.path

PROCESSED_POSTFIX = '_preprocessed.txt'

# turn (a, b) & (b, a) entries to just (a, b)
def dedupe_undirected_and_remove_comments():
    inputs = glob(os.path.join("data", "*.txt"))
    for filename in inputs:
        if PROCESSED_POSTFIX in filename:
            continue
        with open(filename) as f:
            print(f'Prerocessing {filename}')
            lines = f.readlines()
            lines = filter(lambda l: not l.startswith('#'), lines)
            edges = sorted(list(set(map(lambda l: tuple(sorted(l.split())), lines))))
            outname = filename.replace('.txt', PROCESSED_POSTFIX)
            with open(outname, 'w') as o:
                edge_list = map(lambda pair: '\t'.join(pair), edges)
                o.write('\n'.join(edge_list))


if __name__ == '__main__':
    dedupe_undirected_and_remove_comments()
