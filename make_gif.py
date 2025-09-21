import imageio.v2 as imageio
import os

def make_gif(frame_dir="frames", output="drone_sim.gif", fps=20):
    images = []
    files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])
    for f in files:
        images.append(imageio.imread(os.path.join(frame_dir, f)))
    imageio.mimsave(output, images, fps=fps)
    print(f"[OK] GIF saved to {output}")

if __name__ == "__main__":
    make_gif()
