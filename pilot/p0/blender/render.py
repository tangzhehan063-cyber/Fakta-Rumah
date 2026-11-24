#!/usr/bin/env python3
"""Render P0 jalur BLENDER (bpy 5.3 sebagai modul Python, Cycles CPU).
Membaca spec/scene.json yang SAMA dengan jalur web.
pakai:
  python blender/render.py stills [samples] [scale]
  python blender/render.py clip   [samples] [scale] [seconds]
"""
import json, math, os, sys, time
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
samples = int(sys.argv[2]) if (len(sys.argv) > 2 and sys.argv[2].isdigit()) else 64
scale = 1.0 if mode == "depth" else (float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
S = json.load(open(os.path.join(ROOT, os.environ.get("SCENE", "spec/scene.json"))))

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module="cycles")
scene = bpy.context.scene
scene.render.engine = "CYCLES"
cy = scene.cycles
cy.device = "CPU"
cy.samples = samples
cy.use_denoising = True
try:
    cy.denoiser = "OPENIMAGEDENOISE"
except Exception as e:
    print("denoiser:", e)
cy.max_bounces = 6; cy.diffuse_bounces = 3; cy.glossy_bounces = 3; cy.transparent_max_bounces = 8
cy.use_adaptive_sampling = True
scene.render.resolution_x = int(S["format"]["width"] * scale)
scene.render.resolution_y = int(S["format"]["height"] * scale)
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = os.environ.get("VIEW", "AgX")
scene.view_settings.look = "None"
scene.view_settings.exposure = 0.0


def c3(h):
    h = h.lstrip("#")
    lin = lambda v: (v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return [lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)] + [1.0]

def conv(x, y, z):          # Three (Y-up) -> Blender (Z-up): rotasi +90 derajat pada X
    return (x, -z, y)

# ---------------------------------------------------------------- material
texdir = os.path.join(ROOT, "assets/tex")
mats = {}
for name, m in S["materials"].items():
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    base = c3(m["color"])
    bsdf.inputs["Roughness"].default_value = m["roughness"]
    bsdf.inputs["Metallic"].default_value = m["metallic"]
    if "map" in m:
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = bpy.data.images.load(os.path.join(texdir, m["map"]))
        tn.image.colorspace_settings.name = "sRGB"
        tn.extension = "REPEAT"; tn.interpolation = "Cubic"
        if m["color"].lower() != "#ffffff":
            mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
            mix.inputs[0].default_value = 1.0
            mix.inputs[7].default_value = base
            nt.links.new(tn.outputs["Color"], mix.inputs[6])
            nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
        else:
            nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = base
    if "opacity" in m:
        bsdf.inputs["Alpha"].default_value = m["opacity"]
    if "emissive" in m:
        bsdf.inputs["Emission Color"].default_value = c3(m["emissive"])
        bsdf.inputs["Emission Strength"].default_value = m["emissive_strength"] * 2.0
    mats[name] = mat

# ---------------------------------------------------------------- geometri
for ob in S["objects"]:
    P = ob["positions"]; N = ob["normals"]; UV = ob["uvs"]; I = ob["indices"]
    verts = [conv(P[i], P[i + 1], P[i + 2]) for i in range(0, len(P), 3)]
    norms = [conv(N[i], N[i + 1], N[i + 2]) for i in range(0, len(N), 3)]
    faces = [tuple(I[i:i + 3]) for i in range(0, len(I), 3)]
    mesh = bpy.data.meshes.new(ob["name"])
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    uv = mesh.uv_layers.new(name="UV")
    for loop in mesh.loops:
        k = loop.vertex_index
        uv.data[loop.index].uv = (UV[k * 2], UV[k * 2 + 1])
    mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
    mesh.normals_split_custom_set_from_vertices(norms)
    obj = bpy.data.objects.new(ob["name"], mesh)
    obj.data.materials.append(mats[ob["material"]])
    scene.collection.objects.link(obj)
    if ob["material"] in ("glass", "water"):
        obj.visible_shadow = False

