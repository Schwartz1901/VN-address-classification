# -*- coding: utf-8 -*-
"""Group2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nL5B06qpgS_g4IWstFl4PPtA7fIgo3Op
"""

# NOTE: you CAN change this cell
# If you want to use your own database, download it here
# !gdown ...

# Provided text files
# !gdown --fuzzy https://drive.google.com/file/d/1oSXQHLoVSGfBOLR4NjNwQRTkDb8Zd8OU/view?usp=drive_link -O list_province.txt
# !gdown --fuzzy https://drive.google.com/file/d/18sZoDAqJWyUfmjQN3VpKfkDHFQ-tcml6/view?usp=drive_link -O list_district.txt
# !gdown --fuzzy https://drive.google.com/file/d/1VfDCj7R11jf3SIZyoZdYL7fIN-AIhC-1/view?usp=drive_link -O list_ward.txt

# Self - generated text files
!gdown --fuzzy https://drive.google.com/file/d/1STd4s-soelFToo67ejTNwFgA4ooErcuf/view?usp=sharing -O list_province.txt
!gdown --fuzzy https://drive.google.com/file/d/16XmmpcCAAwZkcKlxhzSHErIHf2P9i10g/view?usp=sharing -O list_district.txt
!gdown --fuzzy https://drive.google.com/file/d/1x_vEugEAWgGEg-2rdKcGvj14HfxfEsXr/view?usp=sharing -O list_ward.txt

# NOTE: you CAN change this cell
# Add more to your needs
# you must place ALL pip install here
!pip install editdistance

# NOTE: you CAN change this cell
# import your library here

import editdistance
import re
from collections import deque
from itertools import combinations


# NOTE: you MUST change this cell
# New methods / functions must be written under class Solution.

class Solution:
    def __init__(self):
        # list provice, district, ward for private test, do not change for any reason (these file will be provided later with this exact name)

        self.province_path = 'list_province.txt'
        self.district_path = 'list_district.txt'
        self.ward_path = 'list_ward.txt'

        self.province_trie = MyTrie()
        self.district_trie = MyTrie()
        self.ward_trie = MyTrie()


        self._create_trie(self.province_path, self.province_trie)
        self._create_trie(self.district_path, self.district_trie)
        self._create_trie(self.ward_path, self.ward_trie)

       #     write your preprocess here, add more method if needed
    def _segment(self, s: str):
        ### Case 1: String contain "," as a delimiter
        if (',' in s):
            s = s.split(',')
            s = [x.strip() for x in s]
            return s
        ### Case 2: String contain "." as a delimiter:
        elif ('.' in s):
            s = s.split('.')
            s = [x.strip() for x in s]
            return s
        ### Case 3: String contain " " as a delimiter:
        else:
            # push a whole string into a list for the same output
            s = [s]
            return s

    def _seperate(self, s: str):
        # s = [re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', x) for x in s]
        # s = [re.sub(r'([a-z])([A-Z])', r'\1 \2', x) for x in s]
        s = [re.sub(r'([a-zA-Z])(?=[A-Z])', r'\1 ', x) for x in s]

        s = [re.sub(r'\.', ' ', x) for x in s]
        s = [re.sub(r'tp\.?', '', x, flags=re.IGNORECASE) for x in s]

        # s = [re.sub(r't\.?', '', x, flags=re.IGNORECASE) for x in s]
        # s = [re.sub(r'h\.?', '', x, flags=re.IGNORECASE) for x in s]
        return s

    def _handle_prefix(self, s: str):
        full_prefix = ['xã', 'thị trấn', 'phường', 'thị xã', 'huyện', 'tỉnh', 'thành phố']
        regex = r'\b(' + '|'.join(full_prefix) + r')\.?\s*(?=[A-Za-z0-9])'
        s = re.sub(regex, '', s, flags=re.IGNORECASE).strip()
        return s

    def _generate_combination(self, s, max_com = 5):
        words = s.split()
        combinations = []
        for length in range(2, max_com + 1):
            for i in range(len(words) - length + 1):
                combination = ' '.join(words[i:i + length])
                combinations.append(combination)
        return combinations

        # Open Dataset
    def _create_trie(self, dataset, trie):
          with open(dataset, "r", encoding="utf-8") as file:
              for line in file:
                  line = line.strip()
                  trie.insert(line)

    def _count_words(self, s: str):
        """Count the number of words in a string."""
        return len(s.split())


    def process(self, s: str):
        # Pre-process string
        processed_str = self._seperate(self._segment(self._handle_prefix(s)))

        # Initialize result dictionary
        result = {"province": "", "district": "", "ward": ""}

        # Early return if string is empty or too short
        if not processed_str or len(processed_str) < 1:
            return {"cleaned_string": processed_str, **result}

        # Reverse once and work with list directly
        address_parts = list(reversed(processed_str))

        # Store matches with their distances
        matches = {
            "province": [],
            "district": [],
            "ward": []
        }

        # Process each address part
        for address in address_parts:
            word_count = self._count_words(address)
            if word_count <= 1:
                continue

            # Optimize combination generation
            combinations = (self._generate_combination(address, word_count)
                        if word_count < 5
                        else self._generate_combination(address))

            # Search tries in a single pass
            for combo in combinations:
                for area_type, trie in [("province", self.province_trie),
                                    ("district", self.district_trie),
                                    ("ward", self.ward_trie)]:
                    if match := trie.search_closest(combo):
                        distance = editdistance.eval(combo, match)
                        matches[area_type].append((match, distance))
                        break  # Move to next combination once matched

        # Find best matches with minimum edit distance
        for area_type in ["province", "district", "ward"]:
            if matches[area_type]:
                result[area_type] = min(matches[area_type], key=lambda x: x[1])[0]

        return result
    
