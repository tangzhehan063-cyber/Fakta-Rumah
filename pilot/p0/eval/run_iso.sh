#!/usr/bin/env bash
# Render plat isometrik v3 (berurutan agar waktu terukur bersih). Pakai: bash eval/run_iso.sh
cd "$(dirname "$0")/.."
PY=/home/user/venv-bpy/bin/python
export SCENE=spec/scene_neutral.json VIEW="Khronos PBR Neutral"
t0=$(date +%s)
echo "A truck plate"; RES=3240x2112 ONLY=ISO_A $PY blender/render.py stills 48 1.0 2>&1 | grep -E "^ISO"
echo "B layers"; ONLY=ISO_B LAYERS=BACK,MID,FRONT $PY blender/render.py layers 48 1.26 2>&1 | grep -E "^layer"
echo "orbit keys"; ONLY=ISO_O41,ISO_O43,ISO_O45,ISO_O47,ISO_O49 $PY blender/render.py stills 48 1.0 2>&1 | grep -E "^ISO"
echo "orbit depth"; $PY blender/render.py depth ISO_O41 ISO_O43 ISO_O45 ISO_O47 ISO_O49 2>&1 | grep -E "^depth"
echo "TOTAL $(( $(date +%s) - t0 )) s"
