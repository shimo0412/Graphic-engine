import tkinter as tk
from tkinter import ttk, colorchooser
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Shape:
    """図形のプロパティを管理するクラス"""
    def __init__(self, shape_type, position, color, size_param_1, size_param_2, transparent):
        self.shape_type = shape_type
        self.position = position
        self.color = color
        self.size_param_1 = size_param_1
        self.size_param_2 = size_param_2
        self.transparent = transparent


class ShapeDrawer:
    def __init__(self, canvas_frame, control_frame):
        self.shapes = []  # 複数の図形を管理するリスト
        self.current_shape_index = None  # 現在選択されている図形のインデックス

        # Matplotlib FigureとAxesのセットアップ
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # TkinterキャンバスにFigureを描画
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # 図形リストボックスを作成
        self.shape_listbox = tk.Listbox(control_frame, height=8)
        self.shape_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.shape_listbox.bind("<<ListboxSelect>>", self.on_shape_selected)

        # 初期設定として1つの図形を追加
        self.add_shape("sphere", [0, 0, 0], "blue", 1.0, 1.0, True)

    def add_shape(self, shape_type, position, color, size_param_1, size_param_2, transparent):
        """新しい図形を追加する"""
        new_shape = Shape(shape_type, position, color, size_param_1, size_param_2, transparent)
        self.shapes.append(new_shape)
        self.current_shape_index = len(self.shapes) - 1
        self.plot_shapes()
        self.update_shape_list()

    def remove_current_shape(self):
        """現在選択されている図形を削除する"""
        if self.current_shape_index is not None:
            del self.shapes[self.current_shape_index]
            if self.shapes:
                self.current_shape_index = 0
            else:
                self.current_shape_index = None
            self.plot_shapes()
            self.update_shape_list()

    def draw_sphere(self, center, radius, color, transparent):
        """球を描画する関数"""
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
        y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
        z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        alpha = 0.6 if transparent else 1.0
        self.ax.plot_surface(x, y, z, color=color, alpha=alpha)

    def draw_cube(self, origin, size, color, transparent):
        """立方体を描画する関数"""
        x = [origin[0], origin[0] + size]
        y = [origin[1], origin[1] + size]
        z = [origin[2], origin[2] + size]
        alpha = 0.6 if transparent else 1.0
        xx, yy = np.meshgrid(x, y)
        self.ax.plot_surface(xx, yy, np.array([[z[0], z[0]], [z[0], z[0]]]), color=color, alpha=alpha)  # Bottom
        self.ax.plot_surface(xx, yy, np.array([[z[1], z[1]], [z[1], z[1]]]), color=color, alpha=alpha)  # Top
        yy, zz = np.meshgrid(y, z)
        self.ax.plot_surface(np.array([[x[0], x[0]], [x[0], x[0]]]), yy, zz, color=color, alpha=alpha)  # Left
        self.ax.plot_surface(np.array([[x[1], x[1]], [x[1], x[1]]]), yy, zz, color=color, alpha=alpha)  # Right
        xx, zz = np.meshgrid(x, z)
        self.ax.plot_surface(xx, np.array([[y[0], y[0]], [y[0], y[0]]]), zz, color=color, alpha=alpha)  # Front
        self.ax.plot_surface(xx, np.array([[y[1], y[1]], [y[1], y[1]]]), zz, color=color, alpha=alpha)  # Back

    def draw_cylinder(self, center, radius, height, color, transparent):
        """円柱を描画する関数"""
        z = np.linspace(center[2], center[2] + height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = center[0] + radius * np.cos(theta_grid)
        y_grid = center[1] + radius * np.sin(theta_grid)
        alpha = 0.6 if transparent else 1.0
        self.ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha)

    def plot_shapes(self):
        """全ての図形を描画する"""
        self.ax.clear()
        for shape in self.shapes:
            if shape.shape_type == "sphere":
                self.draw_sphere(shape.position, shape.size_param_1, shape.color, shape.transparent)
            elif shape.shape_type == "cube":
                origin = [
                    shape.position[0] - shape.size_param_1 / 2,
                    shape.position[1] - shape.size_param_1 / 2,
                    shape.position[2] - shape.size_param_1 / 2
                ]
                self.draw_cube(origin, shape.size_param_1, shape.color, shape.transparent)
            elif shape.shape_type == "cylinder":
                self.draw_cylinder(shape.position, shape.size_param_1, shape.size_param_2, shape.color, shape.transparent)

        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-5, 5)
        self.canvas.draw()

    def update_shape_list(self):
        """図形リストを更新する"""
        self.shape_listbox.delete(0, tk.END)
        for i, shape in enumerate(self.shapes):
            shape_type = shape.shape_type.capitalize()
            self.shape_listbox.insert(tk.END, f"{i + 1}: {shape_type}")

    def on_shape_selected(self, event):
        """リストボックスで選択された図形を操作対象に設定"""
        selected_index = self.shape_listbox.curselection()
        if selected_index:
            self.select_shape(selected_index[0])

    def select_shape(self, index):
        """操作対象の図形を選択する"""
        self.current_shape_index = index
        self.update_gui_for_selected_shape()

    def update_gui_for_selected_shape(self):
        """選択された図形の設定をGUIに反映する"""
        if self.current_shape_index is None:
            return
        shape = self.shapes[self.current_shape_index]
        shape_combobox.set(shape.shape_type)
        transparency_var.set(shape.transparent)
        size_slider_1.set(shape.size_param_1)
        size_slider_2.set(shape.size_param_2)
        for i, slider in enumerate(position_sliders):
            slider.set(shape.position[i])


