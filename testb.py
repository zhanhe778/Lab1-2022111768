import pytest
from lab1 import TextGraph

# 测试数据：用于构建图的示例文本
TEST_TEXT = """
the quick and the dead
c sharp programming
and another sentence
"""


@pytest.fixture
def setup_graph():
    """创建并初始化TextGraph实例，返回已构建图的对象"""
    graph = TextGraph()
    # 使用临时文件加载测试文本
    with open("Easy Test.txt", "w", encoding="utf-8") as f:
        f.write(TEST_TEXT)
    graph.build_graph("Easy Test.txt")
    return graph


# ------------------- 测试用例1: 正常输入 (有效等价类) -------------------
def test_valid_input_the_and(setup_graph):
    """测试用例1：输入 'the', 'and'（存在桥接词）"""
    word1 = "the"
    word2 = "and"
    expected = "The bridge words from the to and are: quick."

    result = setup_graph.query_bridge_words(word1, word2)
    assert result == expected, f"预期: {expected}, 实际: {result}"


# ------------------- 测试用例2: 空字符串 (无效等价类) -------------------
def test_empty_string_input(setup_graph):
    """测试用例2：输入空字符串，and（无效输入）"""
    word1 = ""  # 空字符串
    word2 = "and"
    expected = "No  or and in the graph!"  # 处理后word1变为空字符串，函数可能返回此结果

    result = setup_graph.query_bridge_words(word1, word2)
    assert result == expected, f"预期: {expected}, 实际: {result}"


# ------------------- 测试用例3: 极短单词 (边界值) -------------------
def test_word_not_exist(setup_graph):
    """测试用例3：输入 'c', 'and'（c存在但无桥接词）"""
    word1 = "c"
    word2 = "and"
    expected = "No bridge words from c to and!"

    result = setup_graph.query_bridge_words(word1, word2)
    assert result == expected, f"预期: {expected}, 实际: {result}"


# ------------------- 测试用例4: 包含非法字符 (无效等价类) -------------------
def test_invalid_characters(setup_graph):
    """测试用例4：输入 '!a', 'and'（非法字符处理）"""
    word1 = "!a"  # 非法字符会被process_text过滤为''
    word2 = "and"
    expected = "No !a or and in the graph!"  # 处理后word1变为空字符串

    result = setup_graph.query_bridge_words(word1, word2)
    assert result == expected, f"预期: {expected}, 实际: {result}"