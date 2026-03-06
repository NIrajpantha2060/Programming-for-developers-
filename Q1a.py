# question no 1 a
from math import gcd
from collections import defaultdict

def maxPoints(customer_locations):
    """
    Find maximum number of customer homes on the same straight line.
    
    Args:
        customer_locations: List of [x, y] coordinates
        
    Returns:
        Maximum number of collinear points
    """
    n = len(customer_locations)
    if n <= 2:
        return n

    result = 0

    for i in range(n):
        slope_count = defaultdict(int)
        same_point = 0
        max_slope_points = 0

        x1, y1 = customer_locations[i]

        for j in range(i + 1, n):
            x2, y2 = customer_locations[j]
            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:
                # Same point
                same_point += 1
            else:
                # Normalize slope using GCD
                g = gcd(dx, dy)
                dx //= g
                dy //= g
                
                # Normalize sign: ensure dx is always positive
                # This prevents (1,1) and (-1,-1) being treated as different
                if dx < 0:
                    dx = -dx
                    dy = -dy
                
                slope_count[(dx, dy)] += 1
                max_slope_points = max(max_slope_points, slope_count[(dx, dy)])

        result = max(result, max_slope_points + same_point + 1)

    return result

def main():
    # Example 1: All points on diagonal line
    customer_locations = [[1, 1], [2, 2], [3, 3]]
    result1 = maxPoints(customer_locations)
    print("Maximum customers covered (Example 1):", result1)
    
    # Example 2: Complex placement
    customer_locations = [[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]
    result2 = maxPoints(customer_locations)
    print("Maximum customers covered (Example 2):", result2)

if __name__ == "__main__":
    main()