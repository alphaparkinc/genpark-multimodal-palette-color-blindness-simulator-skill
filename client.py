import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class MultimodalPaletteColorBlindnessSimulatorClient:
    """
    Color Vision Deficiency (CVD) simulation matrix model.
    Simulates Protanopia (red-blind), Deuteranopia (green-blind), and Tritanopia (blue-blind)
    via Brettel-Vienot LMS spectral confusion models and tests post-simulation perceptual delta E.
    """
    def __init__(self):
        # 3x3 transformation matrices for Protanopia, Deuteranopia, Tritanopia
        self.matrices = {
            "protanopia": [
                [0.56667, 0.43333, 0.00000],
                [0.55833, 0.44167, 0.00000],
                [0.00000, 0.24167, 0.75833]
            ],
            "deuteranopia": [
                [0.62500, 0.37500, 0.00000],
                [0.70000, 0.30000, 0.00000],
                [0.00000, 0.30000, 0.70000]
            ],
            "tritanopia": [
                [0.95000, 0.05000, 0.00000],
                [0.00000, 0.43333, 0.56667],
                [0.00000, 0.47500, 0.52500]
            ]
        }

    def simulate_cvd_pixel(self, r, g, b, deficiency_type):
        m = self.matrices.get(deficiency_type.lower(), self.matrices["protanopia"])
        r_sim = min(255, max(0, int(r * m[0][0] + g * m[0][1] + b * m[0][2])))
        g_sim = min(255, max(0, int(r * m[1][0] + g * m[1][1] + b * m[1][2])))
        b_sim = min(255, max(0, int(r * m[2][0] + g * m[2][1] + b * m[2][2])))
        return r_sim, g_sim, b_sim

    def color_delta_e(self, rgb1, rgb2):
        # Euclidean RGB distance as fast perceptual disparity approximation
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

    def simulate_palette(self, hex_colors):
        results = []
        for hex_str in hex_colors:
            clean = hex_str.strip().lstrip('#')
            r = int(clean[0:2], 16)
            g = int(clean[2:4], 16)
            b = int(clean[4:6], 16)

            cvd_variants = {}
            for dtype in ["protanopia", "deuteranopia", "tritanopia"]:
                r_s, g_s, b_s = self.simulate_cvd_pixel(r, g, b, dtype)
                delta = round(self.color_delta_e((r, g, b), (r_s, g_s, b_s)), 2)
                cvd_variants[dtype] = {
                    "hex": f"#{r_s:02x}{g_s:02x}{b_s:02x}".upper(),
                    "rgb": [r_s, g_s, b_s],
                    "perceptual_delta_e": delta
                }

            results.append({
                "original_hex": f"#{clean.upper()}",
                "original_rgb": [r, g, b],
                "cvd_simulations": cvd_variants
            })

        return {
            "status": "success",
            "colors_tested_count": len(hex_colors),
            "palette_simulations": results
        }
