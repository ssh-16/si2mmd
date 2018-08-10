import hashlib
import os

class Function:
    def __init__(self, name="root", file_type='X', file_name="", fold_level=-1):
        self.name = name
        self.file_type = file_type
        self.file_name = file_name
        self.fold_level = fold_level
        self.id = hashlib.sha1((name + ' ' + file_name).encode()).hexdigest()
        self.childs = []
    def IdToString(self):
        return self.ShortNameWithType()
        #ret = 'id' + str(self.id)
        #return ret
    def AddChild(self, node):
        #if self.id != node.id:
        if not node in self.childs:
            self.childs.append(node)
    def ShortName(self):
        names = self.name.split('::')
        return names[-1]
    def ShortNameWithType(self):
        return self.ShortName() + '_' + self.file_type

def PrintTreeSub(root, output, drawed):
    if root.file_type == 'X':
        for child in root.childs:
            root_id = root.IdToString()
            child_id = child.IdToString()
            if not (root_id + '_to_' + child_id) in drawed:
                if root_id != child_id and root.ShortName() != 'root' and \
                        child.file_type == 'X':
                    output.writelines('    %s --> %s\n' % (root_id, child_id))
                drawed[(root_id + '_to_' + child_id)] = 1
                PrintTreeSub(child, output, drawed)

def PrintTree(root, output):
    drawed = dict()
    PrintTreeSub(root, output, drawed)

MAX_LINE_LENGTH = 2048

def ReadFile(filename, output):
    file = open(filename, 'r')
    root = Function()
    # output.writelines('    %s[%s]\n' % (root.IdToString(), root.ShortName()))
    stack = [root]
    occured = dict()
    while True:
        line = file.readline(MAX_LINE_LENGTH)
        if not line:
            break
        fold_level = 0
        while line[fold_level] == '\t':
            fold_level += 1
        [name, file_name, dir_name] = line.split()
        if file_name[-1] == 'h':
            file_type = 'H'
        else:
            file_type = 'X'
        node = Function(name, file_type, file_name, fold_level)
        while len(stack) > 0 and fold_level <= stack[-1].fold_level:
            stack.pop()
        parent = stack[-1]
        parent.AddChild(node)
        stack.append(node)
        #print('%d: %s\t%s\t%s\t%s' % (fold_level, file_type, name, file_name, node.GetId()))
        if not node.ShortName() in occured:
            output.writelines('    %s[%s]\n' % (node.IdToString(), node.ShortName()))
            occured[node.ShortName()] = 1
    file.close()
    return root

if __name__ == "__main__":
    function_names = ['A', 'B']
    current_dir = 'D:/Desktop/'
    for function_name in function_names:
        filename = current_dir + function_name + '.txt'
        outputfile = current_dir + function_name + '.mmd'
        output = open(outputfile, 'w')
        output.writelines('graph LR\n')
        root = ReadFile(filename, output)
        output.writelines('\n')
        PrintTree(root, output)
        output.close()
        cmd = 'mmdc -i ' + outputfile + ' -o ' + current_dir + function_name + '.png' + ' -w 2048'
        os.system(cmd)
