
# -*- coding: UTF-8 -*-



class Node:
    # 定义树，包括值和左右子点
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def one_expression_tree(operators, operands):
    root_node = Node(operators[0])
    operator1 = Node(operators[1])
    operator2 = Node(operators[2])
    operand0 = Node(operands[0])
    operand1 = Node(operands[1])
    operand2 = Node(operands[2])
    operand3 = Node(operands[3])
    root_node.left = operator1
    root_node.right =operand0
    operator1.left = operator2
    operator1.right = operand1
    operator2.left = operand2
    operator2.right = operand3
    return root_node

def two_expression_tree(operators, operands):
    root_node = Node(operators[0])
    operator1 = Node(operators[1])
    operator2 = Node(operators[2])
    operand0 = Node(operands[0])
    operand1 = Node(operands[1])
    operand2 = Node(operands[2])
    operand3 = Node(operands[3])
    root_node.left = operator1
    root_node.right =operator2
    operator1.left = operand0
    operator1.right = operand1
    operator2.left = operand2
    operator2.right = operand3
    return root_node



def perm(l):
    """
    # 获得一个列表的全排列
    递归思路，固定列表的第一个元素，后面的元素实现全排列
    :param l: l
    :return: l 的全排列
    """
    if len(l)<=1:
        return [l]
    r = []
    for i in range(len(l)):
        s = l[:i]+l[i+1:]
        p = perm(s)
        for x in p:
            r.append(l[i:i+1]+x)
    return r


def Calculate_Num2Num(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    else:
        return float(a)/float(b)


def Calculate_Tree(node):
    if node.left is None:
        return node.val
    return Calculate_Num2Num(Calculate_Tree(node.left), Calculate_Tree(node.right), node.val)


def midTraverse(node,LRD_list):
    if node.left != None:
        midTraverse(node.left,LRD_list)
    LRD_list.append(node.val)
    if node.right != None:
        midTraverse(node.right,LRD_list)
    return LRD_list


def PanChong_one(temp_node_list_one):
    # 去除重复的，比如 (((4+6)-2)*3) = 24 和 (((6+4)-2)*3) = 24
    Result_node_list = temp_node_list_one.copy()
    for ii in range(len(temp_node_list_one)):
        LRD_list = []
        temp_node = temp_node_list_one[ii]
        calculate_list = midTraverse(temp_node, LRD_list)
        if calculate_list[1] == "+" or calculate_list[1] == "*":
            for jj in range(ii+1, len(temp_node_list_one)):
                LRD_list = []
                calculate_list_com = midTraverse(temp_node_list_one[jj], LRD_list)
                if calculate_list[0] == calculate_list_com[2] and calculate_list[2] == calculate_list_com[0]:
                    Result_node_list.pop(jj)
    return Result_node_list


def PanChong_tow(temp_node_list_tow):
    # 去除重复的，比如 ((4*6)÷(3-2)) = 24 和 ((6*4)÷(3-2)) = 24
    Result_node_list = temp_node_list_tow.copy()
    for ii in range(len(temp_node_list_tow)):
        LRD_list = []
        temp_node = temp_node_list_tow[ii]
        calculate_list = midTraverse(temp_node, LRD_list)
        if calculate_list[3] == "+" or calculate_list[3] == "*":
            for jj in range(ii + 1, len(temp_node_list_tow)):
                LRD_list = []
                calculate_list_com = midTraverse(temp_node_list_tow[jj], LRD_list)
                if calculate_list[1] == calculate_list_com[-2] and \
                        calculate_list[-2] == calculate_list_com[1] and \
                        len(list(({calculate_list[0], calculate_list[2]}) ^ {calculate_list_com[-1], calculate_list_com[-3]})) == 0:
                    Result_node_list.pop(jj)
        else:
            if calculate_list[1] == "+" or calculate_list[1] == "*":
                for jj in range(ii + 1, len(temp_node_list_tow)):
                    LRD_list = []
                    calculate_list_com = midTraverse(temp_node_list_tow[jj], LRD_list)
                    if calculate_list[0] == calculate_list_com[2] and calculate_list[2] == calculate_list_com[0]:
                        Result_node_list.pop(jj)
            else:
                if calculate_list[-2] == "+" or calculate_list[-2] == "*":
                    for jj in range(ii + 1, len(temp_node_list_tow)):
                        LRD_list = []
                        calculate_list_com = midTraverse(temp_node_list_tow[jj], LRD_list)
                        if calculate_list[-3] == calculate_list_com[0] and calculate_list[0] == calculate_list_com[-3]:
                            Result_node_list.pop(jj)


def calculate(nums):
    nums_possible = perm(nums)
    operators_possible = perm(['+','-','*','÷'])
    goods_noods_one = []
    goods_noods_two = []
    for nums in nums_possible:
        for op in operators_possible:
            node = one_expression_tree(op, nums)
            if Calculate_Tree(node) == 24:
                goods_noods_one.append(node)
            node = two_expression_tree(op, nums)
            if Calculate_Tree(node) == 24:
                goods_noods_two.append(node)

    goods_noods1 = PanChong_one(goods_noods_one)
    goods_noods2 = PanChong_one(goods_noods_two)
    goods_noods = goods_noods1 + goods_noods2
    for nn in goods_noods:
        print_expression_tree(nn)
    # map(lambda node: print_expression_tree(node), goods_noods)



def print_expression_tree(root):
    print_node(root)
    print(' = 24')


def print_node(node):
    if node is None:
        return u"没有结果"
    if node.left is None and node.right is None:
        print(node.val, end="")
    else:
        print('(', end="")
        print_node(node.left)
        print(node.val, end="")
        print_node(node.right)
        print(')', end="")


if __name__ == '__main__':
    str_list = ""
    calculate([2, 3, 4, 6])
