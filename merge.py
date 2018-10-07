import csv


filenames = ['asin2.csv', 'asin1.csv']
with open('out.csv', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
