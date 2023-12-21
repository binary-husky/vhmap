import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from vhmap.read_batch_data import read_party, feed_sample
from vhmap.seaborn_defaults import init, roll_color_palette, legend


party = [
    {
        "Method": "Model 1",
        "path": [
            "TEMP/v2d_logger",
            # "TEMP2/v2d_logger",
            # "TEMP3/v2d_logger",
        ]
    },
    # {
    #     "Method": "Model 2",
    #     "path": [
    #         ...
    #     ]
    # },
]


party = read_party(party)
sample_metas = []
samples = []
x_axis_name = 'x axis name'
key_pairs = [
    {'main_key':'sin of=10', 'graph_key':'score', 'tag':'tag', 'tag_value': 'tag_value'},
]



# 读取数据
samples, sample_metas = feed_sample(party, samples, sample_metas, smooth_level=0, 
                                    drop_data = 0, x_shift=1, key_pairs=key_pairs, 
                                    max_x=None, x_axis_name=x_axis_name)



pd_sample = pd.DataFrame(samples)
init(font_scale=2)
palette = sns.color_palette("husl", 3)
fig, axes = plt.subplots(1, 1, sharex=True, figsize=(10,10))

res1 = sns.lineplot(ax=axes, data=pd_sample, x=x_axis_name, y=key_pairs[0]['graph_key'], hue="Method")

legend(res1,水平位置百分比=0.8, 垂直位置百分比=0.7, 边框=True, 字体大小=15)
changedNameOfImage = True
path = './static_image/'
if not os.path.exists(path): os.makedirs(path)

nameOfImage = "final"
assert changedNameOfImage
plt.savefig('%s/%s.jpg'%(path,nameOfImage),bbox_inches='tight')
plt.savefig('%s/%s.pdf'%(path,nameOfImage),bbox_inches='tight')
print('finish!')