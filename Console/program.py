# arr = [7, 9, 11, 12, 5]
arr = [15, 18, 2, 3, 6, 12]
left, size, right, i = 0, len(arr), len(arr) - 1, 1

print(f"arr =", arr)

while left <= right:
    print(f"\nFor left = {left} & right = {right}, iteration #{i}")
    i += 1

    condition = arr[left] <= arr[right]
    print(f"arr[left] <= arr[right] -> {condition} (return left)")
    if condition:
        print("\n\nOutput:", left)
        break

    mid: int = int(left + (right - left) / 2)
    print(f"mid =", mid)

    next: int = (mid + 1) % size
    print(f"next =", next)

    prev: int = (mid - 1 + size) % size
    print(f"prev =", prev)

    condition = arr[mid] <= arr[next] and arr[mid] <= arr[prev]
    print(f"arr[mid] <= arr[next] && arr[mid] <= arr[prev] -> {condition} (return mid)")
    if condition:
        print("\n\nOutput:", mid)
        break

    condition = arr[mid] >= arr[left]
    print(f"arr[mid] >= arr[left] -> {condition} -> ", end='')
    if condition:
        left = mid + 1
        print("left = mid + 1")
    else:
        right = mid - 1
        print("right = mid - 1")