import sys, json
from client import MultimodalPaletteColorBlindnessSimulatorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    simulator = MultimodalPaletteColorBlindnessSimulatorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-multimodal-palette-color-blindness-simulator-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    swatches = req.get("hex_colors", ["#EF4444", "#10B981"])
    res = simulator.simulate_palette(swatches)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
