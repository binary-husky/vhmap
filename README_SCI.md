# Visual Hybrid Multi-Agent Playground (VHMAP 使用说明书)

vhmap是一个基于ThreeJs+Python的开源项目，提供了一个简洁易用的Python接口，用于创建和控制3D场景的可视化工具。它适用于**科研**、多智能体强化学习领域的3D演示、娱乐等应用。vhmap具有以下特点：

简化的Python接口；客户端渲染，流畅的帧率；占用服务端资源极少；基于ThreeJs，支持拖动和手机触屏；支持透视和投影两种视图切换；支持回放；使用zlib压缩数据流，网络带宽需求小。

通过以上特点，vhmap为用户提供了一个简单高效、具有交互性的3D可视化解决方案。


## 安装
```shell
pip install vhmap>=4.2
```


## 2D数据采集与实时绘图

![2023-12-21_17-31-46-crop mkv](https://github.com/binary-husky/vhmap/assets/96192199/54a990ad-3756-477c-88e7-c296d30723b1)

```python
import numpy as np
import time
from vhmap.config import GlobalConfig; GlobalConfig.logdir = 'live_image'

""" 
没有时间轴
"""
def main():
    from vhmap.mcom import mcom
    visual_bridge = mcom(path='TEMP/v2d_logger/', draw_mode='Img')
    for you_experiment_at_time_step_t in range(1000):
        t = you_experiment_at_time_step_t
        visual_bridge.rec(value=np.sin(t/10), name='sin')
        visual_bridge.rec(value=np.cos(t/10), name='cos')
        visual_bridge.rec_show()    # 绘制
        time.sleep(0.3)


""" 
有时间轴
"""
def main():
    from vhmap.mcom import mcom
    visual_bridge = mcom(path='TEMP/v2d_logger/', draw_mode='Img')
    for you_experiment_at_time_step_t in range(1000):
        t = you_experiment_at_time_step_t
        visual_bridge.rec(value=t/10, name='time')
        visual_bridge.rec(value=np.sin(t/10), name='sin')
        visual_bridge.rec(value=np.cos(t/20), name='cos')
        visual_bridge.rec_show()    # 绘制
        time.sleep(0.3)


""" 
分组对比
"""
def main():
    from vhmap.mcom import mcom
    visual_bridge = mcom(path='TEMP/v2d_logger/', draw_mode='Img')
    for you_experiment_at_time_step_t in range(1000):
        t = you_experiment_at_time_step_t
        visual_bridge.rec(value=np.sin(t/10), name='sin of=10')
        visual_bridge.rec(value=np.sin(t/15), name='sin of=15')
        visual_bridge.rec(value=np.sin(t/20), name='sin of=20')
        visual_bridge.rec(value=np.cos(t/20), name='cos of=20')
        visual_bridge.rec(value=np.cos(t/50), name='cos of=50')
        visual_bridge.rec_show()    # 绘制
        time.sleep(0.3)

if __name__ == '__main__':
    main()
```


## 数据后处理（seaborn）

```python
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

```



