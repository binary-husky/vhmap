# Visual Hybrid Multi-Agent Playground (VHMAP 使用说明书)

vhmap是一个基于ThreeJs+Python的开源项目，提供了一个简洁易用的Python接口，用于创建和控制3D场景的可视化工具。它适用于**科研**、多智能体强化学习领域的3D演示、娱乐等应用。vhmap具有以下特点：

简化的Python接口；客户端渲染，流畅的帧率；占用服务端资源极少；基于ThreeJs，支持拖动和手机触屏；支持透视和投影两种视图切换；支持回放；使用zlib压缩数据流，网络带宽需求小。

通过以上特点，vhmap为用户提供了一个简单高效、具有交互性的3D可视化解决方案。

## 2D绘图使用说明书

```
import numpy as np
import time
from config import GlobalConfig; GlobalConfig.logdir = 'live_image'

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
