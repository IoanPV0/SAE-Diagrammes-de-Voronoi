def test_3_points_triangle():
    points = [Point(0,0), Point(4,0), Point(2,3)]
    calc = VoronoiCalculator()
    diagram = calc.compute(points)
    assert len(diagram.vertices) == 1
    assert len(diagram.edges) == 3  # 1 finie + 2 rayons