# Tkinterアプリケーションのセットアップ
root = tk.Tk()
root.title("3D Shape Drawer")
root.geometry("900x700")

# メインフレームの作成
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# 左ペイン（操作用コントロール）
control_frame = tk.Frame(main_frame, width=300)
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# 右ペイン（描画キャンバス）
canvas_frame = tk.Frame(main_frame, bg="white")
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# ShapeDrawerクラスのインスタンス作成
drawer = ShapeDrawer(canvas_frame, control_frame)

# ----------------------------
# コントロールウィジェットの配置
# ----------------------------

# 図形リスト
tk.Label(control_frame, text="Shapes").pack(anchor=tk.W)
shape_listbox = drawer.shape_listbox  # ShapeDrawerのリストボックスを使用

# 図形の選択
tk.Label(control_frame, text="Shape Type").pack(anchor=tk.W)
shape_combobox = ttk.Combobox(control_frame, values=["sphere", "cube", "cylinder"])
shape_combobox.pack(fill=tk.X, padx=5, pady=5)

shape_combobox.bind("<<ComboboxSelected>>", lambda event: drawer.on_shape_type_changed(event))

def on_shape_type_changed(event):
    """図形の種類を変更する"""
    if drawer.current_shape_index is not None:
        shape = drawer.shapes[drawer.current_shape_index]
        shape.shape_type = shape_combobox.get()
        drawer.plot_shapes()

shape_combobox.bind("<<ComboboxSelected>>", on_shape_type_changed)

# 図形の透明度
transparency_var = tk.BooleanVar(value=True)
transparency_checkbutton = tk.Checkbutton(control_frame, text="Transparent", variable=transparency_var, command=lambda: update_shape_property("transparent", transparency_var.get()))
transparency_checkbutton.pack(anchor=tk.W)

# サイズスライダー
tk.Label(control_frame, text="Size Parameter 1").pack(anchor=tk.W)
size_slider_1 = tk.Scale(control_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
size_slider_1.pack(fill=tk.X, padx=5, pady=5)

tk.Label(control_frame, text="Size Parameter 2").pack(anchor=tk.W)
size_slider_2 = tk.Scale(control_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
size_slider_2.pack(fill=tk.X, padx=5, pady=5)

# 位置スライダー
tk.Label(control_frame, text="Position").pack(anchor=tk.W)
position_sliders = []
for axis in ["X", "Y", "Z"]:
    tk.Label(control_frame, text=f"Position {axis}").pack(anchor=tk.W)
    slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL)
    slider.pack(fill=tk.X, padx=5, pady=5)
    position_sliders.append(slider)

def update_shape_property(property_name, value):
    """図形のプロパティを更新する"""
    if drawer.current_shape_index is not None:
        shape = drawer.shapes[drawer.current_shape_index]
        setattr(shape, property_name, value)
        drawer.plot_shapes()

def update_position():
    """位置スライダーの値を図形に反映"""
    if drawer.current_shape_index is not None:
        shape = drawer.shapes[drawer.current_shape_index]
        shape.position = [slider.get() for slider in position_sliders]
        drawer.plot_shapes()

def update_size():
    """サイズスライダーの値を図形に反映"""
    if drawer.current_shape_index is not None:
        shape = drawer.shapes[drawer.current_shape_index]
        shape.size_param_1 = size_slider_1.get()
        shape.size_param_2 = size_slider_2.get()
        drawer.plot_shapes()

for slider in position_sliders:
    slider.config(command=lambda _: update_position())

size_slider_1.config(command=lambda _: update_size())
size_slider_2.config(command=lambda _: update_size())


# 設定リセットボタン
tk.Button(control_frame, text="Reset Settings", command=lambda: drawer.reset_settings()).pack(fill=tk.X, padx=5, pady=5)


# 色選択
tk.Label(control_frame, text="Color").pack(anchor=tk.W)
color_button = tk.Button(control_frame, text="Choose Color", command=lambda: choose_color())
color_button.pack(fill=tk.X, padx=5, pady=5)

def choose_color():
    """色選択ダイアログを開き、図形の色を変更"""
    if drawer.current_shape_index is not None:
        color_code = colorchooser.askcolor(title="Choose Color")[1]
        if color_code:
            shape = drawer.shapes[drawer.current_shape_index]
            shape.color = color_code
            drawer.plot_shapes()

# 図形の追加と削除
tk.Button(control_frame, text="Add Shape", command=lambda: drawer.add_shape("sphere", [0, 0, 0], "blue", 1.0, 1.0, True)).pack(fill=tk.X, padx=5, pady=5)
tk.Button(control_frame, text="Remove Shape", command=lambda: drawer.remove_current_shape()).pack(fill=tk.X, padx=5, pady=5)

# 初期状態の設定
drawer.update_shape_list()

# メインループ
root.mainloop()
