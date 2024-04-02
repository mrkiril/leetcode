from math import inf
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TargetResp:
    target_value: int
    num_list: list[int]

    def __eq__(self, other):
        return self.target_value == other.target_value and self.num_list == other.num_list


def get_num_list(num_list: list[int], f_index: int, l_index: int) -> list[int]:
    n = len(num_list)
    response_list = []
    for index in range(f_index, l_index):
        if index >= n:
            val = num_list[index - n]
        else:
            val = num_list[index]
        response_list.append(val)
    return response_list


class Solution:
    def lengthOfLongestSubsequence(
        self, nums: list[int], target: int
    ) -> list[TargetResp]:
        n = len(nums)
        table_len = 2 * n + 1
        f = [[-inf] * (target + 1) for _ in range(table_len)]
        f[0][0] = 0

        # key: sum, value: last_index,
        target_last_indexes = {k: [] for k in range(target + 1)}

        for i in range(1, table_len):
            if i > n:
                x = nums[i - n - 1]
            else:
                x = nums[i - 1]

            for j in range(target + 1):
                prev_row_index = i - 1
                f[i][j] = f[prev_row_index][j]
                if j >= x:
                    previous_len = f[prev_row_index][j - x] + 1
                    new_len = max(f[i][j], previous_len)
                    if f[i][j] < new_len and (
                        prev_row_index in target_last_indexes[j - x]
                        or not target_last_indexes[j - x]
                    ):
                        target_last_indexes[j] = [i]
                        f[i][j] = new_len
                    elif (
                        f[i][j] == previous_len and previous_len > 0
                        and (
                            (previous_len >= 2 and prev_row_index in target_last_indexes[j - x])
                            or (previous_len == 1 and x == j)
                        )
                    ):
                        target_last_indexes[j].append(i)

        len_dict = {
            index: f[-1][index]
            for index in range(target//2, target + 1)
            if f[-1][index] > 0
        }
        last_index_dict = {
            k: v
            for k, v in target_last_indexes.items()
            if target // 2 <= k <= target
        }
        resp_list = []
        for target_value, length in len_dict.items():
            for last_index_value in last_index_dict[target_value]:
                # last_index_value = last_index_dict[target_value][0]
                first_index_value = last_index_value - length
                final_list = get_num_list(nums, first_index_value, last_index_value)
                resp_list.append(
                    TargetResp(target_value=target_value, num_list=final_list)
                )
        return resp_list


if __name__ == '__main__':
    nums = [1, 1, 1, 1, 1, 1, 1, 2, 1]

    print("= = = = = = = = = = = = = = = = = = ")
    print(f"nums: {nums}")
    m = 4
    target = 2 * m
    solution = Solution()
    target_resp_list = solution.lengthOfLongestSubsequence(nums, target)
    for t in target_resp_list:
        print(f"target_value: {t.target_value}, length: {len(t.num_list)} -> {t.num_list}")
