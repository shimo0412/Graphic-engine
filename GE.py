import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def draw_sphere(ax, center, radius, color):
    """球を描画する関数"""
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=0.6)

def draw_cube(ax, origin, size, color):
    """立方体を描画する関数"""
    x = [origin[0], origin[0] + size]
    y = [origin[1], origin[1] + size]
    z = [origin[2], origin[2] + size]
    xx, yy = np.meshgrid(x, y)
    ax.plot_surface(xx, yy, np.array([[z[0], z[0]], [z[0], z[0]]]), color=color, alpha=0.6)  # Bottom
    ax.plot_surface(xx, yy, np.array([[z[1], z[1]], [z[1], z[1]]]), color=color, alpha=0.6)  # Top
    yy, zz = np.meshgrid(y, z)
    ax.plot_surface(np.array([[x[0], x[0]], [x[0], x[0]]]), yy, zz, color=color, alpha=0.6)  # Left
    ax.plot_surface(np.array([[x[1], x[1]], [x[1], x[1]]]), yy, zz, color=color, alpha=0.6)  # Right
    xx, zz = np.meshgrid(x, z)
    ax.plot_surface(xx, np.array([[y[0], y[0]], [y[0], y[0]]]), zz, color=color, alpha=0.6)  # Front
    ax.plot_surface(xx, np.array([[y[1], y[1]], [y[1], y[1]]]), zz, color=color, alpha=0.6)  # Back

def draw_cylinder(ax, center, radius, height, color):
    """円柱を描画する関数"""
    z = np.linspace(center[2], center[2] + height, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = center[0] + radius * np.cos(theta_grid)
    y_grid = center[1] + radius * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.6)

def plot_shape(shape):
    """選択された図形をプロットする関数"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    if shape == "sphere":
        draw_sphere(ax, center=[0, 0, 0], radius=1, color='blue')
    elif shape == "cube":
        draw_cube(ax, origin=[-1, -1, -1], size=2, color='red')
    elif shape == "cylinder":
        draw_cylinder(ax, center=[0, 0, 0], radius=1, height=2, color='green')
    else:
        print("無効な図形です。")
        return
    
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    plt.show()

def on_select(event):
    """選択された図形を描画する関数"""
    selected_shape = shape_combobox.get()
    plot_shape(selected_shape)

# GUIのセットアップ
root = tk.Tk()
root.title("3D Shape Drawer")

# ラベル
label = tk.Label(root, text="描画する図形を選択してください:")
label.pack(pady=10)

# コンボボックス
shape_options = ["sphere", "cube", "cylinder"]
shape_combobox = ttk.Combobox(root, values=shape_options, state="readonly")
shape_combobox.set("sphere")
shape_combobox.pack(pady=10)

# ボタン
draw_button = tk.Button(root, text="描画", command=lambda: on_select(None))
draw_button.pack(pady=10)

# イベントバインド
shape_combobox.bind("<<ComboboxSelected>>", on_select)

# GUIの開始
root.mainloop()
