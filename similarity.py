from preprocess import haversine

def DTWDistance(t1, t2):
    n = len(t1)
    m = len(t2)
    dtw = [[None for i in range(m+1)] for j in range(n+1)]
    for i in range(1,n+1):
        dtw[i][0] = float('inf')
    for i in range(1,m+1):
        dtw[0][i] = float('inf')
    dtw[0][0] = 0
    print(dtw)
    for i in range(1,n+1):
        for j in range(1,m+1):
            point1 = t1[i-1]
            point2 = t2[j-1]
            lon1 = point1[1]
            lat1 = point1[2]
            lon2 = point2[1]
            lat2 = point2[2]
            cost = haversine(lon1, lat1, lon2, lat2)
            dtw[i][j] = cost + min(dtw[i-1][j], dtw[i][j-1], dtw[i-1][j-1])
    print(dtw)
    return dtw[n][m]

print(DTWDistance([[1,2,3], [2,3,4], [3,4,5]], [[1,5,6], [2,6,7], [3,7,8]]))