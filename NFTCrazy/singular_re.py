import re
def plural_to_singular(self):
        """将复数形式变为单数形式"""
        word = self.ori_name.lower()

        # 定义规则：处理复数变单数
        if re.search(r'([^aeiouy]|qu)ies$', word):
            singular_word = re.sub(r'([^aeiouy]|qu)ies$', r'\1y', word)  # 比如 parties -> party
        elif re.search(r'(?:([^f])ves|([lr])ves)$', word):
            singular_word = re.sub(r'(?:([^f])ves|([lr])ves)$', r'\1\2f', word)  # 比如 wives -> wife
        elif word.endswith('es'):
            singular_word = word[:-2]  # 去掉末尾的 'es'
        elif word.endswith('s'):
            singular_word = word[:-1]  # 去掉末尾的 's'
        else:
            singular_word = word

        # 保存变体
        self.variant_dic[singular_word] = 'plural_to_singular'

def singular_to_plural(self):
        """将单数形式变为复数形式"""
        word = self.ori_name.lower()

        # 定义规则：处理单数变复数
        if re.search(r'([^aeiouy]|qu)y$', word):
            plural_word = re.sub(r'([^aeiouy]|qu)y$', r'\1ies', word)  # 比如 party -> parties
        elif re.search(r'(?:([^f])fe|([lr])f)$', word):
            plural_word = re.sub(r'(?:([^f])fe|([lr])f)$', r'\1\2ves', word)  # 比如 wife -> wives
        elif not word.endswith('s'):
            plural_word = word + 's'  # 添加 's'
        else:
            plural_word = word

        # 保存变体
        self.variant_dic[plural_word] = 'singular_to_plural'            