'''
读取in_file文件，将代码块转为python格式代码块
如果python代码块中有包含 Out[] 格式的jupyter notebook输出，则将其单独作为一个代码块，采用java的高亮 
'''

def split_out(in_file, out_file):

    with open(in_file, 'r', encoding = 'utf8') as fin:
        lines = fin.readlines()

    with open(out_file, 'w', encoding = 'utf8') as fout:
        block_flag = True  # 为True，则遇到```说明是代码块的开头，要加python
        
        out_flag = False  # 为False说明未对jupyter notebook的Out做切割，不用担心后面跟的有In[]
        for i,line in enumerate(lines):
            
            # 为代码段加python标签 
            if '```' in line:
                if block_flag:
                    lines[i] = line.replace('```','```python')
                else:
                    out_flag = False  # 代码块结束，自动复原
                block_flag = not block_flag
                # print(block_flag)

            # 为jupyter notebook 的output修改，保证输出好看
            # 只将多行的Out做修改
            if re.match(r'^Out\[(\d+)\]: $', line):
                lines[i] = '```\n\n```java\n'+line
                out_flag = True # 标记有Out做切割，后面如果有In[]，则要重开代码块
            
            if 'In [' in line and out_flag == True:
                lines[i] = '```\n\n```python\n'+line
                out_flag = False

        fout.write(''.join(lines))