# ---------------------------------------------------------------- cahaya + dunia
L = S["lights"]
sun_d = bpy.data.lights.new("key", "SUN")
sun_d.color = c3(L["key"]["color"])[:3]
sun_d.energy = 3.0 * L["key"]["strength"]
sun_d.angle = math.radians(5.0)            # kelembutan bayangan
sun = bpy.data.objects.new("key", sun_d)
scene.collection.objects.link(sun)
d = L["key"]["dir_from"]
import mathutils
dirv = mathutils.Vector(conv(*d)).normalized()
sun.rotation_euler = (-dirv).to_track_quat("-Z", "Y").to_euler()

pt = bpy.data.lights.new("accent", "POINT")
pt.color = c3(L["accent"]["color"])[:3]
pt.energy = 18.0 * L["accent"]["strength"]
pt.shadow_soft_size = L["accent"]["radius"]
ptob = bpy.data.objects.new("accent", pt); ptob.location = conv(*L["accent"]["pos"])
scene.collection.objects.link(ptob)

world = bpy.data.worlds.new("w"); scene.world = world; world.use_nodes = True
nt = world.node_tree
bg = nt.nodes["Background"]
# langit/ground lembut: gradien vertikal sederhana lewat Gradient texture pada koordinat 'Generated'
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
nt.links.new(tc.outputs["Generated"], sep.inputs[0])
nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
ramp.color_ramp.elements[0].color = c3(L["fill"]["ground"])
ramp.color_ramp.elements[1].color = c3(L["fill"]["sky"])
nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.15 * L["fill"]["strength"] + 0.25

# ---------------------------------------------------------------- kamera
camd = bpy.data.cameras.new("cam"); camd.sensor_fit = "VERTICAL"; camd.clip_start = 0.05; camd.clip_end = 40
cam = bpy.data.objects.new("cam", camd); scene.collection.objects.link(cam); scene.camera = cam

def pose(c):
    az, el = math.radians(c["az"]), math.radians(c["el"])
    t = mathutils.Vector(conv(*c["target"]))
    off3 = (math.cos(el) * math.sin(az) * c["dist"], math.sin(el) * c["dist"], math.cos(el) * math.cos(az) * c["dist"])
    pos = t + mathutils.Vector(conv(*off3))
    return pos, t

def apply_cam(c):
    pos, t = pose(c)
    cam.location = pos
    cam.rotation_euler = (t - pos).to_track_quat("-Z", "Y").to_euler()
    camd.angle = math.radians(c["fov"])
    if c.get("dof"):
        camd.dof.use_dof = True
        camd.dof.focus_distance = c["dof"]["focus"]
        camd.dof.aperture_fstop = c["dof"]["fstop"]
    else:
        camd.dof.use_dof = False

ease = lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def lerp_cam(a, b, u):
    l = lambda p, q: p + (q - p) * u
    da, db = a.get("dof"), b.get("dof")
    dof = None
    if da or db:
        dof = {"focus": l((da or {"focus": a["dist"]})["focus"], (db or {"focus": b["dist"]})["focus"]),
               "fstop": l((da or {"fstop": 16})["fstop"], (db or {"fstop": 16})["fstop"])}
    return {"target": [l(x, y) for x, y in zip(a["target"], b["target"])], "az": l(a["az"], b["az"]), "el": l(a["el"], b["el"]),
            "dist": l(a["dist"], b["dist"]), "fov": l(a["fov"], b["fov"]), "dof": dof}

def render(path):
    scene.render.filepath = path
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return time.time() - t0


