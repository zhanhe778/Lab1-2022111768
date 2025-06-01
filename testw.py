import pytest
import sys
from pathlib import Path


# 添加项目根目录到路径（根据实际情况调整）
PROJECT_ROOT = str(Path(__file__).parent)
sys.path.insert(0, PROJECT_ROOT)  # 插入到路径最前面，优先搜索

print(f"Python搜索路径: {sys.path}")  # 调试用

from 1_3 import TextGraph



# 测试用例1：word1不存在
def test_word1_not_found(setup_graph):
    result = setup_graph.calc_shortest_path("non_existent")
    assert result == "non_existent not found in graph!"


# 测试用例2：word2不存在
def test_word2_not_found(setup_graph):
    result = setup_graph.calc_shortest_path("a", "non_existent")
    assert result == "non_existent not found in graph!"


# 测试用例3：单源路径，无节点可达
def test_single_source_no_reachable_nodes(setup_graph):
    result = setup_graph.calc_shortest_path("e")  # e没有入边
    assert "No paths from e." in result


# 测试用例4：单源路径，有节点可达
def test_single_source_with_reachable_nodes(setup_graph):
    result = setup_graph.calc_shortest_path("a")
    assert "Shortest path from a to b: a -> b (length: 1)" in result


# 测试用例5：两点间存在路径（需重构路径）
def test_path_exists(setup_graph):
    result = setup_graph.calc_shortest_path("a", "d")
    assert "Shortest path from a to d: a -> b -> c -> d (length: 3)" in result


# 测试用例6：两点间无路径
def test_path_not_exists(setup_graph):
    result = setup_graph.calc_shortest_path("a", "e")
    assert "No path exists from a to e!" in result


# 测试用例7：同一节点的路径（直接返回）
def test_same_node_path(setup_graph):
    result = setup_graph.calc_shortest_path("a", "a")
    assert "Shortest path from a to a: a (length: 0)" in result


# 测试用例8：路径重构-多层循环（覆盖while node is not None多次迭代）
def test_path_reconstruction_multiple_steps(setup_graph):
    result = setup_graph.calc_shortest_path("a", "d")
    # 验证路径重构是否正确处理多层前驱
    assert "a -> b -> c -> d" in result, "路径重构错误"


# 测试用例9：路径重构-单层循环（覆盖while node is not None一次迭代）
def test_path_reconstruction_single_step(setup_graph):
    result = setup_graph.calc_shortest_path("a", "b")
    assert "a -> b" in result, "单层路径重构错误"


# 测试用例10：路径重构-无前驱（覆盖while node is not None不执行）
def test_path_reconstruction_no_predecessor(setup_graph):
    # 修改图结构，使b无前驱
    graph = setup_graph
    graph.previous = {"a": None, "b": None, "c": "b", "d": "c"}
    result = graph.calc_shortest_path("a", "a")
    assert "a (length: 0)" in result, "无前驱节点路径错误"


# -------------- 测试图结构 --------------
@pytest.fixture
def setup_graph():
    graph = TextGraph()

    # 构建测试图
    test_text = """
    a b
    b c
    c d
    """

    with open("test_input.txt", "w", encoding="utf-8") as f:
        f.write(test_text)

    graph.build_graph("test_input.txt")

    # 显式添加节点e（存在但不可达）
    graph.nodes.add("e")

    return graph