## Tests for StaminaComponent.
## Plugin used: test-quality/test-gen-godot
class_name TestStaminaComponent extends GdUnitTestSuite

var _stamina: StaminaComponent


func before_test() -> void:
    _stamina = auto_free(StaminaComponent.new())
    _stamina.max_stamina = 100.0
    _stamina.drain_rate = 50.0       # drain 50/s — fast for testing
    _stamina.regen_rate = 25.0       # regen 25/s
    _stamina.regen_delay = 0.0       # no delay in tests
    _stamina.sprint_min_stamina = 10.0
    add_child(_stamina)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

func test_starts_at_max_stamina() -> void:
    assert_float(_stamina.current_stamina).is_equal(100.0)


func test_is_not_depleted_at_start() -> void:
    assert_bool(_stamina.is_depleted).is_false()


# ---------------------------------------------------------------------------
# Draining
# ---------------------------------------------------------------------------

func test_drain_reduces_stamina_over_time() -> void:
    _stamina.start_drain()
    _stamina._process(1.0)   # simulate 1 second
    assert_float(_stamina.current_stamina).is_less(100.0)


func test_drain_by_expected_amount() -> void:
    _stamina.start_drain()
    _stamina._process(1.0)
    # drain_rate=50, 1 second => stamina = 50
    assert_float(_stamina.current_stamina).is_equal_approx(50.0, 0.01)


func test_stop_drain_halts_reduction() -> void:
    _stamina.start_drain()
    _stamina._process(0.5)
    var after_half: float = _stamina.current_stamina
    _stamina.stop_drain()
    _stamina._process(1.0)
    assert_float(_stamina.current_stamina).is_equal_approx(after_half, 0.01)


func test_drain_to_zero_sets_depleted() -> void:
    _stamina.start_drain()
    _stamina._process(2.1)   # 100 / 50 = 2s to empty + buffer
    assert_bool(_stamina.is_depleted).is_true()


func test_drain_to_zero_emits_depleted_signal() -> void:
    var monitor := monitor_signals(_stamina)
    _stamina.start_drain()
    _stamina._process(2.1)
    assert_signal(monitor).is_emitted("depleted")


func test_stamina_does_not_go_below_zero() -> void:
    _stamina.start_drain()
    _stamina._process(10.0)
    assert_float(_stamina.current_stamina).is_greater_equal(0.0)


# ---------------------------------------------------------------------------
# Regeneration
# ---------------------------------------------------------------------------

func test_regen_restores_stamina() -> void:
    _stamina.current_stamina = 50.0
    _stamina._process(1.0)   # not draining, regen_delay=0
    assert_float(_stamina.current_stamina).is_greater(50.0)


func test_regen_by_expected_amount() -> void:
    _stamina.current_stamina = 50.0
    _stamina._process(1.0)
    # regen_rate=25, 1 second => stamina = 75
    assert_float(_stamina.current_stamina).is_equal_approx(75.0, 0.01)


func test_regen_does_not_exceed_max() -> void:
    _stamina.current_stamina = 95.0
    _stamina._process(2.0)
    assert_float(_stamina.current_stamina).is_equal(100.0)


func test_recovery_emits_recovered_signal() -> void:
    # deplete fully
    _stamina.start_drain()
    _stamina._process(2.1)
    assert_bool(_stamina.is_depleted).is_true()

    var monitor := monitor_signals(_stamina)
    _stamina.stop_drain()
    # regen enough to cross sprint_min_stamina (10.0), regen_rate=25 => 0.4s
    _stamina._process(0.5)
    assert_signal(monitor).is_emitted("recovered")


func test_recovery_clears_depleted_flag() -> void:
    _stamina.start_drain()
    _stamina._process(2.1)
    _stamina.stop_drain()
    _stamina._process(0.5)
    assert_bool(_stamina.is_depleted).is_false()


# ---------------------------------------------------------------------------
# get_fraction
# ---------------------------------------------------------------------------

func test_get_fraction_full() -> void:
    assert_float(_stamina.get_fraction()).is_equal(1.0)


func test_get_fraction_half() -> void:
    _stamina.current_stamina = 50.0
    assert_float(_stamina.get_fraction()).is_equal_approx(0.5, 0.001)


func test_get_fraction_zero_max_safe() -> void:
    _stamina.max_stamina = 0.0
    assert_float(_stamina.get_fraction()).is_equal(0.0)
