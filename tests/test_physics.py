import unittest

import numpy as np

from physics.phase_1.capacitor import time_constant as capacitor_time_constant, v_charge, v_discharge
from physics.phase_1.inductor import i_buildup, i_decay, time_constant as inductor_time_constant
from physics.phase_1.ohms_law import current, current_profile, power
from physics.phase_1.resonant_frequency import f0, f0_curve
from physics.phase_1.series_parallel import parallel, series
from physics.phase_2.short_circuit import three_phase_fault_current


class PhysicsFunctionsTest(unittest.TestCase):
    def test_ohms_law_scalar_and_profile(self):
        self.assertAlmostEqual(current(12, 6), 2)
        self.assertAlmostEqual(power(12, 6), 24)
        np.testing.assert_allclose(current_profile(12, [3, 6]), [4, 2])

    def test_resistor_combinations(self):
        self.assertAlmostEqual(series(2, 3, 5), 10)
        self.assertAlmostEqual(parallel(2, 3), 1.2)

    def test_capacitor_charge_and_discharge(self):
        self.assertAlmostEqual(capacitor_time_constant(2_000, 0.001), 2)
        self.assertAlmostEqual(v_charge(0, 10, 2), 0)
        self.assertAlmostEqual(v_discharge(0, 10, 2), 10)
        self.assertAlmostEqual(v_charge(2, 10, 2), 10 * (1 - np.exp(-1)))

    def test_inductor_current_transitions(self):
        self.assertAlmostEqual(inductor_time_constant(4, 2), 0.5)
        self.assertAlmostEqual(i_buildup(0, 12, 4, 0.5), 0)
        self.assertAlmostEqual(i_decay(0, 3, 0.5), 3)
        np.testing.assert_allclose(
            i_decay(np.array([0.0, 0.5]), 3, 0.5), [3, 3 * np.exp(-1)]
        )

    def test_resonant_frequency_vectorizes(self):
        self.assertAlmostEqual(f0(1e-3, 1e-6), 1 / (2 * np.pi * np.sqrt(1e-9)))
        np.testing.assert_allclose(f0_curve(np.array([1e-6, 4e-6]), 1e-3), [
            f0(1e-3, 1e-6),
            f0(1e-3, 4e-6),
        ])

    def test_fault_current_decreases_with_distance(self):
        near = three_phase_fault_current(230, 2, 0.1, 1)
        far = three_phase_fault_current(230, 2, 0.1, 100)
        self.assertGreater(near, far)
        self.assertTrue(np.isfinite(near))


if __name__ == "__main__":
    unittest.main()
