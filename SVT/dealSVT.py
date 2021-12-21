import os
import sys
from PIL import Image
from xml.etree import ElementTree
 

def read_SVT_dataset(XML_src, image_dst):
    '''从xml文件中提出图片信息写入txt文件中
    @param XML_src: xml文件路径
    @param write_txt: 提取图片的信息
    @param image_src: 图片文件所在文件夹
    '''

    with open(XML_src) as f:
        tree = ElementTree.parse(f)
 
    lexs = []
    gts = []

    for node in tree.iter('image'):
        for row in node:
            if row.tag == 'imageName':
                name = row.text
                image = Image.open(name)

            elif row.tag == 'lex':
                lexs.append("{} {}".format(name[4:-4], row.text))

            elif row.tag == 'taggedRectangles':
                count = 0
                for each_taggedRec in row:
                    gt = each_taggedRec.find('tag').text
                    if len(gt) < 3 or not gt.isalnum():
                        continue

                    count = count + 1
                    sub_image_name = "{}_{}.png".format(name[4:-4], count)
                    gts.append("{} {}".format(sub_image_name, gt))

                    tmp_dict = each_taggedRec.attrib
                    x = int(tmp_dict['x'])
                    y =  int(tmp_dict['y'])
                    height = int(tmp_dict['height'])
                    width = int(tmp_dict['width'])
                    crop_img = image.crop([x, y, x + width, y + height])
                    crop_img.save("{}/{}".format(image_dst, sub_image_name))

  
    
    with open("gt.txt", "w") as f:
        f.write("\n".join(gts))
    
    with open("lex.txt", "w") as f:
        f.write("\n".join(lexs))
    

 
 
if __name__ == '__main__':
    read_SVT_dataset('test.xml', "image")