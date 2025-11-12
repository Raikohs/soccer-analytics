import open3d as o3d
import numpy as np

# =========================
# Assignment #5 - Open3D
# =========================

# === Этап 0. Загрузка модели ===
model_path = r"C:\Users\Raimbek\Desktop\untitled.obj"
mesh = o3d.io.read_triangle_mesh(model_path)
if not mesh.has_vertex_normals():
    mesh.compute_vertex_normals()
print(f"Модель загружена: {model_path}")

# =========================
# Этап 1. Загрузка и визуализация
# =========================
print("\n=== Этап 1. Загрузка и визуализация ===")
print(f"Вершины: {len(mesh.vertices)}")
print(f"Треугольники: {len(mesh.triangles)}")
print(f"Цвета: {mesh.has_vertex_colors()}")
print(f"Нормали: {mesh.has_vertex_normals()}")

if not mesh.has_vertex_colors():
    vertices = np.asarray(mesh.vertices)
    colors = (vertices - vertices.min(axis=0)) / (vertices.max(axis=0) - vertices.min(axis=0) + 1e-8)
    mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

o3d.visualization.draw_geometries([mesh])
print("Исходная модель отображена.\n")

# =========================
# Этап 2. Преобразование в облако точек
# =========================
pcd = mesh.sample_points_poisson_disk(number_of_points=10000)
print("\n=== Этап 2. Преобразование в облако точек ===")
print(f"Вершины (точки): {len(pcd.points)}")
print(f"Цвета: {pcd.has_colors()}")
o3d.visualization.draw_geometries([pcd])
print("Модель преобразована в плотное облако точек.\n")

# =========================
# Этап 3. Реконструкция поверхности
# =========================
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
mesh_rec, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
bbox = pcd.get_axis_aligned_bounding_box()
mesh_cropped = mesh_rec.crop(bbox)
print("\n=== Этап 3. Реконструкция поверхности ===")
print(f"Вершины: {len(mesh_cropped.vertices)}")
print(f"Треугольники: {len(mesh_cropped.triangles)}")
print(f"Цвета: {mesh_cropped.has_vertex_colors()}")
o3d.visualization.draw_geometries([mesh_cropped])
print("Поверхность восстановлена и обрезаны артефакты.\n")

# =========================
# Этап 4. Вокселизация
# =========================
voxel_size = 0.05
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)
print("\n=== Этап 4. Вокселизация ===")
print(f"Количество вокселей: {len(voxel_grid.get_voxels())}")
print(f"Цвета: {pcd.has_colors()}")
o3d.visualization.draw_geometries([voxel_grid])
print("Объект преобразован в воксели.\n")

# =========================
# Этап 5. Добавление платформы
# =========================
plane_width = 4
plane_depth = 4
plane_height = 0.05
platform = o3d.geometry.TriangleMesh.create_box(width=plane_width, height=plane_height, depth=plane_depth)
center = mesh.get_center()
platform.translate([center[0] - plane_width/2, center[1] - 0.5 - plane_height/2, center[2] - plane_depth/2])
platform.paint_uniform_color([0.7, 0.4, 0.1])
print("\n=== Этап 5. Добавление платформы ===")
o3d.visualization.draw_geometries([mesh, platform])
print("Платформа добавлена как сплошная доска.\n")

# =========================
# Этап 6. Клиппинг по платформе
# =========================
points = np.asarray(pcd.points)
plane_y = center[1] - 0.5  # уровень платформы
mask = points[:, 1] > plane_y  # оставляем точки выше платформы
pcd_clipped = pcd.select_by_index(np.where(mask)[0])

print("\n=== Этап 6. Клиппинг ===")
print(f"Осталось точек: {len(pcd_clipped.points)}")
print(f"Цвета: {pcd_clipped.has_colors()}")
print(f"Нормали: {pcd_clipped.has_normals()}")
o3d.visualization.draw_geometries([pcd_clipped, platform])
print("Клиппинг выполнен по платформе.\n")

# =========================
# Этап 7. Сплошная поверхность с градиентом по X
# =========================
pcd_clipped.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
mesh_final, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd_clipped, depth=8)
bbox = pcd_clipped.get_axis_aligned_bounding_box()
mesh_final = mesh_final.crop(bbox)

# Градиент по X
vertices = np.asarray(mesh_final.vertices)
x_min, x_max = vertices[:, 0].min(), vertices[:, 0].max()
x_norm = (vertices[:, 0] - x_min) / (x_max - x_min + 1e-8)

colors = np.zeros((vertices.shape[0], 3))
colors[:, 0] = x_norm          # красный канал
colors[:, 2] = 1 - x_norm      # синий канал
mesh_final.vertex_colors = o3d.utility.Vector3dVector(colors)

# Экстремальные точки
max_point = vertices[np.argmax(vertices[:, 0])]
min_point = vertices[np.argmin(vertices[:, 0])]

sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=0.1)
sphere_max.translate(max_point)
sphere_max.paint_uniform_color([1, 0, 0])  # красная сфера

sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=0.1)
sphere_min.translate(min_point)
sphere_min.paint_uniform_color([0, 0, 1])  # синяя сфера

# Визуализация
o3d.visualization.draw_geometries([mesh_final, sphere_max, sphere_min])
print("Сплошная поверхность с градиентом цвета по X, экстремальные точки отмечены.\n")
