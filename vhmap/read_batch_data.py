
import os
import socket
import time
import traceback
import numpy as np
from colorama import init; init()
from multiprocessing import Process, Pipe

def get_files_to_read(base_path):
    starting_file_index = -1
    ending_file_index = -1
    pointer = 0
    while True:
        es = os.path.exists(base_path+'/mcom_buffer_%d____starting_session.txt'%pointer)
        ee = os.path.exists(base_path+'/mcom_buffer_%d.txt'%pointer)
        if (not es) and (not ee): break
        assert not (ee and es), ('?')
        if es: starting_file_index = pointer; ending_file_index = pointer
        if ee: ending_file_index = pointer
        pointer += 1
        assert pointer < 1e3
    assert starting_file_index>=0 and ending_file_index>=0, ('查找日志失败:', base_path)

    file_path = []
    for i in range(starting_file_index, ending_file_index+1):
        if i==starting_file_index: file_path.append(base_path+'/mcom_buffer_%d____starting_session.txt'%i)
        else: file_path.append(base_path+'/mcom_buffer_%d.txt'%i)
        assert os.path.exists(file_path[0]), ('?')
    return file_path

def read_experiment(base_path):
    files_to_read = get_files_to_read(base_path)
    cmd_lines = []
    for file in files_to_read:
        f = open(file, 'r')
        lines = f.readlines()
        cmd_lines.extend(lines)
    dictionary = {}

    def rec(value,name): 
        if name not in dictionary:
            dictionary[name] = []
        dictionary[name].append(value)
        return

    for cmd_str in cmd_lines:
        if '>>' in cmd_str:
            cmd_str_ = cmd_str[2:].strip('\n')
            if not cmd_str_.startswith('rec('): continue
            eval('%s'%cmd_str_)
    return dictionary

def stack_cutlong(arr_list, min_len=None):
    if min_len is None:
        min_len = min([len(item) for item in arr_list])
    print([len(item) for item in arr_list],'\tselect:', min_len)
    return np.stack([item[:min_len] for item in arr_list])


def smooth(data, sm=1):
    if sm > 1:
        y = np.ones(sm)*1.0/sm
        d = np.convolve(y, data, 'valid')#"same")
    else:
        d = data
    return np.array(d)


def tsplot(ax, data, label, resize_x, smooth_level=None, **kw):
    if smooth_level is not None:
        print('警告 smooth_level=',smooth_level)
        data = smooth(data, smooth_level)

    print('警告 resize_x=',resize_x)
    x = np.arange(data.shape[1])
    x = resize_x*x
    est = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    cis = (est - sd, est + sd)
    ax.fill_between(x,cis[0],cis[1],alpha=0.4, **kw)
    ax.plot(x,est, linewidth=1.5, label=label, **kw)
    ax.margins(x=0)







def read_party(party):
    import sys
    if sys.platform.startswith('win'):
        for ex in party:
            for i, path in enumerate(ex['path']):
                ex['path'][i] =  ex['path'][i].replace(':','_')

    for ex in party:
        for i, path in enumerate(ex['path']):
            ex['path'][i] =  ex['path'][i]

    for ex in party:
        pathes = ex['path']
        for path in pathes:
            ex['readings of %s'%path] = read_experiment(path)
            print('readings of %s'%path)

    return party


def feed_sample(party, samples, sample_metas, smooth_level = 1, drop_data = 0, x_shift=None, key_pairs=None, max_x=None, x_axis_name='Episodes'):
    def shift_x(x):
        return x * x_shift
    
    def get_ydata(key_pair):
        main_key = key_pair['main_key']
        ydata = ex[f'readings of {path}'][main_key]
        ydata = np.array(ydata)
        if smooth_level is not None:
            ydata = smooth(ydata, smooth_level); print(f'警告, 平滑系数smooth_level={smooth_level}')
        return ydata
    

    for ex in party:
        for path in ex['path']:
            read_ydata_arr = []
            for key_pair in key_pairs:
                read_ydata_arr.append(get_ydata(key_pair))
            ydata_arr_len = [len(a) for a in read_ydata_arr]
            ydata_arr_len_max = max(ydata_arr_len)
            for t in range(ydata_arr_len_max):
                if (drop_data is not None) and (drop_data!=0) and (not t%drop_data==0): continue
                if (max_x is not None) and (shift_x(t) > max_x): continue
                for i, key_pair in enumerate(key_pairs):
                    main_key_name_on_graph = key_pair['graph_key']
                    tag = key_pair['tag']
                    tag_value = key_pair['tag_value']
                    sample_fragment = {
                        x_axis_name: shift_x(t),
                        tag: tag_value,
                        'Method':ex['Method'],
                    }
                    sample_fragment.update({
                        main_key_name_on_graph: read_ydata_arr[i][t]
                    })
                    samples.append(sample_fragment)
    return samples, sample_metas