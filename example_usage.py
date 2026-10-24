from client import MultimodalPaletteColorBlindnessSimulatorClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    simulator = MultimodalPaletteColorBlindnessSimulatorClient()
    print("=== MULTIMODAL PALETTE COLOR BLINDNESS SIMULATOR ===")
    
    test_swatches = ["#EF4444", "#10B981", "#3B82F6", "#F59E0B"]
    res = simulator.simulate_palette(test_swatches)
    
    print(f"Tested {res['colors_tested_count']} Core Brand Swatches across Protanopia / Deuteranopia / Tritanopia:")
    print()
    for item in res['palette_simulations']:
        print(f"Original: {item['original_hex']}")
        for dtype, sim in item['cvd_simulations'].items():
            print(f"  - {dtype.capitalize():<12}: {sim['hex']} (Delta E: {sim['perceptual_delta_e']})")
        print()

if __name__ == "__main__":
    main()
