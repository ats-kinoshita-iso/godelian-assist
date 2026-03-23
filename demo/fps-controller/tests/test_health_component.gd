## Tests for HealthComponent.
## Plugin used: test-quality/test-gen-godot
class_name TestHealthComponent extends GdUnitTestSuite

var _health: HealthComponent


func before_test() -> void:
    _health = auto_free(HealthComponent.new())
    _health.max_health = 100.0
    _health.invincibility_time = 0.0  # disable i-frames for most tests
    add_child(_health)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

func test_starts_at_max_health() -> void:
    assert_float(_health.current_health).is_equal(100.0)


func test_is_not_dead_at_start() -> void:
    assert_bool(_health.is_dead).is_false()


# ---------------------------------------------------------------------------
# take_damage
# ---------------------------------------------------------------------------

func test_take_damage_reduces_health() -> void:
    _health.take_damage(30.0)
    assert_float(_health.current_health).is_equal(70.0)


func test_take_damage_does_not_go_below_zero() -> void:
    _health.take_damage(999.0)
    assert_float(_health.current_health).is_greater_equal(0.0)


func test_take_damage_returns_actual_amount() -> void:
    var dealt: float = _health.take_damage(40.0)
    assert_float(dealt).is_equal(40.0)


func test_take_damage_caps_at_remaining_health() -> void:
    _health.current_health = 20.0
    var dealt: float = _health.take_damage(50.0)
    assert_float(dealt).is_equal(20.0)


func test_take_damage_emits_health_changed() -> void:
    var monitor := monitor_signals(_health)
    _health.take_damage(10.0)
    assert_signal(monitor).is_emitted("health_changed")


func test_take_damage_to_zero_emits_died() -> void:
    var monitor := monitor_signals(_health)
    _health.take_damage(100.0)
    assert_signal(monitor).is_emitted("died")


func test_take_damage_sets_is_dead() -> void:
    _health.take_damage(100.0)
    assert_bool(_health.is_dead).is_true()


func test_damage_blocked_when_dead() -> void:
    _health.kill()
    var dealt: float = _health.take_damage(50.0)
    assert_float(dealt).is_equal(0.0)


# ---------------------------------------------------------------------------
# Invincibility frames
# ---------------------------------------------------------------------------

func test_second_hit_blocked_during_invincibility() -> void:
    _health.invincibility_time = 5.0
    _health.take_damage(10.0)
    var dealt: float = _health.take_damage(10.0)
    assert_float(dealt).is_equal(0.0)
    assert_float(_health.current_health).is_equal(80.0)


# ---------------------------------------------------------------------------
# heal
# ---------------------------------------------------------------------------

func test_heal_increases_health() -> void:
    _health.current_health = 50.0
    _health.heal(20.0)
    assert_float(_health.current_health).is_equal(70.0)


func test_heal_does_not_exceed_max() -> void:
    _health.current_health = 90.0
    _health.heal(50.0)
    assert_float(_health.current_health).is_equal(100.0)


func test_heal_emits_health_changed() -> void:
    var monitor := monitor_signals(_health)
    _health.current_health = 50.0
    _health.heal(10.0)
    assert_signal(monitor).is_emitted("health_changed")


# ---------------------------------------------------------------------------
# kill
# ---------------------------------------------------------------------------

func test_kill_sets_health_to_zero() -> void:
    _health.kill()
    assert_float(_health.current_health).is_equal(0.0)


func test_kill_emits_died() -> void:
    var monitor := monitor_signals(_health)
    _health.kill()
    assert_signal(monitor).is_emitted("died")


# ---------------------------------------------------------------------------
# get_fraction
# ---------------------------------------------------------------------------

func test_get_fraction_full_health() -> void:
    assert_float(_health.get_fraction()).is_equal(1.0)


func test_get_fraction_half_health() -> void:
    _health.current_health = 50.0
    assert_float(_health.get_fraction()).is_equal_approx(0.5, 0.001)


func test_get_fraction_zero_max_health_safe() -> void:
    _health.max_health = 0.0
    assert_float(_health.get_fraction()).is_equal(0.0)