### Trie Class
class MyTrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False  # Will store the actual word when true

class MyTrie:
    def __init__(self):
        self.root = MyTrieNode()

    def insert(self, word):
        """Insert a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = MyTrieNode()
            node = node.children[char]
        node.is_word = word  # Store the complete word at the end node

    def _collect_words_from_node(self, node, prefix, words, max_words=100):
        """Collect words efficiently using BFS with a limit."""
        queue = deque([(node, prefix)])
        collected = 0

        while queue and collected < max_words:
            current_node, current_prefix = queue.popleft()
            if current_node.is_word:
                words.append(current_prefix)
                collected += 1

            for char, child in current_node.children.items():
                queue.append((child, current_prefix + char))

    def search_closest(self, query, max_distance=2):
        """Find the closest word to query within max_distance edits."""
        if not query:
            return None

        # Check for exact match
        node = self.root
        prefix = ""
        for char in query:
            if char not in node.children:
                break
            node = node.children[char]
            prefix += char
        else:  # Only executes if loop completes without breaking
            if node.is_word:
                return prefix

        # Collect candidate words efficiently
        candidate_words = []
        self._collect_words_from_node(node, prefix, candidate_words)

        # If no candidates found from current node, search from root
        if not candidate_words:
            self._collect_words_from_node(self.root, "", candidate_words)

        if not candidate_words:
            return None

        # Find closest word with early termination
        min_distance = float('inf')
        closest_word = None

        for word in candidate_words:
            if word == query:  # Skip exact match (already checked)
                continue
            distance = editdistance.eval(query, word)
            if distance < min_distance:
                min_distance = distance
                closest_word = word
            if min_distance == 1:  # Can't get better than distance 1
                break

        # Return result based on criteria
        return (closest_word
                if (closest_word and
                    min_distance <= max_distance and
                    not closest_word.isdigit())
                else None)   

# NOTE: DO NOT change this cell
# This cell is for downloading private test
!rm -rf test.json
# this link is public test
!gdown --fuzzy https://drive.google.com/file/d/1PBt3U9I3EH885CDhcXspebyKI5Vw6uLB/view?usp=sharing -O test.json

# CORRECT TESTS
groups_province = {}
groups_district = {'hòa bình': ['Hoà Bình', 'Hòa Bình'], 'kbang': ['Kbang', 'KBang'], 'quy nhơn': ['Qui Nhơn', 'Quy Nhơn']}
groups_ward = {'ái nghĩa': ['ái Nghĩa', 'Ái Nghĩa'], 'ái quốc': ['ái Quốc', 'Ái Quốc'], 'ái thượng': ['ái Thượng', 'Ái Thượng'], 'ái tử': ['ái Tử', 'Ái Tử'], 'ấm hạ': ['ấm Hạ', 'Ấm Hạ'], 'an ấp': ['An ấp', 'An Ấp'], 'ẳng cang': ['ẳng Cang', 'Ẳng Cang'], 'ẳng nưa': ['ẳng Nưa', 'Ẳng Nưa'], 'ẳng tở': ['ẳng Tở', 'Ẳng Tở'], 'an hòa': ['An Hoà', 'An Hòa'], 'ayun': ['Ayun', 'AYun'], 'bắc ái': ['Bắc ái', 'Bắc Ái'], 'bảo ái': ['Bảo ái', 'Bảo Ái'], 'bình hòa': ['Bình Hoà', 'Bình Hòa'], 'châu ổ': ['Châu ổ', 'Châu Ổ'], 'chư á': ['Chư á', 'Chư Á'], 'chư rcăm': ['Chư Rcăm', 'Chư RCăm'], 'cộng hòa': ['Cộng Hoà', 'Cộng Hòa'], 'cò nòi': ['Cò  Nòi', 'Cò Nòi'], 'đại ân 2': ['Đại Ân  2', 'Đại Ân 2'], 'đak ơ': ['Đak ơ', 'Đak Ơ'], "đạ m'ri": ["Đạ M'ri", "Đạ M'Ri"], 'đông hòa': ['Đông Hoà', 'Đông Hòa'], 'đồng ích': ['Đồng ích', 'Đồng Ích'], 'hải châu i': ['Hải Châu  I', 'Hải Châu I'], 'hải hòa': ['Hải Hoà', 'Hải Hòa'], 'hành tín đông': ['Hành Tín  Đông', 'Hành Tín Đông'], 'hiệp hòa': ['Hiệp Hoà', 'Hiệp Hòa'], 'hòa bắc': ['Hoà Bắc', 'Hòa Bắc'], 'hòa bình': ['Hoà Bình', 'Hòa Bình'], 'hòa châu': ['Hoà Châu', 'Hòa Châu'], 'hòa hải': ['Hoà Hải', 'Hòa Hải'], 'hòa hiệp trung': ['Hoà Hiệp Trung', 'Hòa Hiệp Trung'], 'hòa liên': ['Hoà Liên', 'Hòa Liên'], 'hòa lộc': ['Hoà Lộc', 'Hòa Lộc'], 'hòa lợi': ['Hoà Lợi', 'Hòa Lợi'], 'hòa long': ['Hoà Long', 'Hòa Long'], 'hòa mạc': ['Hoà Mạc', 'Hòa Mạc'], 'hòa minh': ['Hoà Minh', 'Hòa Minh'], 'hòa mỹ': ['Hoà Mỹ', 'Hòa Mỹ'], 'hòa phát': ['Hoà Phát', 'Hòa Phát'], 'hòa phong': ['Hoà Phong', 'Hòa Phong'], 'hòa phú': ['Hoà Phú', 'Hòa Phú'], 'hòa phước': ['Hoà Phước', 'Hòa Phước'], 'hòa sơn': ['Hoà Sơn', 'Hòa Sơn'], 'hòa tân': ['Hoà Tân', 'Hòa Tân'], 'hòa thuận': ['Hoà Thuận', 'Hòa Thuận'], 'hòa tiến': ['Hoà Tiến', 'Hòa Tiến'], 'hòa trạch': ['Hoà Trạch', 'Hòa Trạch'], 'hòa vinh': ['Hoà Vinh', 'Hòa Vinh'], 'hương hòa': ['Hương Hoà', 'Hương Hòa'], 'ích hậu': ['ích Hậu', 'Ích Hậu'], 'ít ong': ['ít Ong', 'Ít Ong'], 'khánh hòa': ['Khánh Hoà', 'Khánh Hòa'], 'krông á': ['Krông Á', 'KRông á'], 'lộc hòa': ['Lộc Hoà', 'Lộc Hòa'], 'minh hòa': ['Minh Hoà', 'Minh Hòa'], 'mường ải': ['Mường ải', 'Mường Ải'], 'mường ẳng': ['Mường ẳng', 'Mường Ẳng'], 'nậm ét': ['Nậm ét', 'Nậm Ét'], 'nam hòa': ['Nam Hoà', 'Nam Hòa'], 'na ư': ['Na ư', 'Na Ư'], 'ngã sáu': ['Ngã sáu', 'Ngã Sáu'], 'nghi hòa': ['Nghi Hoà', 'Nghi Hòa'], 'nguyễn úy': ['Nguyễn Uý', 'Nguyễn úy', 'Nguyễn Úy'], 'nhân hòa': ['Nhân Hoà', 'Nhân Hòa'], 'nhơn hòa': ['Nhơn Hoà', 'Nhơn Hòa'], 'nhơn nghĩa a': ['Nhơn nghĩa A', 'Nhơn Nghĩa A'], 'phúc ứng': ['Phúc ứng', 'Phúc Ứng'], 'phước hòa': ['Phước Hoà', 'Phước Hòa'], 'sơn hóa': ['Sơn Hoá', 'Sơn Hóa'], 'tạ an khương đông': ['Tạ An Khương  Đông', 'Tạ An Khương Đông'], 'tạ an khương nam': ['Tạ An Khương  Nam', 'Tạ An Khương Nam'], 'tăng hòa': ['Tăng Hoà', 'Tăng Hòa'], 'tân hòa': ['Tân Hoà', 'Tân Hòa'], 'tân hòa thành': ['Tân Hòa  Thành', 'Tân Hòa Thành'], 'tân khánh trung': ['Tân  Khánh Trung', 'Tân Khánh Trung'], 'tân lợi': ['Tân lợi', 'Tân Lợi'], 'thái hòa': ['Thái Hoà', 'Thái Hòa'], 'thiết ống': ['Thiết ống', 'Thiết Ống'], 'thuận hòa': ['Thuận Hoà', 'Thuận Hòa'], 'thượng ấm': ['Thượng ấm', 'Thượng Ấm'], 'thụy hương': ['Thuỵ Hương', 'Thụy Hương'], 'thủy xuân': ['Thuỷ Xuân', 'Thủy Xuân'], 'tịnh ấn đông': ['Tịnh ấn Đông', 'Tịnh Ấn Đông'], 'tịnh ấn tây': ['Tịnh ấn Tây', 'Tịnh Ấn Tây'], 'triệu ái': ['Triệu ái', 'Triệu Ái'], 'triệu ẩu': ['Triệu ẩu', 'Triệu Ẩu'], 'trung hòa': ['Trung Hoà', 'Trung Hòa'], 'trung ý': ['Trung ý', 'Trung Ý'], 'tùng ảnh': ['Tùng ảnh', 'Tùng Ảnh'], 'úc kỳ': ['úc Kỳ', 'Úc Kỳ'], 'ứng hòe': ['ứng Hoè', 'Ứng Hoè'], 'vĩnh hòa': ['Vĩnh Hoà', 'Vĩnh Hòa'], 'vũ hòa': ['Vũ Hoà', 'Vũ Hòa'], 'xuân ái': ['Xuân ái', 'Xuân Ái'], 'xuân áng': ['Xuân áng', 'Xuân Áng'], 'xuân hòa': ['Xuân Hoà', 'Xuân Hòa'], 'xuất hóa': ['Xuất Hoá', 'Xuất Hóa'], 'ỷ la': ['ỷ La', 'Ỷ La']}
groups_ward.update({1: ['1', '01'], 2: ['2', '02'], 3: ['3', '03'], 4: ['4', '04'], 5: ['5', '05'], 6: ['6', '06'], 7: ['7', '07'], 8: ['8', '08'], 9: ['9', '09']})
def to_same(groups):
    same = {ele: k for k, v in groups.items() for ele in v}
    return same
same_province = to_same(groups_province)
same_district = to_same(groups_district)
same_ward = to_same(groups_ward)
def normalize(text, same_dict):
    return same_dict.get(text, text)

TEAM_NAME = 'GROUP_2'  # This should be your team name
EXCEL_FILE = f'{TEAM_NAME}.xlsx'

import json
import time
with open('test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

summary_only = True
df = []
solution = Solution()
timer = []
correct = 0
for test_idx, data_point in enumerate(data):
    address = data_point["text"]

    ok = 0
    try:
        answer = data_point["result"]
        answer["province_normalized"] = normalize(answer["province"], same_province)
        answer["district_normalized"] = normalize(answer["district"], same_district)
        answer["ward_normalized"] = normalize(answer["ward"], same_ward)

        start = time.perf_counter_ns()
        result = solution.process(address)
        finish = time.perf_counter_ns()
        timer.append(finish - start)
        result["province_normalized"] = normalize(result["province"], same_province)
        result["district_normalized"] = normalize(result["district"], same_district)
        result["ward_normalized"] = normalize(result["ward"], same_ward)

        province_correct = int(answer["province_normalized"] == result["province_normalized"])
        district_correct = int(answer["district_normalized"] == result["district_normalized"])
        ward_correct = int(answer["ward_normalized"] == result["ward_normalized"])
        ok = province_correct + district_correct + ward_correct

        df.append([
            test_idx,
            address,
            answer["province"],
            result["province"],
            answer["province_normalized"],
            result["province_normalized"],
            province_correct,
            answer["district"],
            result["district"],
            answer["district_normalized"],
            result["district_normalized"],
            district_correct,
            answer["ward"],
            result["ward"],
            answer["ward_normalized"],
            result["ward_normalized"],
            ward_correct,
            ok,
            timer[-1] / 1_000_000_000,
        ])
    except Exception as e:
        print(f"{answer = }")
        print(f"{result = }")
        df.append([
            test_idx,
            address,
            answer["province"],
            "EXCEPTION",
            answer["province_normalized"],
            "EXCEPTION",
            0,
            answer["district"],
            "EXCEPTION",
            answer["district_normalized"],
            "EXCEPTION",
            0,
            answer["ward"],
            "EXCEPTION",
            answer["ward_normalized"],
            "EXCEPTION",
            0,
            0,
            0,
        ])
        # any failure count as a zero correct
        pass
    correct += ok


    if not summary_only:
        # responsive stuff
        print(f"Test {test_idx:5d}/{len(data):5d}")
        print(f"Correct: {ok}/3")
        print(f"Time Executed: {timer[-1] / 1_000_000_000:.4f}")


print(f"-"*30)
total = len(data) * 3
score_scale_10 = round(correct / total * 10, 2)
if len(timer) == 0:
    timer = [0]
max_time_sec = round(max(timer) / 1_000_000_000, 4)
avg_time_sec = round((sum(timer) / len(timer)) / 1_000_000_000, 4)

import pandas as pd

df2 = pd.DataFrame(
    [[correct, total, score_scale_10, max_time_sec, avg_time_sec]],
    columns=['correct', 'total', 'score / 10', 'max_time_sec', 'avg_time_sec',],
)

columns = [
    'ID',
    'text',
    'province',
    'province_student',
    'province_normalized',
    'province_student_normalized',
    'province_correct',
    'district',
    'district_student',
    'district_normalized',
    'district_student_normalized',
    'district_correct',
    'ward',
    'ward_student',
    'ward_normalized',
    'ward_student_normalized',
    'ward_correct',
    'total_correct',
    'time_sec',
]

df = pd.DataFrame(df)
df.columns = columns

print(f'{TEAM_NAME = }')
print(f'{EXCEL_FILE = }')
print(df2)

!pip install xlsxwriter
writer = pd.ExcelWriter(EXCEL_FILE, engine='xlsxwriter')
df2.to_excel(writer, index=False, sheet_name='summary')
df.to_excel(writer, index=False, sheet_name='details')
writer.close()