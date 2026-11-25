import cv2
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

y, x = np.mgrid[-60:60:600j, -100:100:1000j]
grid = ((x % 10 < 1) | (y % 10 < 1)).astype(np.float32)
pattern = (np.sin(x / 5) * np.cos(y / 5) + 1) / 2
img_synth = np.clip((grid + pattern) * 128, 0, 255).astype(np.uint8)
img_rgb = np.stack([img_synth] * 3, axis=-1)

h, w, _ = img_rgb.shape

x_dva = np.linspace(-100, 100, w)
y_dva = np.linspace(60, -60, h)
X_dva, Y_dva = np.meshgrid(x_dva, y_dva)

E = np.sqrt(X_dva**2 + Y_dva**2)

sigmas = [0, 5, 15, 31, 65]
layers = []
for s in sigmas:
  if s == 0:
    layers.append(img_rgb.astype(np.float32))
  else:
    # ksize dispari basato su sigma
    k = s * 2 + 1
    blurred = cv2.GaussianBlur(img_rgb, (k, k), s)
    layers.append(blurred.astype(np.float32))

E_norm = np.clip(E / 80.0, 0, 1)

n_layers = len(sigmas)
img_foveated = np.zeros_like(layers[0])
for i in range(n_layers):
  
  center = i / (n_layers - 1)
  weight = np.exp(-((E_norm - center) ** 2) / 0.05)
  weight = weight[:, :, np.newaxis]
  img_foveated += layers[i] * weight

weights_sum = np.zeros((h, w, 1), dtype=np.float32)
for i in range(n_layers):
  center = i / (n_layers - 1)
  weights_sum += np.exp(-((E_norm - center) ** 2) / 0.05)[:, :, np.newaxis]
img_foveated = np.clip(img_foveated / weights_sum, 0, 255).astype(np.uint8)

fig, ax = plt.subplots(figsize=(14, 8), facecolor="black")
ax.set_facecolor("black")
extent = [-100, 100, -60, 60]

ax.imshow(img_foveated, extent=extent, origin="upper")

for r in [10, 30, 60, 90]:
  c = patches.Circle(
      (0, 0),
      radius=r,
      fill=False,
      color="white",
      linestyle=":",
      linewidth=0.8,
      alpha=0.6,
  )
  ax.add_patch(c)
  ax.text(
      r,
      2,
      f"{r}°",
      color="white",
      fontsize=8,
      alpha=0.7,
      fontweight="bold",
      bbox=dict(
          boxstyle="round,pad=0.1",
          facecolor="black",
          edgecolor="none",
          alpha=0.5,
      ),
  )

angoli = np.radians([0, 45, 90, 135, 180, 225, 270, 315, 360])
raggi = [100, 80, 55, 55, 60, 55, 70, 85, 100]
t = np.linspace(0, 2 * np.pi, 200)
r_interp = np.interp(t, angoli, raggi, period=2 * np.pi)
ax.plot(
    r_interp * np.cos(t),
    r_interp * np.sin(t),
    color="cyan",
    linewidth=2,
    label="Limite Anatomico OD",
)

ax.add_patch(
    patches.Ellipse(
        (15, -1.5),
        width=5.5,
        height=7.5,
        facecolor="black",
        edgecolor="red",
        linewidth=1.2,
        linestyle="--",
        label="Blind spot",
    )
)

ax.add_patch(
    patches.Rectangle(
        (-10, -6),
        20,
        12,
        fill=True,
        facecolor="yellow",
        alpha=0.35,
        edgecolor="yellow",
        linewidth=2,
        label="Argus II (20°x12°)",
    )
)
ax.add_patch(
    patches.Rectangle(
        (-5, -5),
        10,
        10,
        fill=True,
        facecolor="lime",
        alpha=0.45,
        edgecolor="lime",
        linewidth=2,
        label="Alpha IMS (10°x10°)",
    )
)

ax.plot(0, 0, "r+", markersize=10, markeredgewidth=2)

ax.set_xlim(-105, 105)
ax.set_ylim(-65, 65)
ax.set_xlabel("Horizontal visual field (DVA)", color="white", fontsize=11)
ax.set_ylabel("Vertical visual field (DVA)", color="white", fontsize=11)
ax.tick_params(colors="white")
ax.set_title(
    "Visual acuity decay vs Protesi",
    color="white",
    fontsize=13,
    fontweight="bold",
)
ax.legend(
    loc="lower left", facecolor="#111111", edgecolor="none", labelcolor="white"
)

plt.tight_layout()
plt.savefig("foveated_visual_field.png", dpi=300, facecolor="black")
plt.show()