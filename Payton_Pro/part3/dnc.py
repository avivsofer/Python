def dnc(baseFunc, combineFunc):
    def divide_and_conquer(arr):
        if len(arr) <= 1:
            return baseFunc(arr[0])
        else:
            mid = len(arr) // 2
            left_half = divide_and_conquer(arr[:mid])
            right_half = divide_and_conquer(arr[mid:])
            return combineFunc(left_half, right_half)

    return divide_and_conquer


def baseFunc(organ):
    value = organ
    return value


def combineFunc(value1, value2):
    valueSum = value1 + value2
    return valueSum


def maxAreaHist(hist):
    def divideAndMax(start, end):
        if start == end:
            return hist[start]
        
        mid = (start + end) // 2
        
        leftMaxArea = divideAndMax(start, mid)
        rightMaxArea = divideAndMax(mid + 1, end)
        
        leftIn, rightIn = mid, mid + 1
        min_height = min(hist[leftIn], hist[rightIn])
        max_area_across = min_height * 2
        
        while leftIn > start or rightIn < end:
            if (rightIn < end and (leftIn == start or hist[rightIn + 1] >= hist[leftIn - 1])):
                rightIn += 1
                min_height = min(min_height, hist[rightIn])
            else:
                leftIn -= 1
                min_height = min(min_height, hist[leftIn])
            max_area_across = max(max_area_across, min_height * (rightIn - leftIn + 1))
        
        return max(leftMaxArea, rightMaxArea, max_area_across)
    
    return divideAndMax(0, len(hist) - 1)
