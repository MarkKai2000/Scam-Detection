# 针对一些容易出现视觉差的字符

common_letter_replace_dic = {'b':'p','i':'1,l',"l":'i,1',"o":'0','c':'k','k':'c','p':'b','m':'n','n':'m','s':'5'}

'p':'b'
v-w
w-v
p-z
p-f
p-g
空格换成'_'和'-'

m l
n l
i y

i - o

z-s

# Omissions 
删除尾部的s


# Insertion
moonbirds - moonbhirds


# 问题
1. 生成关键词，对于Combo的处理 部分匹配
    - 现有的就是后面加上1，2，一些数字等
    - 不要求精确命中

2. 对于大小写的处理，有必要吗


3. 对于空格的处理，将空格作为一个分割，将NFT分割为几个部分
    - 删除的处理，删除个别字符，还是直接删除单词

4. 工具比较问题
