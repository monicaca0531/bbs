# encoding: utf-8

import random
from PIL import Image, ImageDraw, ImageFont
import string

class Captcha(object):
    # 生成几位数的验证码
    number = 4
    # 验证码图片的宽度和高度
    size = (100,30)
    # 验证码字体大小
    frontsize = 25
    # 加入干扰线的条数
    line_number = 2

    # 构建一个验证码源文件
    SOURCE = list(string.ascii_letters)
    for index in range(0,10):
        SOURCE.append(str(index))

    # 生成随机的颜色
    @classmethod
    def __gene_random_color(cls,start=0,end=255):
        # random.seed()
        return (random.randint(start,end),random.randint(start,end),random.randint(start,end))

    # 随机选择一种字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'Courgette-Regular.ttf',
            'LHANDW.TTF',
            'Lobster-Regular.ttf',
            'verdana.ttf'
        ]
        font = random.choice(fonts)
        return 'utils/captcha/'+font

    # 随机生成字符串
    @classmethod
    def gene_text(cls, number):
        return ''.join(random.sample(cls.SOURCE,number))

    # 绘制干扰线
    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0,width),random.randint(0,height))
        end = (random.randint(0,width),random.randint(0,height))
        draw.line([begin,end], fill=cls.__gene_random_color(),width=2)

    # 绘制干扰点
    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100,max(0,int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0,100)
                if tmp > 100 - chance:
                    draw.point((w,h),fill=cls.__gene_random_color())

    ### 生成验证码 ###
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片的宽和高
        width,height = cls.size
        # 创建图片
        image = Image.new('RGBA',(width,height),cls.__gene_random_color(0,100))
        # 验证码的字体
        font = ImageFont.truetype(cls.__gene_random_font(),cls.frontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text(cls.number)
        # 获取字体的尺寸
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(((width-font_width)/2, (height-font_height)/2),text,fill=cls.__gene_random_color(150,255),font=font)
        # 绘制干扰线
        for x in range(0,cls.line_number):
            cls.__gene_line(draw,width,height)
        # 制造噪点
        cls.__gene_points(draw,10,width,height)
        return (text,image)