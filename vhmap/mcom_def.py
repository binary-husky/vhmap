import os

fn_names = [
    "v3d_object", "flash", "plot", "figure", "hold", "box", "pause", "clf", "xlim", "ylim", "xlabel", 
    "ylabel", "drawnow", "v2d", "v3d_init", "v3d_init", "v2L", "title", "plot3", "grid", "v3dx", "v3d_show", 
    "v3d_pop", "v3d_line_object", "v3d_clear", "v3d_add_terrain", "set_style", "set_env", "use_geometry", 
    "rec_disable_percentile_clamp", "rec_enable_percentile_clamp",
    "geometry_rotate_scale_translate", "test_function_terrain", 'line3d', 'advanced_geometry_rotate_scale_translate',
    "advanced_geometry_material", "skip"
]
align_names = [
    ('初始化3D', 'v3d_init'),
    ('设置样式', 'set_style'),
    ('形状之旋转缩放和平移','geometry_rotate_scale_translate'),
    ('其他几何体之旋转缩放和平移','advanced_geometry_rotate_scale_translate'),
    ('其他几何体之材质','advanced_geometry_material'),
    ('发送几何体','v3d_object'),
    ('结束关键帧','v3d_show'),
    ('发送线条','line3d'),
    ('发射光束','flash'),
    ('空指令','skip'),
]

def find_where_to_log(path):
    if not os.path.exists(path): os.makedirs(path)

    def find_previous_start_end():
        start = None; end = None; t = 0
        while True:
            is_body = os.path.exists(path + '/mcom_buffer_%d.txt' % t)
            is_head = os.path.exists(path + '/mcom_buffer_%d____starting_session.txt' % t)
            if is_head: start = t
            if is_head or is_body: end = t; t += 1
            else:
                new = t
                return (start, end, new)

    prev_start, prev_end, new = find_previous_start_end()
    return prev_start, prev_end, new

