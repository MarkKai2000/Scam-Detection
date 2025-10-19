import string
import os
import re
import itertools

glyphs_ascii = {
		'0': ('o',),
		'1': ('l', 'i'),
		'3': ('8',),
		'6': ('9',),
		'8': ('3',),
		'9': ('6',),
		'b': ('d', 'lb'),
		'c': ('e',),
		'd': ('b', 'cl', 'dl'),
		'e': ('c',),
		'g': ('q',),
		'h': ('lh'),
		'i': ('1', 'l'),
		'k': ('lc'),
		'l': ('1', 'i'),
		'm': ('n', 'nn', 'rn'),
		'n': ('m', 'r'),
		'o': ('0',),
		'q': ('g',),
		'w': ('vv',),
		'rn': ('m',),
		'cl': ('d',),
	}

qwerty = {
    '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
    'a': 'qwsz', 's': 'edxzaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
    'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
}

qwertz = {
    '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7zt5', '7': '8uz6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6zgfr5', 'z': '7uhgt6', 'u': '8ijhz7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
    'a': 'qwsy', 's': 'edxyaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'zhbvft', 'h': 'ujnbgz', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
    'y': 'asx', 'x': 'ysdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
}

azerty = {
    '1': '2a', '2': '3za1', '3': '4ez2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'a': '2zq1', 'z': '3esqa2', 'e': '4rdsz3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0m',
    'q': 'zswa', 's': 'edxwqz', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'iknhu', 'k': 'olji', 'l': 'kopm', 'm': 'lp',
    'w': 'sxq', 'x': 'wsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhj'
}

# keyboards = [qwerty, qwertz, azerty]
keyboards = [qwerty]

vowel = ['a', 'e', 'o', 'i', 'u']
common_letter_replace_dic = {'b':'p','i':'1,l',"l":'i,1',"o":'0','c':'k','k':'c','p':'b','m':'n,l','n':'m','s':'5','d':'b','0':'o','z':'s'}

prefix_list = []

class MutationMethod:
    """generate NFT Collection name variants"""

    def __init__(self, ori_name):
        self.ori_name = ori_name
        self.variant_dic = {}
        self.length = len(self.ori_name)


    # 示例：nftname_mutation 里面调用这些新函数
    def nftname_mutation(self):
        self.vowel_character_deletion()
        self.vowel_character_insertion()
        self.vowel_character_substitution()
        self.double_character_deletion()
        self.double_character_insertion()
        self.common_misspelling_mistakes_substition()
        
        self.plural_to_singular()  # 添加单复数变换
        self.singular_to_plural()  # 添加单复数变换
        
        self.keyboard_insertion()  # 调用通用插入函数
        if (self.ori_name in self.variant_dic.keys()) or (self.ori_name.lower() in self.variant_dic.keys()):
            self.variant_dic.pop(self.ori_name.lower())


    def vowel_character_insertion(self):
        for i in range(0,self.length):
            word = self.ori_name.lower()
            if word[i] in vowel:
                for r_letter in vowel:
                    word_front = self.ori_name.lower()
                    # a -> ia
                    word_end = self.ori_name.lower()
                    # a -> ai
                    
                    word_front = word_front[0:i] + r_letter + word_front[i:]
                    self.variant_dic[word_front] = 'vowel_character_insertion'
                    
                    word_end = word_end[0:i+1] + r_letter + word_end[i+1:]
                    self.variant_dic[word_end] = 'vowel_character_insertion'

    def vowel_character_deletion(self):
        for i in range(0,self.length):
            word = self.ori_name.lower()
            if word[i] in vowel:
                word = word[0:i] + word[i+1:]
                self.variant_dic[word] = 'vowel_character_deletion'

    def vowel_character_substitution(self):
        for i in range(0,self.length):
            word = self.ori_name.lower()
            if word[i] in vowel:
                for r_letter in vowel:
                    word = self.ori_name.lower()
                    if r_letter != word[i]:
                        word = word[0:i] + r_letter + word[i+1:]
                        self.variant_dic[word] = 'vowel_character_substitution'


    def double_character_insertion(self):
        for i in range(0,self.length-1):
            word = self.ori_name.lower()
            if word[i] == word[i + 1]:
                word = word[0:i] + word[i] + word[i:]
                self.variant_dic[word] = 'double_character_insertion'

    def double_character_deletion(self):
        """检测并删除双字符"""
        for i in range(0, self.length - 1):
            word = self.ori_name.lower()
            if word[i] == word[i + 1]:
                # 删除相邻的重复字符，只需进行一次删除操作
                new_word = word[0:i] + word[i + 1:]
                self.variant_dic[new_word] = 'double_character_deletion'



    def common_misspelling_mistakes_substition(self):
        """处理常见拼写错误的替换"""
        self.double_character_common_misspelling_mistakes_substition()
        for i in range(0, self.length):
            word = self.ori_name.lower()
            if word[i] in common_letter_replace_dic:
                # 获取替换字符（可能有多个替换值）
                replacements = common_letter_replace_dic[word[i]].split(',')
                for r_letter in replacements:
                    new_word = word[0:i] + r_letter + word[i+1:]
                    self.variant_dic[new_word] = 'misspelling_mistakes_substition'


    def double_character_common_misspelling_mistakes_substition(self):
        """处理重复字符的常见拼写错误替换"""
        for i in range(0, self.length - 1):
            word = self.ori_name.lower()
            if word[i] == word[i + 1] and word[i] in common_letter_replace_dic:
                # 获取替换字符（可能有多个替换值）
                replacements = common_letter_replace_dic[word[i]].split(',')
                for r_letter in replacements:
                    new_word = word[0:i] + r_letter + r_letter + word[i+2:]
                    self.variant_dic[new_word] = 'misspelling_mistakes_substition'

        
    def plural_to_singular(self):
        """将复数形式变为单数形式"""
        word = self.ori_name.lower()
        if word.endswith('s'):
            # 去掉末尾的 's'
            singular_word = word[:-1]
            self.variant_dic[singular_word] = 'plural_to_singular'

    def singular_to_plural(self):
        """将单数形式变为复数形式"""
        word = self.ori_name.lower()
        if not word.endswith('s'):
            # 添加 's'
            plural_word = word + 's'
            self.variant_dic[plural_word] = 'singular_to_plural'   
                    
                

    def keyboard_insertion(self):
        """基于多种键盘布局生成插入字符的变体"""
        for i in range(0, len(self.ori_name)):  # 遍历每个字符位置
            prefix, orig_c, suffix = self.ori_name[:i], self.ori_name[i], self.ori_name[i+1:]
            
            # 遍历所有键盘布局中的字符
            for c in (char for keyboard in keyboards for char in keyboard.get(orig_c, [])):
                # 在当前位置插入字符的所有可能性
                new_words = [
                    prefix + c + orig_c + suffix,  # 在字符前插入
                    prefix + orig_c + c + suffix   # 在字符后插入
                ]
                for new_word in new_words:
                    self.variant_dic[new_word] = 'keyboard_insertion'



    

# 使用示例
mutation = MutationMethod('goblintown')
mutation.nftname_mutation()
# mutation.common_misspelling_mistakes_substition()
# print(mutation.variant_dic)
mutation_result_dic = mutation.variant_dic
for key,value in mutation_result_dic.items():
    print("%s %s"%(value.ljust(40),key))
