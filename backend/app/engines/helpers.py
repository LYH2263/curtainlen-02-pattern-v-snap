import math

# 输入均为米、精度到厘米级，1e-9 m（微米级以下）容差足以吞掉浮点误差
_EPS = 1e-9

def ceil_units(v: float) -> int:
    return int(math.ceil(float(v) - _EPS))

def ceil_align(value: float, step: float) -> float:
    """把 value 向上对齐到 step 的整数倍；恰好为倍数时不再多抬一档。"""
    return ceil_units(float(value) / float(step)) * float(step)
