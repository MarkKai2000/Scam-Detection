def process_nft_name_with_Homophones(nft_name):
    with open("homophones.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines if not line.startswith("#") and line.strip()]
        
    # 将每一行的同音词分组
    word_sets = [line.lower().split(",") for line in lines]

        # 生成同音词字典
    homophones_dict = {}
    for word_set in word_sets:
        for word in word_set:
            homophones_dict[word.strip()] = word_set
    
    # print(homophones_dict)
    
    words = nft_name.lower().split()  
    variants = []
    # print(words)
    # 遍历每个单词，检查是否有错拼的替换
    for i, word in enumerate(words):
        if word in homophones_dict:
            homophones = homophones_dict[word]
            for item in homophones:
                if item != word:
                    new_variant = words[:i] + [item] + words[i+1:]
                    variants.append(" ".join(new_variant))
    if not variants:
        return []
    return variants


def process_nft_name_with_misspellings(nft_name):
    """处理 NFT 名称并生成拼写错误变体，基于 common-misspellings.txt 文件"""
    file_path = "common-misspellings.txt"
    misspelling_dict = {}

    # 读取并加载拼写错误字典
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 解析文件，过滤注释行和空行
    lines = [line.strip() for line in lines if not line.startswith("#") and line.strip()]

    # 遍历每一行，解析出正确的单词和错拼单词，并建立双向字典
    for line in lines:
        correct, misspelled = line.lower().split("->")
        correct = correct.strip()
        misspelled = misspelled.strip()

        # 将正确拼写和错拼的关系存入字典，双向存储
        for word in correct.split(","):
            word = word.strip()
            misspelling_dict[word] = misspelled
            misspelling_dict[misspelled] = word  # 反向存储
        
        # 如果 misspelled 里有多个值，确保所有的拼写变体都能双向存储
        for misspelled_word in misspelled.split(","):
            misspelled_word = misspelled_word.strip()
            misspelling_dict[misspelled_word] = correct
            misspelling_dict[correct] = misspelled_word  # 反向存储


    # print("加载的拼写错误字典：", misspelling_dict)

    words = nft_name.lower().split()  
    variants = []
    # print(words)
    for i, word in enumerate(words):
        if word in misspelling_dict:
            misspelled_word = misspelling_dict[word]
            new_variant = words[:i] + [misspelled_word] + words[i+1:]
            variants.append(" ".join(new_variant))

    if not variants:
        return []
    return variants


# 示例用法
if __name__ == "__main__":
    
    variants = process_nft_name_with_Homophones("Ape Bored Yacht Club")
    print(variants)
    # 输入的 NFT 名称
    # nft_name = "Bored Ape Yacht Club"
    nft_name = "Yacht"
    
    # 处理拼写错误变体
    variants = process_nft_name_with_misspellings(nft_name)

    # 输出结果
    print(f"原始名称: {nft_name}")
    if variants:
        print("生成的拼写错误变体:")
        for variant in variants:
            print(variant)
    else:
        print("没有生成拼写错误变体。")
