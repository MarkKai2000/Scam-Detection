def bitsquatting(domain):
    masks = [1, 2, 4, 8, 16, 32, 64, 128]
    chars = set('abcdefghijklmnopqrstuvwxyz0123456789')
    result = []
    for i, c in enumerate(domain):
        for mask in masks:
            b = chr(ord(c) ^ mask)
            if b in chars:
                # 将生成的位欺骗域名添加到结果列表
                result.append(domain[:i] + b + domain[i+1:])
    return result

# 使用示例
domain = "CryptoZunks"
bit_squat_domains = bitsquatting(domain)

# 输出所有生成的位欺骗域名
for squat_domain in bit_squat_domains:
    print(squat_domain)
