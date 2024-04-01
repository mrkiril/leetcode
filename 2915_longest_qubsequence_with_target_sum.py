from math import inf


class Solution:
    def lengthOfLongestSubsequence(self, nums: list[int], target: int) -> tuple[dict[int, int | float], dict[int, [int]]]:
        n = len(nums)
        f = [[-inf] * (target + 1) for _ in range(2 * n + 1)]
        f[0][0] = 0

        # key: sum, value: last_index,
        target_last_indexes = {k: [] for k in range(target + 1)}

        for i in range(1, 2 * n + 1):
            if i > n:
                x = nums[i - n - 1]
            else:
                x = nums[i - 1]

            for j in range(target + 1):
                prev_row_index = i - 1
                f[i][j] = f[prev_row_index][j]
                if j >= x:
                    new_len = max(f[i][j], f[prev_row_index][j - x] + 1)
                    if f[i][j] < new_len and (
                        prev_row_index in target_last_indexes[j - x]
                        or not target_last_indexes[j - x]
                    ):
                        target_last_indexes[j] = [i]
                        f[i][j] = new_len
                    elif (
                        f[i][j] == new_len and new_len > 0
                        and (
                            (new_len >= 2 and prev_row_index in target_last_indexes[j - x])
                            or (new_len == 1 and x == j)
                        )
                    ):
                        target_last_indexes[j].append(i)

        return (
            {
                index: f[-1][index]
                for index in range(target//2, target + 1)
                if f[-1][index] > 0
            },
            {
                k: v
                for k, v in target_last_indexes.items()
                if target // 2 <= k <= target
            }
        )


def get_num_list(num_list: list[int], f_index: int, l_index: int) -> list[int]:
    n = len(num_list)
    response_list = []
    for index in range(f_index, l_index):
        if index >= n:
            val = nums[index - n]
        else:
            val = nums[index]
        response_list.append(val)
    return response_list


if __name__ == '__main__':
    nums = [5, 5, 1, 1, 3, 4]
    print("= = = = = = = = = = = = = = = = = = ")
    print(f"nums: {nums}")
    m = 7
    target = 2 * m
    solution = Solution()
    len_dict, last_index_dict = solution.lengthOfLongestSubsequence(nums, target)
    for target_value, length in len_dict.items():
        last_index_value = last_index_dict[target_value][0]
        first_index_value = last_index_value - length
        final_list = get_num_list(nums, first_index_value, last_index_value)
        print(f"target_value: {target_value}, length: {length} -> {final_list}")

