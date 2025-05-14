import streamlit as st
from robot.robot_factory import RobotFactory
from strategy.path_strategy import FastPath, SafePath
from sensors.observer import Sensor, ObstacleAlert
from commands.command import StartCommand, StopCommand
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 初始化策略與感測器
fast_strategy = FastPath()
safe_strategy = SafePath()
sensor = Sensor()
alert = ObstacleAlert()
sensor.register(alert)

# Streamlit 介面
st.title("起點-終點路徑選擇")
st.write("選擇路徑策略：")
strategy_name = st.radio("路徑選項", ("最佳路徑", "最遠路徑"))

# 根據選擇決定路徑策略與路徑
if strategy_name == "最佳路徑":
    strategy = fast_strategy
    path_description = "顯示最佳路徑"
else:
    strategy = safe_strategy
    path_description = "顯示最遠路徑"

# 初始顯示網格
st.write(f"策略: {strategy_name} 已選擇")

# 建立機器人
robot = RobotFactory.create_robot("delivery", "John")

# 顯示起始網格 (不顯示路徑)
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_xticks(range(7))
ax.set_yticks(range(7))
ax.grid(True)

# 標示起點與終點
ax.text(0.5, 0.5, "起點", fontsize=12, ha="center", va="center", color="green")
ax.add_patch(
    patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor="green", linewidth=2)
)

ax.text(5.5, 0.5, "終點", fontsize=12, ha="center", va="center", color="red")
ax.add_patch(patches.Rectangle((5, 0), 1, 1, fill=False, edgecolor="red", linewidth=2))

# 設定障礙物
obstacles = [
    (1, 0),
    (1, 2),
    (2, 0),
    (2, 2),
    (2, 4),
    (1, 4),
    (4, 3),
    (4, 1),
    (5, 1),
]
for ox, oy in obstacles:
    ax.add_patch(patches.Rectangle((ox, oy), 1, 1, color="gray"))

ax.set_title(f"6x6 網格圖", fontsize=14)
# 設定繁體中文字型 (確保 matplotlib 能支援)
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]  # 微軟正黑體
plt.rcParams["axes.unicode_minus"] = False  # 處理負號顯示問題

st.pyplot(fig)

# 啟動按鈕
if st.button("Start"):
    start = StartCommand(robot)
    start.execute()
    st.write(f"{robot.name} 開始走...")

    # 假裝機器人正在運行並等待
    for _ in range(3):
        time.sleep(1)
        st.write(f"{robot.name} 正在移動...")
        sensor.notify()
        time.sleep(1)

    # 停止機器人
    stop = StopCommand(robot)
    stop.execute()
    st.write(f"{robot.name} 抵達終點")

    # 顯示最佳路徑或一般路徑
    time.sleep(2)  # 停頓 2 秒後顯示路徑

    st.write(path_description)  # 顯示相對應的路徑描述

    # 繪製路徑
    path = strategy.calculate_path()

    # 繪製 6x6 網格圖
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_xticks(range(7))
    ax.set_yticks(range(7))
    ax.grid(True)

    # 標示起點與終點
    ax.text(0.5, 0.5, "起點", fontsize=12, ha="center", va="center", color="green")
    ax.add_patch(
        patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor="green", linewidth=2)
    )

    ax.text(5.5, 0.5, "終點", fontsize=12, ha="center", va="center", color="red")
    ax.add_patch(
        patches.Rectangle((5, 0), 1, 1, fill=False, edgecolor="red", linewidth=2)
    )

    # 設定障礙物
    for ox, oy in obstacles:
        ax.add_patch(patches.Rectangle((ox, oy), 1, 1, color="gray"))

    # 繪製路徑
    path_color = "blue"  # 這裡選擇藍色為路徑
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        ax.plot(
            [x1 + 0.5, x2 + 0.5], [y1 + 0.5, y2 + 0.5], color=path_color, linewidth=2
        )

    ax.set_title(f"6x6 路徑圖 ({strategy_name})", fontsize=14)
    st.pyplot(fig)
