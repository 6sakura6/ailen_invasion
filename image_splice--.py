# 图片拼接
import PIL.Image as Image

IMAGE_SIZE = 100 # 图片大小
IMAGE_PATH = 'images/big_ship_image.bmp' # 拼接成功后所保存的路径

# 将所要拼接的所有图片按顺序组成一个列表
image_names = ['images/ship02.bmp', 'images/shop02_left_five_point.bmp',
               'images/ship02.bmp', 'images/shop02_right_five_point.bmp',
               'images/ship02.bmp', 'images/shop02_down_three_point.bmp']

# 拼接函数
def image_compose():
    # 首先创建一个空白的长条图片以供我们的图片覆盖在这上面
    # 创建一个长为len(image_names) * IMAGE_SIZE， 宽为IMAGE_SIZE的图片
    to_image = Image.new('RGB', (len(image_names) * IMAGE_SIZE, IMAGE_SIZE))
    i = 0# 用来遍历列表
    for image in image_names:
        # 逐一打开列表中的图片
        # resize用来调整打开的图片的大小 Image.Resampling.LANCZOS表示抗锯齿
        from_image = Image.open(image).resize((IMAGE_SIZE, IMAGE_SIZE),
                                              Image.Resampling.LANCZOS)
        # paste表示覆盖，from_image是本次覆盖的图片
        # (i * IMAGE_SIZE, 0)是覆盖的区域
        to_image.paste(from_image, (i * IMAGE_SIZE, 0))
        i += 1
    # 返回一张保存的图片
    return to_image.save(IMAGE_PATH)

if __name__ == '__main__':
    image_compose()  # 调用函数