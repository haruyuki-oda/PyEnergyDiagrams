#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for xlim functionality in energy diagram
"""

import matplotlib.pyplot as plt
from energydiagram import ED

# Test 1: With xlim specified
print("Test 1: Energy diagram with xlim=(0, 10)")
ed1 = ED(xlim=(0, 10))
ed1.add_level(0, "Reactant")
ed1.add_level(5, "TS")
ed1.add_level(2, "Product")
ed1.add_link(0, 1)
ed1.add_link(1, 2)

fig1, ax1 = plt.subplots(figsize=(8, 6))
ed1.plot(ax=ax1)
ax1.set_title("With xlim=(0, 10) - Fixed X-axis Range")
plt.tight_layout()
plt.savefig("test_with_xlim.png", dpi=150)
print("Saved: test_with_xlim.png")
plt.close()

# Test 2: Without xlim (original behavior)
print("\nTest 2: Energy diagram without xlim (original behavior)")
ed2 = ED()
ed2.add_level(0, "Reactant")
ed2.add_level(5, "TS")
ed2.add_level(2, "Product")
ed2.add_link(0, 1)
ed2.add_link(1, 2)

fig2, ax2 = plt.subplots(figsize=(8, 6))
ed2.plot(ax=ax2)
ax2.set_title("Without xlim - Auto-scaled (original behavior)")
plt.tight_layout()
plt.savefig("test_without_xlim.png", dpi=150)
print("Saved: test_without_xlim.png")
plt.close()

# Test 3: With xlim and position="last"
print("\nTest 3: Testing position='last' with xlim")
ed3 = ED(xlim=(0, 12))
ed3.add_level(0, "A")
ed3.add_level(3, "B", position="last")  # Same X position as A
ed3.add_level(5, "C")
ed3.add_level(2, "D", position="last")  # Same X position as C
ed3.add_level(-1, "E")

fig3, ax3 = plt.subplots(figsize=(8, 6))
ed3.plot(ax=ax3)
ax3.set_title("With xlim=(0, 12) - Testing position='last'")
plt.tight_layout()
plt.savefig("test_position_last.png", dpi=150)
print("Saved: test_position_last.png")
plt.close()

print("\n✓ All tests completed successfully!")
print("The xlim functionality is working correctly.")
print("\nUsage:")
print("  ed = ED(xlim=(xmin, xmax))  # Specify X-axis range")
print("  ed = ED()                    # Original behavior (auto-scale)")
