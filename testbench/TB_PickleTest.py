import pickle

# Create dict object
randDict = {
    0 : {
        3 : ((0.123, 1.234), (1.22, 2.22), (3.923,912.1)),
        6 : ((9.8, 5.6), (1.1, 2.3), (9.9, 4.4))
    },
    2 : {
        3 : ((0.132, 9.32), (93.32, 345.4))
    }
}

filename = 'pickle_test'
outfile = open(filename, 'wb')
pickle.dump(randDict, outfile)
outfile.close()

infile = open(filename, 'rb')
newDict = pickle.load(infile)
infile.close()

print(newDict[0])
idx = newDict[0]
print(idx[3])
val = idx[3]
print(val[0])
print(val[0][0])
