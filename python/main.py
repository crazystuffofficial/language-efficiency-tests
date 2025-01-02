import time

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

if __name__ == "__main__":
    arr = [
  2493, 3089, 4076, 2354, 4385, 9309, 5987, 2407, 6149, 8951,
  7715, 7609, 9864, 7420, 6692, 9011, 3282, 9822, 7787, 4461,
  6098, 5515, 5989, 7242, 7007, 3149, 1009, 3088, 6177, 5209,
  6815, 6491, 6125, 1888, 2065, 2052, 2597, 1579, 2869, 1847,
  6895, 9140, 8321, 3625, 6234, 9241, 9441, 1209, 4673, 1533,
  6590, 8994, 8453, 6578, 2842, 8923, 1385, 1337, 6868, 7384,
  2439, 4510, 6260, 7322, 6883, 9356, 2134, 1874, 7551, 5615,
  2094, 3098, 9007, 8015, 3421, 1108, 7987, 7775, 5797, 9885,
  7244, 6582, 1395, 4448, 3678, 2056, 3640, 7017, 8298, 1217,
  4323, 6315, 8128, 6607, 4422, 2227, 7959, 7200, 5320, 7075,
  9018, 1192, 1746, 1151, 7309, 4317, 1257, 2770, 9513, 7159,
  5593, 7747, 7593, 2677, 6284, 4245, 4367, 2145, 6429, 3144,
  4396, 8291, 3097, 3301, 6195, 5578, 1742, 5770, 3370, 9692,
  4519, 8082, 4690, 8317, 3021, 6192, 2628, 8399, 7303, 1419,
  8747, 2626, 1264, 5757, 7990, 3229, 1223, 6624, 6972, 1293,
  4853, 2460, 1662, 6093, 6994, 1799, 1837, 7750, 6651, 2165,
  2224, 2689, 2690, 7564, 5633, 7735, 1336, 1443, 4321, 7169,
  2068, 7882, 7055, 1150, 7181, 4468, 5420, 3062, 2090, 5864,
  3837, 9630, 1593, 4940, 5488, 7306, 4473, 5452, 1229, 9982,
  3254, 3394, 3042, 2495, 2749, 4051, 7607, 2824, 2319, 9062,
  1354, 7616, 4183, 4981, 4947, 3565, 2559, 6941, 4334, 9544,
  8761, 2661, 5429, 2630, 2799, 4783, 6449, 3585, 1891, 7190,
  7128, 1043, 2888, 6671, 6931, 8456, 3809, 9649, 6595, 9350,
  8884, 3479, 2488, 9995, 5384, 2012, 4926, 1677, 2040, 6099,
  2762, 8459, 2790, 7483, 2249, 2311, 2525, 9935, 2923, 1899,
  1687, 2445, 9035, 4109, 3853, 9490, 5662, 5818, 7011, 1454,
  5667, 8499, 7681, 7535, 1458, 4879, 5147, 3161, 8048, 1283,
  6120, 9750, 5947, 8812, 6238, 7574, 9190, 7881, 1232, 6812,
  9264, 7054, 7972, 7732, 5779, 3011, 7818, 3125, 4462, 2323,
  7441, 5739, 8275, 5055, 3191, 4101, 4961, 5985, 7779, 1260,
  9328, 7645, 9321, 4679, 6493, 3902, 5941, 7024, 8255, 9699,
  1208, 6173, 6124, 7477, 2310, 1165, 8709, 8257, 6884, 6319,
  9705, 9326, 9472, 1554, 8209, 9065, 6186, 1300, 3794, 4444,
  4791, 6443, 2067, 4413, 6519, 6779, 2691, 2494, 8929, 4249,
  7914, 5938, 9074, 9839, 5602, 7949, 2061, 3387, 3443, 3972,
  2922, 5194, 3743, 3384, 3649, 2798, 3580, 9814, 4579, 3038,
  5042, 7429, 3540, 7806, 2755, 3041, 2229, 3006, 2111, 9764
]

    start_time = time.time()
    for i in range(1000):
        bubble_sort(arr)
    end_time = time.time()
    print("Sorted array:", arr)
    print("Execution time:", end_time - start_time)