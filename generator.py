# Generate lock combo

CORRECT_COMBO = (3, 6, 1)

# Using traditional method
# found_combo = False
# for c1 in range(10):
#     if found_combo:
#         break
#     for c2 in range(10):
#         if found_combo:
#             break
#         for c3 in range(10):
#             if (c1, c2, c3) == CORRECT_COMBO:
#                 print("Found the correct combo: {}".format((c1, c2, c3)))
#                 found_combo = True
#                 break
#             print(c1, c2, c3)

# Using a generator
def combo_gen():
    for c1 in range(10):
        for c2 in range(10):
            for c3 in range(10):
                yield(c1, c2, c3)

for (c1, c2, c3) in combo_gen():
    print(c1, c2, c3)
    if (c1, c2, c3) == CORRECT_COMBO:
        print("Found the combo: {}".format((c1, c2, c3)))
        break