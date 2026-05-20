"""
生成电影知识图谱样本数据
结合豆瓣 Top250 列表页数据 + 手工整理的经典电影详情，构建完整的知识图谱数据集。
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 经典电影详情数据 (中文电影为主，使用豆瓣公开信息)
MOVIE_DETAILS = {
    "1292052": {  # The Shawshank Redemption
        "title": "肖申克的救赎", "year": 1994, "rating": 9.7,
        "duration": 142, "summary": "银行家安迪因被误判杀害妻子及其情人而被关进肖申克监狱，凭借才智和毅力用二十年时间完成越狱。",
        "genres": ["剧情", "犯罪"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1047973", "name": "弗兰克·德拉邦特", "role": "director"}],
        "writers": [{"douban_id": "1047973", "name": "弗兰克·德拉邦特", "role": "writer"},
                     {"douban_id": "1027225", "name": "斯蒂芬·金", "role": "writer"}],
        "actors": [{"douban_id": "1054521", "name": "蒂姆·罗宾斯", "role_name": "安迪·杜佛兰"},
                    {"douban_id": "1054534", "name": "摩根·弗里曼", "role_name": "瑞德"},
                    {"douban_id": "1041174", "name": "鲍勃·冈顿", "role_name": "典狱长"}],
    },
    "1291546": {  # 霸王别姬
        "title": "霸王别姬", "year": 1993, "rating": 9.6,
        "duration": 171, "summary": "段小楼与程蝶衣从小在京剧班学艺，两人合演《霸王别姬》名震京城，历经中国半个世纪的社会变迁。",
        "genres": ["剧情", "爱情", "同性"], "countries": ["中国大陆", "中国香港"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1023045", "name": "陈凯歌", "role": "director"}],
        "writers": [{"douban_id": "1023045", "name": "陈凯歌", "role": "writer"},
                     {"douban_id": "1041515", "name": "李碧华", "role": "writer"}],
        "actors": [{"douban_id": "1003494", "name": "张国荣", "role_name": "程蝶衣"},
                    {"douban_id": "1023514", "name": "张丰毅", "role_name": "段小楼"},
                    {"douban_id": "1016899", "name": "巩俐", "role_name": "菊仙"}],
    },
    "1292722": {  # 阿甘正传
        "title": "阿甘正传", "year": 1994, "rating": 9.5,
        "duration": 142, "summary": "智商只有75的阿甘，凭借跑步天赋和纯真的心，经历了美国几十年的历史变迁。",
        "genres": ["剧情", "爱情"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1053561", "name": "罗伯特·泽米吉斯", "role": "director"}],
        "actors": [{"douban_id": "1054450", "name": "汤姆·汉克斯", "role_name": "阿甘"},
                    {"douban_id": "1048027", "name": "罗宾·怀特", "role_name": "珍妮"}],
    },
    "1295644": {  # 这个杀手不太冷
        "title": "这个杀手不太冷", "year": 1994, "rating": 9.4,
        "duration": 110, "summary": "职业杀手莱昂无意中搭救了一个全家被杀害的小女孩玛蒂尔达，两人在相处中产生了超越年龄的情感。",
        "genres": ["剧情", "动作", "犯罪"], "countries": ["法国"], "languages": ["英语", "法语"],
        "directors": [{"douban_id": "1031876", "name": "吕克·贝松", "role": "director"}],
        "actors": [{"douban_id": "1010509", "name": "让·雷诺", "role_name": "莱昂"},
                    {"douban_id": "1054454", "name": "娜塔莉·波特曼", "role_name": "玛蒂尔达"},
                    {"douban_id": "1013847", "name": "加里·奥德曼", "role_name": "斯坦斯菲尔德"}],
    },
    "1292063": {  # 美丽人生
        "title": "美丽人生", "year": 1997, "rating": 9.6,
        "duration": 116, "summary": "犹太人圭多和儿子被关进集中营，他哄骗儿子这是一场游戏，用生命保护了儿子的童心。",
        "genres": ["剧情", "喜剧", "爱情", "战争"], "countries": ["意大利"], "languages": ["意大利语"],
        "directors": [{"douban_id": "1045105", "name": "罗伯托·贝尼尼", "role": "director"}],
        "actors": [{"douban_id": "1045105", "name": "罗伯托·贝尼尼", "role_name": "圭多"}],
    },
    "1291561": {  # 千与千寻
        "title": "千与千寻", "year": 2001, "rating": 9.4,
        "duration": 125, "summary": "少女千寻随父母误入神灵世界，为救回变成猪的父母，她在汤屋工作并逐渐成长。",
        "genres": ["剧情", "动画", "奇幻"], "countries": ["日本"], "languages": ["日语"],
        "directors": [{"douban_id": "1054418", "name": "宫崎骏", "role": "director"}],
        "actors": [{"douban_id": "1025452", "name": "柊瑠美", "role_name": "千寻(配音)"}],
    },
    "1292720": {  # 泰坦尼克号
        "title": "泰坦尼克号", "year": 1997, "rating": 9.4,
        "duration": 194, "summary": "穷画家杰克和贵族少女罗丝在泰坦尼克号上相恋，船撞冰山后杰克为救罗丝而牺牲。",
        "genres": ["剧情", "爱情", "灾难"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1022571", "name": "詹姆斯·卡梅隆", "role": "director"}],
        "actors": [{"douban_id": "1041029", "name": "莱昂纳多·迪卡普里奥", "role_name": "杰克"},
                    {"douban_id": "1054446", "name": "凯特·温丝莱特", "role_name": "罗丝"}],
    },
    "1291549": {  # 放牛班的春天
        "title": "放牛班的春天", "year": 2004, "rating": 9.3,
        "duration": 97, "summary": "音乐教师马修来到一所问题儿童寄宿学校，用音乐打开了孩子们封闭的心扉。",
        "genres": ["剧情", "音乐"], "countries": ["法国"], "languages": ["法语"],
        "directors": [{"douban_id": "1056315", "name": "克里斯托夫·巴拉蒂", "role": "director"}],
        "actors": [{"douban_id": "1045064", "name": "杰拉尔·朱尼奥", "role_name": "马修"}],
    },
    "1291841": {  # 教父
        "title": "教父", "year": 1972, "rating": 9.3,
        "duration": 175, "summary": "维托·柯里昂是美国最有权势的黑手党家族首领，小儿子迈克尔从不愿涉足家族事业到最终继承父业。",
        "genres": ["剧情", "犯罪"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1054419", "name": "弗朗西斯·福特·科波拉", "role": "director"}],
        "actors": [{"douban_id": "1054451", "name": "马龙·白兰度", "role_name": "维托·柯里昂"},
                    {"douban_id": "1054452", "name": "阿尔·帕西诺", "role_name": "迈克尔·柯里昂"}],
    },
    "1292001": {  # 海上钢琴师
        "title": "海上钢琴师", "year": 1998, "rating": 9.3,
        "duration": 165, "summary": "1900年在一艘豪华邮轮上被遗弃的婴儿，成长为天才钢琴师，却一生未曾踏上陆地。",
        "genres": ["剧情", "音乐"], "countries": ["意大利"], "languages": ["英语"],
        "directors": [{"douban_id": "1018983", "name": "朱塞佩·托纳多雷", "role": "director"}],
        "actors": [{"douban_id": "1041136", "name": "蒂姆·罗斯", "role_name": "1900"}],
    },
    "1292213": {  # 大话西游之大圣娶亲
        "title": "大话西游之大圣娶亲", "year": 1995, "rating": 9.2,
        "duration": 99, "summary": "至尊宝穿越时空回到五百年前，遇到了紫霞仙子，在情与义之间做出选择。",
        "genres": ["喜剧", "爱情", "奇幻", "古装"], "countries": ["中国香港"], "languages": ["粤语"],
        "directors": [{"douban_id": "1027846", "name": "刘镇伟", "role": "director"}],
        "actors": [{"douban_id": "1048026", "name": "周星驰", "role_name": "至尊宝/孙悟空"},
                    {"douban_id": "1019053", "name": "朱茵", "role_name": "紫霞仙子"},
                    {"douban_id": "1016771", "name": "吴孟达", "role_name": "二当家"}],
    },
    "1291543": {  # 功夫
        "title": "功夫", "year": 2004, "rating": 8.8,
        "duration": 100, "summary": "小混混阿星误闯猪笼城寨，卷入了斧头帮与隐世高手的争斗，最终领悟真正的功夫。",
        "genres": ["动作", "喜剧", "奇幻"], "countries": ["中国大陆", "中国香港"], "languages": ["粤语", "汉语普通话"],
        "directors": [{"douban_id": "1048026", "name": "周星驰", "role": "director"}],
        "writers": [{"douban_id": "1048026", "name": "周星驰", "role": "writer"}],
        "actors": [{"douban_id": "1048026", "name": "周星驰", "role_name": "阿星"},
                    {"douban_id": "1016751", "name": "元秋", "role_name": "包租婆"},
                    {"douban_id": "1028689", "name": "元华", "role_name": "包租公"},
                    {"douban_id": "1014745", "name": "黄圣依", "role_name": "芳儿"}],
    },
    "1291544": {  # 让子弹飞
        "title": "让子弹飞", "year": 2010, "rating": 9.0,
        "duration": 132, "summary": "北洋年间，土匪张牧之劫了县长马邦德的火车，冒充县长去鹅城上任，与恶霸黄四郎展开较量。",
        "genres": ["剧情", "喜剧", "动作"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1027903", "name": "姜文", "role": "director"}],
        "writers": [{"douban_id": "1027903", "name": "姜文", "role": "writer"}],
        "actors": [{"douban_id": "1027903", "name": "姜文", "role_name": "张牧之"},
                    {"douban_id": "1006959", "name": "葛优", "role_name": "马邦德"},
                    {"douban_id": "1044899", "name": "周润发", "role_name": "黄四郎"}],
    },
    "1291552": {  # 无间道
        "title": "无间道", "year": 2002, "rating": 9.3,
        "duration": 101, "summary": "警方卧底陈永仁和黑帮卧底刘建明各自潜伏在对方组织中，一场关于身份的较量就此展开。",
        "genres": ["剧情", "犯罪", "悬疑"], "countries": ["中国香港"], "languages": ["粤语"],
        "directors": [{"douban_id": "1028682", "name": "刘伟强", "role": "director"},
                       {"douban_id": "1274988", "name": "麦兆辉", "role": "director"}],
        "actors": [{"douban_id": "1054424", "name": "刘德华", "role_name": "刘建明"},
                    {"douban_id": "1006583", "name": "梁朝伟", "role_name": "陈永仁"},
                    {"douban_id": "1041381", "name": "黄秋生", "role_name": "黄志诚"},
                    {"douban_id": "1004439", "name": "曾志伟", "role_name": "韩琛"}],
    },
    "1291560": {  # 龙猫
        "title": "龙猫", "year": 1988, "rating": 9.2,
        "duration": 86, "summary": "两姐妹随父亲搬到乡下，在森林中遇到了可爱的龙猫，展开了一系列奇妙冒险。",
        "genres": ["动画", "奇幻", "冒险"], "countries": ["日本"], "languages": ["日语"],
        "directors": [{"douban_id": "1054418", "name": "宫崎骏", "role": "director"}],
    },
    "1292220": {  # 楚门的世界
        "title": "楚门的世界", "year": 1998, "rating": 9.3,
        "duration": 103, "summary": "楚门从小生活在一个巨大的摄影棚中，他的整个人生都是一档直播节目，直到他开始怀疑这个世界。",
        "genres": ["剧情", "科幻"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1027823", "name": "彼得·威尔", "role": "director"}],
        "actors": [{"douban_id": "1054435", "name": "金·凯瑞", "role_name": "楚门"}],
    },
    "1292365": {  # 活着
        "title": "活着", "year": 1994, "rating": 9.3,
        "duration": 132, "summary": "福贵一家在几十年的历史变迁中经历了种种苦难，但始终坚韧地活着。",
        "genres": ["剧情", "历史", "家庭"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1023027", "name": "张艺谋", "role": "director"}],
        "actors": [{"douban_id": "1006959", "name": "葛优", "role_name": "福贵"},
                    {"douban_id": "1016899", "name": "巩俐", "role_name": "家珍"}],
    },
    "1291843": {  # 黑客帝国
        "title": "黑客帝国", "year": 1999, "rating": 9.1,
        "duration": 136, "summary": "程序员尼奥发现看似正常的世界实际上是机器创造的虚拟现实，他加入反抗军对抗机器统治。",
        "genres": ["动作", "科幻"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1027779", "name": "沃卓斯基姐妹", "role": "director"}],
        "actors": [{"douban_id": "1040997", "name": "基努·里维斯", "role_name": "尼奥"}],
    },
    "1292274": {  # 蝙蝠侠：黑暗骑士
        "title": "蝙蝠侠：黑暗骑士", "year": 2008, "rating": 9.2,
        "duration": 152, "summary": "蝙蝠侠面对混乱使者小丑的挑战，在正义与秩序之间做出艰难抉择。",
        "genres": ["剧情", "动作", "科幻", "犯罪"], "countries": ["美国", "英国"], "languages": ["英语"],
        "directors": [{"douban_id": "1054434", "name": "克里斯托弗·诺兰", "role": "director"}],
        "actors": [{"douban_id": "1006956", "name": "克里斯蒂安·贝尔", "role_name": "蝙蝠侠"},
                    {"douban_id": "1006948", "name": "希斯·莱杰", "role_name": "小丑"}],
    },
    "1291858": {  # 鬼子来了
        "title": "鬼子来了", "year": 2000, "rating": 9.3,
        "duration": 139, "summary": "抗战末期，挂甲台村民马大三被迫看管一个日本俘虏和一个翻译，引发了一系列悲剧。",
        "genres": ["剧情", "历史", "战争"], "countries": ["中国大陆"], "languages": ["汉语普通话", "日语"],
        "directors": [{"douban_id": "1027903", "name": "姜文", "role": "director"}],
        "actors": [{"douban_id": "1027903", "name": "姜文", "role_name": "马大三"}],
    },
    "1291572": {  # 指环王：王者无敌
        "title": "指环王：王者无敌", "year": 2003, "rating": 9.3,
        "duration": 201, "summary": "弗罗多和山姆深入魔多销毁至尊魔戒，阿拉贡率领人类大军进行最后的决战。",
        "genres": ["剧情", "动作", "奇幻", "冒险"], "countries": ["新西兰", "美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1041124", "name": "彼得·杰克逊", "role": "director"}],
        "actors": [{"douban_id": "1041126", "name": "伊利亚·伍德", "role_name": "弗罗多"}],
    },
    "fake001": {  # 星际穿越 (Interstellar)
        "title": "星际穿越", "year": 2014, "rating": 9.4,
        "duration": 169, "summary": "未来地球环境恶化，前NASA飞行员库珀穿越虫洞前往遥远星系，为人类寻找新的家园。",
        "genres": ["剧情", "科幻", "冒险"], "countries": ["美国", "英国"], "languages": ["英语"],
        "directors": [{"douban_id": "1054434", "name": "克里斯托弗·诺兰", "role": "director"}],
        "writers": [{"douban_id": "1054434", "name": "克里斯托弗·诺兰", "role": "writer"},
                     {"douban_id": "1041134", "name": "乔纳森·诺兰", "role": "writer"}],
        "actors": [{"douban_id": "fp019", "name": "马修·麦康纳", "role_name": "库珀"},
                    {"douban_id": "fp020", "name": "安妮·海瑟薇", "role_name": "布兰德"},
                    {"douban_id": "1041033", "name": "杰西卡·查斯坦", "role_name": "墨菲(成年)"}],
    },
    "fake002": {  # 盗梦空间 (Inception)
        "title": "盗梦空间", "year": 2010, "rating": 9.4,
        "duration": 148, "summary": "盗梦师柯布通过潜入他人梦境窃取秘密，接受了一个看似不可能的任务：在目标脑中植入一个想法。",
        "genres": ["剧情", "科幻", "悬疑", "冒险"], "countries": ["美国", "英国"], "languages": ["英语", "日语", "法语"],
        "directors": [{"douban_id": "1054434", "name": "克里斯托弗·诺兰", "role": "director"}],
        "writers": [{"douban_id": "1054434", "name": "克里斯托弗·诺兰", "role": "writer"}],
        "actors": [{"douban_id": "1041029", "name": "莱昂纳多·迪卡普里奥", "role_name": "柯布"},
                    {"douban_id": "fp021", "name": "约瑟夫·高登-莱维特", "role_name": "亚瑟"},
                    {"douban_id": "1048167", "name": "艾伦·佩吉", "role_name": "阿里亚德妮"}],
    },
    "fake003": {  # 辛德勒的名单 (Schindler's List)
        "title": "辛德勒的名单", "year": 1993, "rating": 9.6,
        "duration": 195, "summary": "二战期间，德国商人辛德勒目睹犹太人遭受屠杀后，倾尽所有保护了1100多名犹太人的生命。",
        "genres": ["剧情", "历史", "战争"], "countries": ["美国"], "languages": ["英语", "希伯来语", "德语", "波兰语"],
        "directors": [{"douban_id": "1054436", "name": "史蒂文·斯皮尔伯格", "role": "director"}],
        "actors": [{"douban_id": "fp022", "name": "连姆·尼森", "role_name": "奥斯卡·辛德勒"},
                    {"douban_id": "1013847", "name": "加里·奥德曼", "role_name": "阿蒙·戈斯"},
                    {"douban_id": "1041000", "name": "本·金斯利", "role_name": "伊扎克·斯特恩"}],
    },
    "fake004": {  # 搏击俱乐部 (Fight Club)
        "title": "搏击俱乐部", "year": 1999, "rating": 9.0,
        "duration": 139, "summary": "一个患有失眠症的白领遇到了肥皂制造商泰勒，两人创立了地下搏击俱乐部，事态逐渐失控。",
        "genres": ["剧情", "动作", "悬疑", "惊悚"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1017937", "name": "大卫·芬奇", "role": "director"}],
        "actors": [{"douban_id": "fp023", "name": "布拉德·皮特", "role_name": "泰勒·德顿"},
                    {"douban_id": "1054431", "name": "爱德华·诺顿", "role_name": "叙述者"}],
    },
    "fake005": {  # 飞越疯人院 (One Flew Over the Cuckoo's Nest)
        "title": "飞越疯人院", "year": 1975, "rating": 9.1,
        "duration": 133, "summary": "麦克墨菲为了逃避监狱劳动装疯进入精神病院，他的反抗精神唤醒了病人们，却最终被体制无情碾碎。",
        "genres": ["剧情"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1022789", "name": "米洛斯·福尔曼", "role": "director"}],
        "actors": [{"douban_id": "fp024", "name": "杰克·尼科尔森", "role_name": "麦克墨菲"},
                    {"douban_id": "1048168", "name": "路易丝·弗莱彻", "role_name": "瑞秋护士"}],
    },
    "fake006": {  # 机器人总动员 (WALL-E)
        "title": "机器人总动员", "year": 2008, "rating": 9.3,
        "duration": 98, "summary": "地球被垃圾覆盖，清扫机器人瓦力独自工作数百年后，遇到了搜索机器人伊芙，随之展开太空冒险。",
        "genres": ["科幻", "动画", "冒险"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "1049666", "name": "安德鲁·斯坦顿", "role": "director"}],
        "actors": [{"douban_id": "1041127", "name": "本·贝尔特", "role_name": "瓦力(配音)"}],
    },
    "fake007": {  # 疯狂动物城 (Zootopia)
        "title": "疯狂动物城", "year": 2016, "rating": 9.2,
        "duration": 109, "summary": "兔子朱迪来到动物城实现警察梦想，与狐狸尼克搭档侦破一起神秘失踪案。",
        "genres": ["喜剧", "动画", "冒险"], "countries": ["美国"], "languages": ["英语"],
        "directors": [{"douban_id": "fp025", "name": "拜伦·霍华德", "role": "director"},
                       {"douban_id": "fp026", "name": "里奇·摩尔", "role": "director"}],
        "actors": [{"douban_id": "1049505", "name": "金妮弗·古德温", "role_name": "朱迪(配音)"}],
    },
    "fake008": {  # 大闹天宫
        "title": "大闹天宫", "year": 1965, "rating": 9.4,
        "duration": 114, "summary": "孙悟空因不满天庭赐予的弼马温官职大闹天宫，与天兵天将展开一场惊天动地的战斗。",
        "genres": ["动画", "奇幻"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1049791", "name": "万籁鸣", "role": "director"}],
    },
    "fake009": {  # 哪吒之魔童降世
        "title": "哪吒之魔童降世", "year": 2019, "rating": 8.4,
        "duration": 110, "summary": "哪吒本应是灵珠转世却被调包为魔丸，面对命运的偏见和天劫，他喊出'我命由我不由天'。",
        "genres": ["剧情", "喜剧", "动画", "奇幻"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp008", "name": "饺子", "role": "director"}],
        "writers": [{"douban_id": "fp008", "name": "饺子", "role": "writer"}],
    },
    "fake010": {  # 流浪地球
        "title": "流浪地球", "year": 2019, "rating": 7.9,
        "duration": 125, "summary": "太阳即将膨胀吞噬地球，人类启动'流浪地球'计划，在地表建造万座发动机推动地球离开太阳系。",
        "genres": ["科幻", "冒险", "灾难"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp009", "name": "郭帆", "role": "director"}],
        "actors": [{"douban_id": "fp010", "name": "吴京", "role_name": "刘培强"},
                    {"douban_id": "fp027", "name": "屈楚萧", "role_name": "刘启"},
                    {"douban_id": "fp028", "name": "李光洁", "role_name": "王磊"}],
    },
    "fake011": {  # 战狼2
        "title": "战狼2", "year": 2017, "rating": 7.1,
        "duration": 123, "summary": "退伍特种兵冷锋在非洲内战中孤身犯险，保护华侨和当地难民撤离战区。",
        "genres": ["动作", "战争"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp010", "name": "吴京", "role": "director"}],
        "actors": [{"douban_id": "fp010", "name": "吴京", "role_name": "冷锋"},
                    {"douban_id": "fp029", "name": "弗兰克·格里罗", "role_name": "老爹"}],
    },
    "fake012": {  # 红海行动
        "title": "红海行动", "year": 2018, "rating": 8.3,
        "duration": 138, "summary": "中国海军蛟龙突击队深入北非某国执行撤侨任务，卷入了一场惊心动魄的军事对抗。",
        "genres": ["动作", "战争"], "countries": ["中国大陆", "摩洛哥"], "languages": ["汉语普通话", "阿拉伯语"],
        "directors": [{"douban_id": "fp011", "name": "林超贤", "role": "director"}],
        "actors": [{"douban_id": "fp030", "name": "张译", "role_name": "杨锐"},
                    {"douban_id": "fp031", "name": "黄景瑜", "role_name": "顾顺"}],
    },
    "fake013": {  # 我不是药神
        "title": "我不是药神", "year": 2018, "rating": 9.0,
        "duration": 117, "summary": "保健品店主程勇从印度代购白血病特效药，救人无数却被视为走私犯，引发社会对药价与生命的深思。",
        "genres": ["剧情", "喜剧"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp012", "name": "文牧野", "role": "director"}],
        "actors": [{"douban_id": "fp032", "name": "徐峥", "role_name": "程勇"},
                    {"douban_id": "fp033", "name": "王传君", "role_name": "吕受益"},
                    {"douban_id": "fp034", "name": "谭卓", "role_name": "刘思慧"}],
    },
    "fake014": {  # 少年的你
        "title": "少年的你", "year": 2019, "rating": 8.2,
        "duration": 135, "summary": "高考前夕，优等生陈念遭遇校园霸凌，结识街头少年小北，两个孤独的灵魂相互守护。",
        "genres": ["剧情", "爱情", "犯罪"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp013", "name": "曾国祥", "role": "director"}],
        "actors": [{"douban_id": "fp035", "name": "周冬雨", "role_name": "陈念"},
                    {"douban_id": "fp036", "name": "易烊千玺", "role_name": "小北"}],
    },
    "fake015": {  # 你好，李焕英
        "title": "你好，李焕英", "year": 2021, "rating": 7.7,
        "duration": 128, "summary": "贾晓玲穿越到1981年，与年轻时的母亲李焕英相遇，试图让母亲过上'更好'的人生。",
        "genres": ["剧情", "喜剧", "奇幻"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp014", "name": "贾玲", "role": "director"}],
        "writers": [{"douban_id": "fp014", "name": "贾玲", "role": "writer"}],
        "actors": [{"douban_id": "fp014", "name": "贾玲", "role_name": "贾晓玲"},
                    {"douban_id": "fp037", "name": "张小斐", "role_name": "李焕英"},
                    {"douban_id": "fp038", "name": "沈腾", "role_name": "沈光林"}],
    },
    "fake016": {  # 长津湖
        "title": "长津湖", "year": 2021, "rating": 7.4,
        "duration": 176, "summary": "1950年长津湖战役中，中国人民志愿军在极寒条件下与美军精锐展开殊死搏斗。",
        "genres": ["剧情", "历史", "战争"], "countries": ["中国大陆"], "languages": ["汉语普通话", "英语"],
        "directors": [{"douban_id": "1023045", "name": "陈凯歌", "role": "director"},
                       {"douban_id": "fp015", "name": "徐克", "role": "director"}],
        "actors": [{"douban_id": "fp010", "name": "吴京", "role_name": "伍千里"},
                    {"douban_id": "fp036", "name": "易烊千玺", "role_name": "伍万里"}],
    },
    "fake017": {  # 饮食男女
        "title": "饮食男女", "year": 1994, "rating": 9.2,
        "duration": 124, "summary": "退休大厨老朱每周为三个女儿准备丰盛家宴，通过食物传递着关于家庭、爱情和传统的情感。",
        "genres": ["剧情", "家庭"], "countries": ["中国台湾", "美国"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp001", "name": "李安", "role": "director"}],
        "actors": [{"douban_id": "1016933", "name": "郎雄", "role_name": "老朱"},
                    {"douban_id": "fp039", "name": "吴倩莲", "role_name": "朱家倩"}],
    },
    "fake018": {  # 卧虎藏龙
        "title": "卧虎藏龙", "year": 2000, "rating": 8.4,
        "duration": 120, "summary": "大侠李慕白欲将青冥剑交给贝勒爷引退江湖，却被玉娇龙盗走，引发一场江湖恩怨与情仇。",
        "genres": ["剧情", "爱情", "武侠"], "countries": ["中国台湾", "中国香港", "美国", "中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp001", "name": "李安", "role": "director"}],
        "actors": [{"douban_id": "1044899", "name": "周润发", "role_name": "李慕白"},
                    {"douban_id": "fp040", "name": "杨紫琼", "role_name": "俞秀莲"},
                    {"douban_id": "fp041", "name": "章子怡", "role_name": "玉娇龙"}],
    },
    "fake019": {  # 英雄
        "title": "英雄", "year": 2002, "rating": 7.7,
        "duration": 99, "summary": "战国末期，刺客无名奉命刺杀秦王，在与秦王的对谈中讲述了他与残剑、飞雪等侠客的故事。",
        "genres": ["剧情", "动作", "武侠", "古装"], "countries": ["中国大陆", "中国香港"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "1023027", "name": "张艺谋", "role": "director"}],
        "actors": [{"douban_id": "1006583", "name": "梁朝伟", "role_name": "残剑"},
                    {"douban_id": "fp042", "name": "张曼玉", "role_name": "飞雪"},
                    {"douban_id": "fp043", "name": "李连杰", "role_name": "无名"},
                    {"douban_id": "fp041", "name": "章子怡", "role_name": "如月"}],
    },
    "fake020": {  # 一代宗师
        "title": "一代宗师", "year": 2013, "rating": 8.2,
        "duration": 111, "summary": "民国时期，咏春拳宗师叶问从佛山到香港，历经时代变迁，传承中华武术精神。",
        "genres": ["剧情", "动作", "传记"], "countries": ["中国大陆", "中国香港"], "languages": ["汉语普通话", "粤语"],
        "directors": [{"douban_id": "fp002", "name": "王家卫", "role": "director"}],
        "writers": [{"douban_id": "fp002", "name": "王家卫", "role": "writer"}],
        "actors": [{"douban_id": "1006583", "name": "梁朝伟", "role_name": "叶问"},
                    {"douban_id": "fp041", "name": "章子怡", "role_name": "宫二"}],
    },
    "fake021": {  # 重庆森林
        "title": "重庆森林", "year": 1994, "rating": 8.8,
        "duration": 102, "summary": "两个独立的故事：失恋警察223与神秘女毒贩擦肩而过，快餐店女店员阿菲暗恋警察663。",
        "genres": ["剧情", "爱情"], "countries": ["中国香港"], "languages": ["粤语", "汉语普通话"],
        "directors": [{"douban_id": "fp002", "name": "王家卫", "role": "director"}],
        "writers": [{"douban_id": "fp002", "name": "王家卫", "role": "writer"}],
        "actors": [{"douban_id": "1006583", "name": "梁朝伟", "role_name": "警察663"},
                    {"douban_id": "fp044", "name": "王菲", "role_name": "阿菲"},
                    {"douban_id": "fp045", "name": "金城武", "role_name": "警察223"}],
    },
    "fake022": {  # 花样年华
        "title": "花样年华", "year": 2000, "rating": 8.8,
        "duration": 98, "summary": "1962年香港，报社编辑周慕云与邻居苏丽珍发现各自的配偶有婚外情，两人在接触中暗生情愫。",
        "genres": ["剧情", "爱情"], "countries": ["中国香港"], "languages": ["粤语", "上海话"],
        "directors": [{"douban_id": "fp002", "name": "王家卫", "role": "director"}],
        "writers": [{"douban_id": "fp002", "name": "王家卫", "role": "writer"}],
        "actors": [{"douban_id": "1006583", "name": "梁朝伟", "role_name": "周慕云"},
                    {"douban_id": "fp042", "name": "张曼玉", "role_name": "苏丽珍"}],
    },
    "fake023": {  # 色戒
        "title": "色戒", "year": 2007, "rating": 8.7,
        "duration": 157, "summary": "抗战时期，女学生王佳芝奉命色诱汉奸易先生以行刺杀，却在情感与使命之间陷入两难。",
        "genres": ["剧情", "爱情", "情色"], "countries": ["中国台湾", "中国大陆", "美国"], "languages": ["汉语普通话", "粤语", "日语"],
        "directors": [{"douban_id": "fp001", "name": "李安", "role": "director"}],
        "actors": [{"douban_id": "1006583", "name": "梁朝伟", "role_name": "易先生"},
                    {"douban_id": "fp046", "name": "汤唯", "role_name": "王佳芝"}],
    },
    "fake024": {  # 那些年，我们一起追的女孩
        "title": "那些年，我们一起追的女孩", "year": 2011, "rating": 8.1,
        "duration": 110, "summary": "柯景腾和几个好友同时喜欢上了班里最优秀的女生沈佳宜，青春在欢笑和泪水中悄然流逝。",
        "genres": ["剧情", "喜剧", "爱情"], "countries": ["中国台湾"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp016", "name": "九把刀", "role": "director"}],
        "actors": [{"douban_id": "fp047", "name": "柯震东", "role_name": "柯景腾"},
                    {"douban_id": "fp048", "name": "陈妍希", "role_name": "沈佳宜"}],
    },
    "fake025": {  # 海角七号
        "title": "海角七号", "year": 2008, "rating": 7.6,
        "duration": 129, "summary": "小镇恒春要举办日本歌手演唱会，失意歌手阿嘉被拉来组建暖场乐队，一封寄往六十年前的情书牵动着每个人的心。",
        "genres": ["剧情", "喜剧", "爱情"], "countries": ["中国台湾"], "languages": ["汉语普通话", "日语"],
        "directors": [{"douban_id": "fp017", "name": "魏德圣", "role": "director"}],
        "actors": [{"douban_id": "fp049", "name": "范逸臣", "role_name": "阿嘉"},
                    {"douban_id": "fp050", "name": "田中千绘", "role_name": "友子"}],
    },
    "fake026": {  # 大鱼海棠
        "title": "大鱼海棠", "year": 2016, "rating": 6.9,
        "duration": 105, "summary": "少女椿掌管海棠花，为报人类男孩鲲的救命之恩，不惜违背神界戒律将其灵魂化为大鱼送回人间。",
        "genres": ["剧情", "动画", "奇幻"], "countries": ["中国大陆"], "languages": ["汉语普通话"],
        "directors": [{"douban_id": "fp018", "name": "梁旋", "role": "director"},
                       {"douban_id": "fp051", "name": "张春", "role": "director"}],
    },
    "fake027": {  # 你的名字 (Your Name)
        "title": "你的名字。", "year": 2016, "rating": 8.5,
        "duration": 106, "summary": "东京少年泷和乡下少女三叶在梦中交换身体，由此展开跨越时空的追寻与相遇。",
        "genres": ["剧情", "爱情", "动画"], "countries": ["日本"], "languages": ["日语"],
        "directors": [{"douban_id": "fp003", "name": "新海诚", "role": "director"}],
        "writers": [{"douban_id": "fp003", "name": "新海诚", "role": "writer"}],
    },
    "fake028": {  # 寄生虫 (Parasite)
        "title": "寄生虫", "year": 2019, "rating": 8.8,
        "duration": 132, "summary": "贫困的金家四口通过伪装逐步渗透进富裕的朴家，两个家庭之间的寄生与被寄生关系最终引爆了不可挽回的冲突。",
        "genres": ["剧情", "喜剧", "惊悚"], "countries": ["韩国"], "languages": ["韩语", "英语"],
        "directors": [{"douban_id": "fp004", "name": "奉俊昊", "role": "director"}],
        "writers": [{"douban_id": "fp004", "name": "奉俊昊", "role": "writer"}],
        "actors": [{"douban_id": "fp052", "name": "宋康昊", "role_name": "金基泽"},
                    {"douban_id": "fp053", "name": "崔宇植", "role_name": "金基宇"}],
    },
    "fake029": {  # 绿皮书 (Green Book)
        "title": "绿皮书", "year": 2018, "rating": 8.9,
        "duration": 130, "summary": "1962年，意大利裔白人打手托尼为黑人钢琴家谢利当司机兼保镖，两人穿越种族歧视严重的美国南部巡回演出。",
        "genres": ["剧情", "喜剧", "传记"], "countries": ["美国", "中国大陆"], "languages": ["英语", "意大利语", "俄语"],
        "directors": [{"douban_id": "fp005", "name": "彼得·法雷里", "role": "director"}],
        "actors": [{"douban_id": "fp054", "name": "维果·莫腾森", "role_name": "托尼·利普"},
                    {"douban_id": "fp055", "name": "马赫沙拉·阿里", "role_name": "唐·谢利"}],
    },
    "fake030": {  # 何以为家 (Capernaum)
        "title": "何以为家", "year": 2018, "rating": 9.1,
        "duration": 126, "summary": "12岁男孩赞恩将父母告上法庭，罪名是'生下了我'，揭开了黎巴嫩底层儿童的悲惨生存境遇。",
        "genres": ["剧情"], "countries": ["黎巴嫩", "法国", "美国"], "languages": ["阿拉伯语", "阿姆哈拉语"],
        "directors": [{"douban_id": "fp006", "name": "娜丁·拉巴基", "role": "director"}],
        "actors": [{"douban_id": "fp056", "name": "赞恩·阿尔·拉菲亚", "role_name": "赞恩"}],
    },
    "fake031": {  # 小丑 (Joker)
        "title": "小丑", "year": 2019, "rating": 8.7,
        "duration": 122, "summary": "哥谭市的喜剧演员亚瑟·弗莱克在社会漠视与精神疾病的双重压迫下，一步步走向疯狂，化身为小丑。",
        "genres": ["剧情", "惊悚", "犯罪"], "countries": ["美国", "加拿大"], "languages": ["英语"],
        "directors": [{"douban_id": "fp007", "name": "托德·菲利普斯", "role": "director"}],
        "writers": [{"douban_id": "fp007", "name": "托德·菲利普斯", "role": "writer"}],
        "actors": [{"douban_id": "fp057", "name": "华金·菲尼克斯", "role_name": "亚瑟·弗莱克/小丑"},
                    {"douban_id": "1040510", "name": "罗伯特·德尼罗", "role_name": "莫瑞·富兰克林"}],
    },
}


def generate_full_dataset():
    """结合 Top250 列表数据和详情数据生成完整数据集"""
    top250_path = os.path.join(DATA_DIR, 'movies_top250.json')
    if not os.path.exists(top250_path):
        print(f"Warning: {top250_path} not found. Run the Top250 list scraper first.")
        return

    with open(top250_path, 'r', encoding='utf-8') as f:
        top250 = json.load(f)

    all_persons = {}
    movies_out = []
    persons_out = []
    used_details = set()

    for movie in top250:
        douban_id = movie.get('douban_id')
        if douban_id in MOVIE_DETAILS:
            used_details.add(douban_id)
            detail = MOVIE_DETAILS[douban_id]
            movie_full = {
                'douban_id': douban_id,
                'title': detail['title'],
                'year': detail['year'],
                'rating': detail['rating'],
                'duration': detail['duration'],
                'summary': detail['summary'],
                'poster_url': movie.get('pic_url'),
                'genres': detail.get('genres', []),
                'countries': detail.get('countries', []),
                'languages': detail.get('languages', []),
                'directors': detail.get('directors', []),
                'writers': detail.get('writers', []),
                'actors': detail.get('actors', []),
                'related_movie_ids': [],
            }
            movies_out.append(movie_full)

            # 收集所有人物
            for person_list in [detail.get('directors', []), detail.get('writers', []), detail.get('actors', [])]:
                for p in person_list:
                    pid = p.get('douban_id')
                    if pid and pid not in all_persons:
                        all_persons[pid] = {'douban_id': pid, 'name': p['name']}
        else:
            # 不在详情数据库中的电影，只有基本信息
            movie_full = {
                'douban_id': douban_id,
                'title': movie['title'],
                'year': None,
                'rating': movie['rating'],
                'duration': None,
                'summary': '',
                'poster_url': movie.get('pic_url'),
                'genres': [],
                'countries': [],
                'languages': [],
                'directors': [],
                'writers': [],
                'actors': [],
                'related_movie_ids': [],
            }
            movies_out.append(movie_full)

    # 添加 Top250 列表中未覆盖的 MOVIE_DETAILS 条目（使用假 ID 的电影）
    for douban_id, detail in MOVIE_DETAILS.items():
        if douban_id not in used_details:
            movie_full = {
                'douban_id': douban_id,
                'title': detail['title'],
                'year': detail['year'],
                'rating': detail['rating'],
                'duration': detail['duration'],
                'summary': detail['summary'],
                'poster_url': detail.get('poster_url'),
                'genres': detail.get('genres', []),
                'countries': detail.get('countries', []),
                'languages': detail.get('languages', []),
                'directors': detail.get('directors', []),
                'writers': detail.get('writers', []),
                'actors': detail.get('actors', []),
                'related_movie_ids': [],
            }
            movies_out.append(movie_full)
            # 收集人物
            for person_list in [detail.get('directors', []), detail.get('writers', []), detail.get('actors', [])]:
                for p in person_list:
                    pid = p.get('douban_id')
                    if pid and pid not in all_persons:
                        all_persons[pid] = {'douban_id': pid, 'name': p['name']}

    # 为人物补充性别和出生年份信息
    PERSON_EXTRA = {
        "1048026": {"gender": "男", "birth_year": 1962, "birthplace": "中国香港", "alias": "Stephen Chow"},
        "1027903": {"gender": "男", "birth_year": 1963, "birthplace": "河北唐山", "alias": "Jiang Wen"},
        "1016771": {"gender": "男", "birth_year": 1953, "birthplace": "中国香港", "alias": "Ng Man-tat"},
        "1016751": {"gender": "女", "birth_year": 1950, "birthplace": "中国香港", "alias": "Yuen Qiu"},
        "1028689": {"gender": "男", "birth_year": 1952, "birthplace": "中国香港", "alias": "Yuen Wah"},
        "1006959": {"gender": "男", "birth_year": 1957, "birthplace": "北京", "alias": "Ge You"},
        "1016899": {"gender": "女", "birth_year": 1965, "birthplace": "辽宁沈阳", "alias": "Gong Li"},
        "1019053": {"gender": "女", "birth_year": 1971, "birthplace": "中国香港", "alias": "Athena Chu"},
        "1054424": {"gender": "男", "birth_year": 1961, "birthplace": "中国香港", "alias": "Andy Lau"},
        "1006583": {"gender": "男", "birth_year": 1962, "birthplace": "中国香港", "alias": "Tony Leung"},
        "1003494": {"gender": "男", "birth_year": 1956, "birthplace": "中国香港", "alias": "Leslie Cheung"},
        "1023514": {"gender": "男", "birth_year": 1956, "birthplace": "湖南长沙", "alias": "Zhang Fengyi"},
        "1054418": {"gender": "男", "birth_year": 1941, "birthplace": "日本东京", "alias": "Hayao Miyazaki"},
        "1023027": {"gender": "男", "birth_year": 1951, "birthplace": "陕西西安", "alias": "Zhang Yimou"},
        "1044899": {"gender": "男", "birth_year": 1955, "birthplace": "中国香港", "alias": "Chow Yun-fat"},
        "1054521": {"gender": "男", "birth_year": 1958, "birthplace": "美国", "alias": "Tim Robbins"},
        "1054534": {"gender": "男", "birth_year": 1937, "birthplace": "美国", "alias": "Morgan Freeman"},
        "1054450": {"gender": "男", "birth_year": 1956, "birthplace": "美国", "alias": "Tom Hanks"},
        "1010509": {"gender": "男", "birth_year": 1948, "birthplace": "摩洛哥卡萨布兰卡", "alias": "Jean Reno"},
        "1054434": {"gender": "男", "birth_year": 1970, "birthplace": "英国伦敦", "alias": "Christopher Nolan"},
        "1023045": {"gender": "男", "birth_year": 1952, "birthplace": "北京", "alias": "Chen Kaige"},
        "1022571": {"gender": "男", "birth_year": 1954, "birthplace": "加拿大", "alias": "James Cameron"},
        "1054419": {"gender": "男", "birth_year": 1939, "birthplace": "美国", "alias": "Francis Ford Coppola"},
        "1054452": {"gender": "男", "birth_year": 1940, "birthplace": "美国", "alias": "Al Pacino"},
        "1041029": {"gender": "男", "birth_year": 1974, "birthplace": "美国", "alias": "Leonardo DiCaprio"},
        "1048027": {"gender": "女", "birth_year": 1966, "birthplace": "美国", "alias": "Robin Wright"},
        "1041381": {"gender": "男", "birth_year": 1961, "birthplace": "中国香港", "alias": "Anthony Wong"},
        "1004439": {"gender": "男", "birth_year": 1953, "birthplace": "中国香港", "alias": "Eric Tsang"},
        "1047973": {"gender": "男", "birth_year": 1959, "birthplace": "法国", "alias": "Frank Darabont"},
        "1013847": {"gender": "男", "birth_year": 1958, "birthplace": "英国伦敦", "alias": "Gary Oldman"},
        "1054446": {"gender": "女", "birth_year": 1975, "birthplace": "英国", "alias": "Kate Winslet"},
        "1006956": {"gender": "男", "birth_year": 1974, "birthplace": "英国", "alias": "Christian Bale"},
        "1054435": {"gender": "男", "birth_year": 1962, "birthplace": "加拿大", "alias": "Jim Carrey"},
        "1040997": {"gender": "男", "birth_year": 1964, "birthplace": "黎巴嫩贝鲁特", "alias": "Keanu Reeves"},
        "1054436": {"gender": "男", "birth_year": 1946, "birthplace": "美国俄亥俄州辛辛那提", "alias": "Steven Spielberg"},
        "1017937": {"gender": "男", "birth_year": 1962, "birthplace": "美国科罗拉多州丹佛", "alias": "David Fincher"},
        "1022789": {"gender": "男", "birth_year": 1932, "birthplace": "捷克恰斯拉夫", "alias": "Milos Forman"},
        "1054431": {"gender": "男", "birth_year": 1969, "birthplace": "美国马萨诸塞州波士顿", "alias": "Edward Norton"},
        "1041033": {"gender": "女", "birth_year": 1977, "birthplace": "美国加利福尼亚州", "alias": "Jessica Chastain"},
        "1048167": {"gender": "女", "birth_year": 1987, "birthplace": "加拿大新斯科舍省哈利法克斯", "alias": "Elliot Page"},
        "1041000": {"gender": "男", "birth_year": 1943, "birthplace": "英国约克郡斯卡伯勒", "alias": "Ben Kingsley"},
        "1048168": {"gender": "女", "birth_year": 1934, "birthplace": "美国阿拉巴马州", "alias": "Louise Fletcher"},
        "1049666": {"gender": "男", "birth_year": 1965, "birthplace": "美国", "alias": "Andrew Stanton"},
        "1041127": {"gender": "男", "birth_year": 1948, "birthplace": "美国加利福尼亚州", "alias": "Ben Burtt"},
        "1049505": {"gender": "女", "birth_year": 1978, "birthplace": "美国田纳西州孟菲斯", "alias": "Ginnifer Goodwin"},
        "1049791": {"gender": "男", "birth_year": 1900, "birthplace": "中国南京", "alias": "Wan Laiming"},
        "1016933": {"gender": "男", "birth_year": 1930, "birthplace": "中国江苏", "alias": "Lang Xiong"},
        "1040510": {"gender": "男", "birth_year": 1943, "birthplace": "美国纽约", "alias": "Robert De Niro"},
        "1041134": {"gender": "男", "birth_year": 1976, "birthplace": "英国伦敦", "alias": "Jonathan Nolan"},
        "fp001": {"gender": "男", "birth_year": 1954, "birthplace": "中国台湾屏东", "alias": "Ang Lee"},
        "fp002": {"gender": "男", "birth_year": 1958, "birthplace": "中国上海", "alias": "Wong Kar-wai"},
        "fp003": {"gender": "男", "birth_year": 1973, "birthplace": "日本长野县", "alias": "Makoto Shinkai"},
        "fp004": {"gender": "男", "birth_year": 1969, "birthplace": "韩国大邱", "alias": "Bong Joon-ho"},
        "fp005": {"gender": "男", "birth_year": 1956, "birthplace": "美国宾夕法尼亚州", "alias": "Peter Farrelly"},
        "fp006": {"gender": "女", "birth_year": 1974, "birthplace": "黎巴嫩", "alias": "Nadine Labaki"},
        "fp007": {"gender": "男", "birth_year": 1970, "birthplace": "美国纽约", "alias": "Todd Phillips"},
        "fp008": {"gender": "男", "birth_year": 1980, "birthplace": "中国四川泸州", "alias": "Jiao Zi"},
        "fp009": {"gender": "男", "birth_year": 1980, "birthplace": "中国山东济宁", "alias": "Guo Fan"},
        "fp010": {"gender": "男", "birth_year": 1974, "birthplace": "中国北京", "alias": "Wu Jing"},
        "fp011": {"gender": "男", "birth_year": 1965, "birthplace": "中国香港", "alias": "Dante Lam"},
        "fp012": {"gender": "男", "birth_year": 1985, "birthplace": "中国江西", "alias": "Wen Muye"},
        "fp013": {"gender": "男", "birth_year": 1979, "birthplace": "中国香港", "alias": "Derek Tsang"},
        "fp014": {"gender": "女", "birth_year": 1982, "birthplace": "中国湖北襄阳", "alias": "Jia Ling"},
        "fp015": {"gender": "男", "birth_year": 1950, "birthplace": "中国广东广州", "alias": "Tsui Hark"},
        "fp016": {"gender": "男", "birth_year": 1978, "birthplace": "中国台湾", "alias": "Giddens Ko"},
        "fp017": {"gender": "男", "birth_year": 1968, "birthplace": "中国台湾台南", "alias": "Wei Te-sheng"},
        "fp018": {"gender": "男", "birth_year": 1982, "birthplace": "中国江西", "alias": "Liang Xuan"},
        "fp019": {"gender": "男", "birth_year": 1969, "birthplace": "美国得克萨斯州", "alias": "Matthew McConaughey"},
        "fp020": {"gender": "女", "birth_year": 1982, "birthplace": "美国纽约布鲁克林", "alias": "Anne Hathaway"},
        "fp021": {"gender": "男", "birth_year": 1981, "birthplace": "美国加利福尼亚州洛杉矶", "alias": "Joseph Gordon-Levitt"},
        "fp022": {"gender": "男", "birth_year": 1952, "birthplace": "北爱尔兰巴利米纳", "alias": "Liam Neeson"},
        "fp023": {"gender": "男", "birth_year": 1963, "birthplace": "美国俄克拉何马州", "alias": "Brad Pitt"},
        "fp024": {"gender": "男", "birth_year": 1937, "birthplace": "美国新泽西州", "alias": "Jack Nicholson"},
        "fp025": {"gender": "男", "birth_year": 1968, "birthplace": "美国", "alias": "Byron Howard"},
        "fp026": {"gender": "男", "birth_year": 1963, "birthplace": "美国", "alias": "Rich Moore"},
        "fp027": {"gender": "男", "birth_year": 1994, "birthplace": "中国四川眉山", "alias": "Qu Chuxiao"},
        "fp028": {"gender": "男", "birth_year": 1981, "birthplace": "中国河南", "alias": "Li Guangjie"},
        "fp029": {"gender": "男", "birth_year": 1965, "birthplace": "美国纽约", "alias": "Frank Grillo"},
        "fp030": {"gender": "男", "birth_year": 1978, "birthplace": "中国黑龙江哈尔滨", "alias": "Zhang Yi"},
        "fp031": {"gender": "男", "birth_year": 1992, "birthplace": "中国辽宁丹东", "alias": "Huang Jingyu"},
        "fp032": {"gender": "男", "birth_year": 1972, "birthplace": "中国上海", "alias": "Xu Zheng"},
        "fp033": {"gender": "男", "birth_year": 1985, "birthplace": "中国上海", "alias": "Wang Chuanjun"},
        "fp034": {"gender": "女", "birth_year": 1983, "birthplace": "中国黑龙江", "alias": "Tan Zhuo"},
        "fp035": {"gender": "女", "birth_year": 1992, "birthplace": "中国河北石家庄", "alias": "Zhou Dongyu"},
        "fp036": {"gender": "男", "birth_year": 2000, "birthplace": "中国湖南怀化", "alias": "Yi Yangqianxi"},
        "fp037": {"gender": "女", "birth_year": 1986, "birthplace": "中国辽宁鞍山", "alias": "Zhang Xiaofei"},
        "fp038": {"gender": "男", "birth_year": 1979, "birthplace": "中国黑龙江齐齐哈尔", "alias": "Shen Teng"},
        "fp039": {"gender": "女", "birth_year": 1968, "birthplace": "中国台湾", "alias": "Wu Chien-lien"},
        "fp040": {"gender": "女", "birth_year": 1962, "birthplace": "马来西亚怡保", "alias": "Michelle Yeoh"},
        "fp041": {"gender": "女", "birth_year": 1979, "birthplace": "中国北京", "alias": "Zhang Ziyi"},
        "fp042": {"gender": "女", "birth_year": 1964, "birthplace": "中国香港", "alias": "Maggie Cheung"},
        "fp043": {"gender": "男", "birth_year": 1963, "birthplace": "中国北京", "alias": "Jet Li"},
        "fp044": {"gender": "女", "birth_year": 1969, "birthplace": "中国北京", "alias": "Faye Wong"},
        "fp045": {"gender": "男", "birth_year": 1973, "birthplace": "日本东京", "alias": "Takeshi Kaneshiro"},
        "fp046": {"gender": "女", "birth_year": 1979, "birthplace": "中国浙江杭州", "alias": "Tang Wei"},
        "fp047": {"gender": "男", "birth_year": 1991, "birthplace": "中国台湾", "alias": "Ko Chen-tung"},
        "fp048": {"gender": "女", "birth_year": 1983, "birthplace": "中国台湾", "alias": "Michelle Chen"},
        "fp049": {"gender": "男", "birth_year": 1978, "birthplace": "中国台湾", "alias": "Fan Van-chen"},
        "fp050": {"gender": "女", "birth_year": 1981, "birthplace": "日本东京", "alias": "Chie Tanaka"},
        "fp051": {"gender": "男", "birth_year": 1978, "birthplace": "中国福建", "alias": "Zhang Chun"},
        "fp052": {"gender": "男", "birth_year": 1967, "birthplace": "韩国庆尚南道", "alias": "Song Kang-ho"},
        "fp053": {"gender": "男", "birth_year": 1990, "birthplace": "韩国首尔", "alias": "Choi Woo-shik"},
        "fp054": {"gender": "男", "birth_year": 1958, "birthplace": "美国纽约", "alias": "Viggo Mortensen"},
        "fp055": {"gender": "男", "birth_year": 1974, "birthplace": "美国加利福尼亚州奥克兰", "alias": "Mahershala Ali"},
        "fp056": {"gender": "男", "birth_year": 2004, "birthplace": "叙利亚德拉", "alias": "Zain Al Rafeea"},
        "fp057": {"gender": "男", "birth_year": 1974, "birthplace": "波多黎各圣胡安", "alias": "Joaquin Phoenix"},
    }

    for pid, person in all_persons.items():
        extra = PERSON_EXTRA.get(pid, {})
        person.update(extra)
        person.setdefault('gender', None)
        person.setdefault('birth_year', None)
        person.setdefault('birthplace', None)
        person.setdefault('alias', None)
        persons_out.append(person)

    # 保存
    movies_path = os.path.join(DATA_DIR, 'movies.jsonl')
    persons_path = os.path.join(DATA_DIR, 'persons.jsonl')

    with open(movies_path, 'w', encoding='utf-8') as f:
        for m in movies_out:
            f.write(json.dumps(m, ensure_ascii=False) + '\n')

    with open(persons_path, 'w', encoding='utf-8') as f:
        for p in persons_out:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')

    print(f'Generated {len(movies_out)} movies -> {movies_path}')
    print(f'Generated {len(persons_out)} persons -> {persons_path}')

    # 统计
    genres = set()
    for m in movies_out:
        for g in m.get('genres', []):
            genres.add(g)
    print(f'Unique genres: {len(genres)} - {sorted(genres)}')
    movies_with_data = sum(1 for m in movies_out if m['genres'] or m['directors'])
    print(f'Movies with full detail: {movies_with_data}/{len(movies_out)}')
    print('Done!')


if __name__ == '__main__':
    generate_full_dataset()
