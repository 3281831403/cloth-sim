"""布料模拟：约束、碰撞与子步：待实现的核心模块。"""


def verlet_step(positions, previous, accel, dt, damping):
    """带阻尼的 Verlet 积分。"""
    raise NotImplementedError

def distance_constraint(a, b, rest, stiffness):
    """距离约束按刚度修正两端点。"""
    raise NotImplementedError

def collide_circle(position, center, radius):
    """顶点进入圆内时推出到边界。"""
    raise NotImplementedError

def wind_force(normal, wind, strength):
    """风力按法线投影。"""
    raise NotImplementedError

def stitch_seam(a, b, weight):
    """接缝顶点按权重缝合。"""
    raise NotImplementedError

def substeps(dt, max_step):
    """按最大步长计算子步数。"""
    raise NotImplementedError

def self_collision_pairs(positions, min_distance):
    """找出距离小于阈值的顶点对。"""
    raise NotImplementedError

def lod_stride(distance, near, far):
    """LOD 步长随距离增加。"""
    raise NotImplementedError

def anchor_blend(position, anchor, weight):
    """锚点按权重混合。"""
    raise NotImplementedError

def commit_batch(statuses):
    """批量布料全部成功才提交。"""
    raise NotImplementedError
