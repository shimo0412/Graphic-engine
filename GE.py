import tkinter as tk
from tkinter import ttk, colorchooser
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class ShapeDrawer:
    def __init__(self, canvas_frame):
        self.selected_color = "blue"  # 初期の色
        self.selected_shape = "sphere"  # 初期の図形
        self.transparent = True  # 初期状態は透過
        self.size_parameter_1 = 1.0  # 図形のスケールパラメータ1
        self.size_parameter_2 = 1.0  # 図形のスケールパラメータ2

        # Matplotlib FigureとAxesのセットアップ
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # TkinterキャンバスにFigureを描画
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def draw_sphere(self, center, radius):
        """球を描画する関数"""
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
        y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
        z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        alpha = 0.6 if self.transparent else 1.0
        self.ax.plot_surface(x, y, z, color=self.selected_color, alpha=alpha)

    def draw_cube(self, origin, size):
        """立方体を描画する関数"""
        x = [origin[0], origin[0] + size]
        y = [origin[1], origin[1] + size]
        z = [origin[2], origin[2] + size]
        alpha = 0.6 if self.transparent else 1.0
        xx, yy = np.meshgrid(x, y)
        self.ax.plot_surface(xx, yy, np.array([[z[0], z[0]], [z[0], z[0]]]), color=self.selected_color, alpha=alpha)  # Bottom
        self.ax.plot_surface(xx, yy, np.array([[z[1], z[1]], [z[1], z[1]]]), color=self.selected_color, alpha=alpha)  # Top
        yy, zz = np.meshgrid(y, z)
        self.ax.plot_surface(np.array([[x[0], x[0]], [x[0], x[0]]]), yy, zz, color=self.selected_color, alpha=alpha)  # Left
        self.ax.plot_surface(np.array([[x[1], x[1]], [x[1], x[1]]]), yy, zz, color=self.selected_color, alpha=alpha)  # Right
        xx, zz = np.meshgrid(x, z)
        self.ax.plot_surface(xx, np.array([[y[0], y[0]], [y[0], y[0]]]), zz, color=self.selected_color, alpha=alpha)  # Front
        self.ax.plot_surface(xx, np.array([[y[1], y[1]], [y[1], y[1]]]), zz, color=self.selected_color, alpha=alpha)  # Back

    def draw_cylinder(self, center, radius, height):
        """円柱を描画する関数"""
        z = np.linspace(center[2], center[2] + height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = center[0] + radius * np.cos(theta_grid)
        y_grid = center[1] + radius * np.sin(theta_grid)
        alpha = 0.6 if self.transparent else 1.0
        self.ax.plot_surface(x_grid, y_grid, z_grid, color=self.selected_color, alpha=alpha)

    def plot_shape(self):
        """選択された図形を描画する関数"""
        self.ax.clear()  # 前回の描画をクリア

        if self.selected_shape == "sphere":
            self.draw_sphere(center=[0, 0, 0], radius=self.size_parameter_1)
        elif self.selected_shape == "cube":
            self.draw_cube(origin=[-self.size_parameter_1 / 2] * 3, size=self.size_parameter_1)
        elif self.selected_shape == "cylinder":
            self.draw_cylinder(center=[0, 0, 0], radius=self.size_parameter_1, height=self.size_parameter_2)

        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.set_zlabel('Z Axis')
        self.canvas.draw()

    def select_color(self):
        """カラーパレットから色を選択する"""
        color_code = colorchooser.askcolor(title="色を選択してください")[1]
        if color_code:
            self.selected_color = color_code
            self.plot_shape()

    def select_shape(self, event):
        """選択された図形を設定する"""
        self.selected_shape = shape_combobox.get()
        self.plot_shape()

    def toggle_transparency(self):
        """透過・不透過を切り替える"""
        self.transparent = transparency_var.get()
        self.plot_shape()

    def update_size_parameter_1(self, value):
        """スライダーからスケールパラメータ1を更新"""
        self.size_parameter_1 = float(value)
        self.plot_shape()

    def update_size_parameter_2(self, value):
        """スライダーからスケールパラメータ2を更新"""
        self.size_parameter_2 = float(value)
        self.plot_shape()


# GUIのセットアップ
root = tk.Tk()
root.title("3D Shape Drawer")

# キャンバスフレーム
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

drawer = ShapeDrawer(canvas_frame)

# コントロールフレーム
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# 図形選択
label = tk.Label(control_frame, text="描画する図形を選択してください:")
label.pack(pady=5)
shape_options = ["sphere", "cube", "cylinder"]
shape_combobox = ttk.Combobox(control_frame, values=shape_options, state="readonly")
shape_combobox.set("sphere")
shape_combobox.pack(pady=5)
shape_combobox.bind("<<ComboboxSelected>>", drawer.select_shape)

# 透過チェックボックス
transparency_var = tk.BooleanVar(value=True)
transparency_checkbox = tk.Checkbutton(control_frame, text="透過", variable=transparency_var, command=drawer.toggle_transparency)
transparency_checkbox.pack(pady=5)

# サイズスライダー1
slider1_label = tk.Label(control_frame, text="サイズ/半径:")
slider1_label.pack(pady=5)
size_slider_1 = tk.Scale(control_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, command=drawer.update_size_parameter_1)
size_slider_1.set(1.0)
size_slider_1.pack(pady=5)

# サイズスライダー2（高さ用）
slider2_label = tk.Label(control_frame, text="高さ (円柱用):")
slider2_label.pack(pady=5)
size_slider_2 = tk.Scale(control_frame, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, command=drawer.update_size_parameter_2)
size_slider_2.set(1.0)
size_slider_2.pack(pady=5)

# 色選択ボタン
color_button = tk.Button(control_frame, text="色を選択", command=drawer.select_color)
color_button.pack(pady=5)

# 初期描画
drawer.plot_shape()

# GUIの開始
root.mainloop()
