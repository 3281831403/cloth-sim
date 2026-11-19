# 布料模拟：约束、碰撞与子步

布料在角色跑动时穿过身体、拉成橡皮：Verlet 积分没有阻尼，距离约束修正量不够，圆形碰撞只检测不推出，风力没按法线投影，接缝顶点没有缝合，子步数按帧固定，自碰撞没有空间划分，LOD 步长不随距离，锚点混合突变，批量布料只提交一半。

## 目录结构

```
README.md
conftest.py
.gitignore
physics/__init__.py
physics/cloth.py
tests/test_cloth.py
```

## 当前状态

`physics/cloth.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_cloth.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. Verlet 积分加入阻尼
2. 距离约束按刚度修正
3. 圆形碰撞把顶点推出
4. 风力按法线投影
5. 接缝顶点缝合
6. 子步数按最大步长计算
7. 自碰撞按空间网格筛对
8. LOD 步长随距离增加
9. 锚点按权重混合
10. 批量布料统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `physics/cloth.py`
后 15 条用例应全部通过。
