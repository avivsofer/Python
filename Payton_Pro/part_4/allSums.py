def allSumsDP(arr):
    dp = [[False] * (sum(arr) + 1) for _ in range(len(arr) + 1)]
    dp[0][0] = True

    for i in range(1, len(arr) + 1):
        for j in range(sum(arr) + 1):
            dp[i][j] = dp[i-1][j] or (arr[i-1] <= j and dp[i-1][j-arr[i-1]])
    
    theSet = set()
    for j in range(sum(arr) + 1):
        if dp[len(arr)][j]:
            theSet.add(j)

    return theSet
