import pytest
from lab1 import TextGraph

@pytest.fixture
def built_graph():
    """构建一个通用图供大部分测试使用"""
    g = TextGraph()
    text = "To explore strange new worlds,To seek out new life and new civilizations"
    g.build_graph_from_text(text)
    return g

def test_TC01_bridge_exists(built_graph):
    # TC01: 存在 bridge word: explore
    result = built_graph.query_bridge_words("to", "strange")
    assert "explore" in result.lower()

def test_TC02_no_bridge(built_graph):
    # TC02: life -> civilizations 之间无桥接词
    result = built_graph.query_bridge_words("life", "civilizations")
    assert "no bridge" in result.lower()

def test_TC03_word1_not_in_graph(built_graph):
    # TC03: galaxy 不存在
    result = built_graph.query_bridge_words("galaxy", "life")
    assert "no galaxy or life" in result.lower()

def test_TC04_word2_not_in_graph(built_graph):
    # TC04: unknown 不存在
    result = built_graph.query_bridge_words("to", "unknown")
    assert "no to or unknown" in result.lower()

def test_TC05_empty_word1(built_graph):
    # TC05: word1 为空
    result = built_graph.query_bridge_words("", "life")
    assert "no" in result.lower()

def test_TC06_empty_word2(built_graph):
    # TC06: word2 为空
    result = built_graph.query_bridge_words("to", "")
    assert "no" in result.lower()

def test_TC07_case_insensitive(built_graph):
    # TC07: 大小写混合输入
    result = built_graph.query_bridge_words("TO", "STRANGE")
    assert "explore" in result.lower()

def test_TC08_empty_graph():
    # TC08: 空图测试
    g = TextGraph()
    result = g.query_bridge_words("to", "strange")
    assert "no to or strange" in result.lower()
