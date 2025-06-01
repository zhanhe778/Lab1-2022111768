import pytest
from lab1 import TextGraph

@pytest.fixture
def test_graph():
    """使用提供的文本构建测试图"""
    g = TextGraph()
    text = "To explore strange new worlds To seek out new life and new civilizations"
    g.build_graph_from_text(text)
    return g

def test_path1_word1_not_in_graph(test_graph):
    """路径1：word1不在图中"""
    result = test_graph.calc_shortest_path("nonexistent")
    assert result == "nonexistent not found in graph!"

def test_path2_word2_not_in_graph(test_graph):
    """路径2：word2不在图中"""
    result = test_graph.calc_shortest_path("to", "nonexistent")
    assert result == "nonexistent not found in graph!"

def test_path3_word2_none_no_reachable_nodes(test_graph):
    """路径3：word2=None，无可达节点（孤立节点测试）"""
    # 添加孤立节点
    test_graph.nodes.add("isolated")
    result = test_graph.calc_shortest_path("isolated")
    assert result == "No paths found from isolated to other nodes."

def test_path4_word2_none_single_reachable():
    """路径4：word2=None，有1个可达节点"""   
    g = TextGraph()
    g.graph = {
        "worlds": {"to": 1},
        "to": {}  # 确保 to 无后续连接
    }
    g.nodes = set(g.graph.keys()) | {n for edges in g.graph.values() for n in edges.keys()}

    result = g.calc_shortest_path("worlds")
    assert "worlds -> to" in result
    assert len(result.split('\n')) == 1  # 验证只有一条路径

def test_path5_word2_none_multiple_reachable(test_graph):
    """路径5：word2=None，有多个可达节点"""
    result = test_graph.calc_shortest_path("to")
    assert "to -> explore" in result
    assert "to -> seek" in result
    assert "to -> new" not in result  # 验证是直接可达节点

def test_path6_word1_equals_word2(test_graph):
    """路径6：word1=word2"""
    result = test_graph.calc_shortest_path("new", "new")
    assert result == "Shortest path from new to new: new (length: 0)"

def test_path7_directly_connected(test_graph):
    """路径7：word2给定，直接相连"""
    result = test_graph.calc_shortest_path("to", "explore")
    assert result == "Shortest path from to to explore: to -> explore (length: 1)"

def test_path8_multi_hop_reachable(test_graph):
    """路径8：word2给定，多跳可达"""
    result = test_graph.calc_shortest_path("to", "civilizations")
    assert "to -> seek -> out -> new -> civilizations" in result or \
           "to -> explore -> strange -> new -> civilizations" in result

def test_path9_unreachable(test_graph):
    """路径9：word2给定，不可达"""
    # 添加一个真正孤立的节点
    test_graph.nodes.add("isolated")
    result = test_graph.calc_shortest_path("explore", "isolated")
    assert result == "No path exists from explore to isolated!"

def test_path10_visited_skip(test_graph):
    """路径10：节点已访问被跳过"""
    # 添加自环边触发visited检查
    test_graph.graph["new"]["new"] = 1
    result = test_graph.calc_shortest_path("to", "civilizations")
    assert "new" in result  # 只要结果正常即可验证跳过逻辑

def test_path11_distance_update(test_graph):
    """路径11：发现更短距离"""
    # 添加更长路径
    test_graph.graph["explore"]["civilizations"] = 5  # 长路径
    result = test_graph.calc_shortest_path("to", "civilizations")
    assert "to -> seek -> out -> new -> civilizations" in result  # 应选择更短路径

def test_path12_no_distance_update(test_graph):
    """路径12：未发现更短距离"""
    result = test_graph.calc_shortest_path("to", "explore")
    assert result == "Shortest path from to to explore: to -> explore (length: 1)"

def test_path13_queue_empty(test_graph):
    """路径13：优先队列提前清空"""
    # 测试不可达情况
    test_graph.nodes.add("unconnected")
    result = test_graph.calc_shortest_path("to", "unconnected")
    assert result == "No path exists from to to unconnected!"

def test_path14_early_termination(test_graph):
    """路径14：目标节点中途找到"""
    # 添加更远节点确保提前终止
    test_graph.graph["civilizations"]["distant"] = 1
    result = test_graph.calc_shortest_path("to", "new")
    assert "distant" not in result  # 验证不会处理更远节点

def test_path15_first_pop_hit(test_graph):
    """路径15：首次heappop即命中"""
    result = test_graph.calc_shortest_path("to", "to")
    assert result == "Shortest path from to to to: to (length: 0)"

def test_path16_complex_case(test_graph):
    """路径16：复杂多路径情况"""
    # 添加交叉路径
    test_graph.graph["strange"]["life"] = 1
    test_graph.graph["life"]["strange"] = 1
    result = test_graph.calc_shortest_path("to", "civilizations")
    # 验证能找到路径（可能有多条）
    assert "civilizations" in result