if mode == "depth":
    zmin, zmax = 1.0, 9.0
    dm = bpy.data.materials.new("depth"); dm.use_nodes = True
    nt2 = dm.node_tree
    for n in list(nt2.nodes): nt2.nodes.remove(n)
    cd = nt2.nodes.new("ShaderNodeCameraData"); mr = nt2.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = zmin; mr.inputs["From Max"].default_value = zmax
    mr.inputs["To Min"].default_value = 0.0; mr.inputs["To Max"].default_value = 1.0; mr.clamp = True
    comb = nt2.nodes.new("ShaderNodeCombineColor"); em = nt2.nodes.new("ShaderNodeEmission"); out = nt2.nodes.new("ShaderNodeOutputMaterial")
    nt2.links.new(cd.outputs["View Z Depth"], mr.inputs["Value"])
    for ch in ("Red", "Green", "Blue"): nt2.links.new(mr.outputs["Result"], comb.inputs[ch])
    nt2.links.new(comb.outputs["Color"], em.inputs["Color"]); nt2.links.new(em.outputs["Emission"], out.inputs["Surface"])
    bpy.context.view_layer.material_override = dm
    scene.view_settings.view_transform = "Raw"; scene.view_settings.look = "None"
    cy.samples = 1; cy.use_denoising = False; cy.use_adaptive_sampling = False
    scene.render.filter_size = 0.01
    scene.render.image_settings.color_depth = "16"
    scene.render.image_settings.color_mode = "BW"
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    for l in (sun_d, pt): l.energy = 0
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
    os.makedirs(os.path.join(ROOT, "out/blender"), exist_ok=True)
    for name in sys.argv[2:]:
        apply_cam(S["cameras"][name]); camd.dof.use_dof = False
        t = render(os.path.join(ROOT, f"out/blender/depth_{name}.png")); print("depth", name, round(t, 1), "s")
    sys.exit(0)

if mode == "layers":
    objs = {o["name"]: bpy.data.objects[o["name"]] for o in S["objects"]}
    layer_of = {o["name"]: o.get("layer", "MID") for o in S["objects"]}
    os.makedirs(os.path.join(ROOT, "out/blender/layers"), exist_ok=True)
    only = os.environ.get("ONLY", "").split(",")
    for name in only:
        apply_cam(S["cameras"][name])
        for L in os.environ.get("LAYERS", "BACK,MID,FRONT").split(","):
            # objek di luar lapisan: tak terlihat KAMERA tetapi tetap membayangi dan memantulkan cahaya (pencahayaan konsisten)
            for n, ob in objs.items(): ob.visible_camera = (layer_of[n] == L)
            scene.render.film_transparent = (L != "BACK")
            t = render(os.path.join(ROOT, f"out/blender/layers/{name}_{L}.png")); print("layer", name, L, round(t, 1), "s", flush=True)
    sys.exit(0)
timings = {}
if mode == "stills":
    os.makedirs(os.path.join(ROOT, "out/blender"), exist_ok=True)
    for name, c in S["cameras"].items():
        if os.environ.get("ONLY") and name not in os.environ["ONLY"].split(","): continue
        apply_cam(c)
        timings[name] = render(os.path.join(ROOT, f"out/blender/{name}_s{samples}.png"))
        print(name, round(timings[name], 1), "s", flush=True)
else:
    secs = float(sys.argv[4]) if len(sys.argv) > 4 else S["clip"]["seconds"]
    n = int(round(secs * S["format"]["fps"]))
    clip = S["clip"]
    os.makedirs(os.path.join(ROOT, "frames/blender"), exist_ok=True)
    t_all = time.time()
    for f in range(n):
        u = ease(min(1.0, f / max(1, n - 1)))
        apply_cam(lerp_cam(S["cameras"][clip["from"]], S["cameras"][clip["to"]], u))
        render(os.path.join(ROOT, f"frames/blender/f{f:04d}.png"))
        if f % 5 == 0: print("frame", f, "/", n, round(time.time() - t_all), "s", flush=True)
    timings["total"] = time.time() - t_all
    print("total", round(timings["total"]), "s untuk", n, "frame")
os.makedirs(os.path.join(ROOT, "out/blender"), exist_ok=True)
json.dump(timings, open(os.path.join(ROOT, f"out/blender/timings_{mode}_s{samples}.json"), "w"), indent=1)
