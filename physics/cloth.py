"""布料模拟：约束、碰撞与子步。"""

import itertools
import math


def verlet_step(positions, previous, accel, dt, damping):
    """带阻尼的 Verlet 积分。"""
    dt2 = dt * dt
    return [
        [
            p[d] + (p[d] - prev[d]) * damping + a[d] * dt2
            for d in range(len(p))
        ]
        for p, prev, a in zip(positions, previous, accel)
    ]


def distance_constraint(a, b, rest, stiffness):
    """距离约束按刚度修正两端点。"""
    delta = [b[d] - a[d] for d in range(len(a))]
    dist = math.sqrt(sum(x * x for x in delta))
    if dist == 0:
        return [list(a), list(b)]
    scale = 0.5 * stiffness * (dist - rest) / dist
    correction = [x * scale for x in delta]
    return [
        [a[d] + correction[d] for d in range(len(a))],
        [b[d] - correction[d] for d in range(len(b))],
    ]


def collide_circle(position, center, radius):
    """顶点进入圆内时推出到边界。"""
    offset = [position[d] - center[d] for d in range(len(position))]
    dist = math.sqrt(sum(x * x for x in offset))
    if dist >= radius or dist == 0:
        return list(position)
    scale = radius / dist
    return [center[d] + offset[d] * scale for d in range(len(position))]


def wind_force(normal, wind, strength):
    """风力按法线投影。"""
    length = math.sqrt(sum(x * x for x in normal))
    if length == 0:
        return [0] * len(normal)
    n = [x / length for x in normal]
    proj = sum(wind[d] * n[d] for d in range(len(n)))
    return [strength * proj * n[d] for d in range(len(n))]


def stitch_seam(a, b, weight):
    """接缝顶点按权重缝合。"""
    return [a[d] + (b[d] - a[d]) * weight for d in range(len(a))]


def substeps(dt, max_step):
    """按最大步长计算子步数。"""
    if max_step <= 0:
        raise ValueError("max_step must be positive")
    return max(1, math.ceil(dt / max_step))


def self_collision_pairs(positions, min_distance):
    """找出距离小于阈值的顶点对（空间网格宽相 + 精确距离窄相）。"""
    if min_distance <= 0:
        return []
    cells = {}
    for i, p in enumerate(positions):
        key = tuple(int(math.floor(c / min_distance)) for c in p)
        cells.setdefault(key, []).append(i)

    pairs = set()
    for key, indices in cells.items():
        dims = len(key)
        for offset in itertools.product((-1, 0, 1), repeat=dims):
            neighbor = tuple(key[d] + offset[d] for d in range(dims))
            for i in indices:
                for j in cells.get(neighbor, ()):
                    if i >= j:
                        continue
                    delta = [
                        positions[i][d] - positions[j][d]
                        for d in range(dims)
                    ]
                    if sum(x * x for x in delta) < min_distance * min_distance:
                        pairs.add((i, j))
    return [[i, j] for i, j in sorted(pairs)]


def lod_stride(distance, near, far):
    """LOD 步长随距离增加：4 档，步长 1/2/4/8。"""
    if distance <= near:
        return 1
    if distance >= far:
        return 8
    level = int((distance - near) / (far - near) * 3)
    return 2 ** level


def anchor_blend(position, anchor, weight):
    """锚点按权重混合。"""
    return [
        position[d] + (anchor[d] - position[d]) * weight
        for d in range(len(position))
    ]


def commit_batch(statuses):
    """批量布料全部成功才提交。"""
    return all(statuses)
