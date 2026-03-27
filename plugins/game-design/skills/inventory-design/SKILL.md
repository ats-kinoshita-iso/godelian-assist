---
name: inventory-design
description: Design an inventory system — ItemData resource schema, inventory container, and equipment slot architecture.
invocation: /inventory-design
---
> **Godot version**: Godot 4.x (4.0+). All code examples use GDScript 2.0 and are not compatible with Godot 3.


Define the data model and management architecture for a typed Godot 4.x inventory system.

## ItemData Resource Schema

Every item is a `Resource` file that can be created in the editor and stored as `.tres`.

```gdscript
class_name ItemData
extends Resource

## Represents a single item definition. Instances are authored as .tres files.

@export var item_id: String = ""          # Unique key: "sword_iron", "potion_health"
@export var display_name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var item_type: ItemType = ItemType.CONSUMABLE
@export var is_stackable: bool = false
@export var max_stack_size: int = 1
@export var weight: float = 0.0
@export var value: int = 0               # Gold/currency value

# Equipment-specific (only relevant when item_type == EQUIPMENT)
@export var equipment_slot: EquipmentSlot = EquipmentSlot.NONE
@export var stat_modifiers: Dictionary = {}  # {"damage": 5, "defense": 2}

# Consumable-specific
@export var use_effect: String = ""       # Method name on consumer: "heal", "restore_stamina"
@export var use_magnitude: float = 0.0

enum ItemType { CONSUMABLE, EQUIPMENT, KEY_ITEM, MATERIAL, CURRENCY }
enum EquipmentSlot { NONE, HEAD, CHEST, LEGS, FEET, MAIN_HAND, OFF_HAND, ACCESSORY }
```

Save item definitions: `res://assets/data/items/sword_iron.tres`, `res://assets/data/items/potion_health.tres`

## Inventory Container

```gdscript
class_name Inventory
extends Node

## Manages a collection of items. Attach to Player or any container node.

signal item_added(item: ItemData, quantity: int)
signal item_removed(item: ItemData, quantity: int)
signal inventory_full()

@export var capacity: int = 20

var _slots: Array[Dictionary] = []  # [{item: ItemData, quantity: int}]

func add_item(item: ItemData, quantity: int = 1) -> bool:
	if item.is_stackable:
		var slot: Dictionary = _find_stack(item)
		if not slot.is_empty():
			slot["quantity"] += quantity
			item_added.emit(item, quantity)
			return true
	if _slots.size() >= capacity:
		inventory_full.emit()
		return false
	_slots.append({"item": item, "quantity": quantity})
	item_added.emit(item, quantity)
	return true

func remove_item(item: ItemData, quantity: int = 1) -> bool:
	for slot: Dictionary in _slots:
		if slot["item"] == item:
			slot["quantity"] -= quantity
			if slot["quantity"] <= 0:
				_slots.erase(slot)
			item_removed.emit(item, quantity)
			return true
	return false

func _find_stack(item: ItemData) -> Dictionary:
	for slot: Dictionary in _slots:
		if slot["item"] == item and slot["quantity"] < item.max_stack_size:
			return slot
	return {}
```

## Equipment Slot Architecture

```gdscript
class_name EquipmentSystem
extends Node

## Manages what is equipped in each slot. Applies stat modifiers from ItemData.

var _equipped: Dictionary = {}  # {EquipmentSlot: ItemData}

signal equipment_changed(slot: ItemData.EquipmentSlot, item: ItemData)

func equip(item: ItemData) -> void:
	if item.equipment_slot == ItemData.EquipmentSlot.NONE:
		return
	_equipped[item.equipment_slot] = item
	equipment_changed.emit(item.equipment_slot, item)

func unequip(slot: ItemData.EquipmentSlot) -> ItemData:
	var item: ItemData = _equipped.get(slot, null)
	_equipped.erase(slot)
	return item

func get_total_modifier(stat: String) -> int:
	var total: int = 0
	for item: ItemData in _equipped.values():
		total += item.stat_modifiers.get(stat, 0)
	return total
```

## Design Questions to Resolve

| Question | Options |
|---|---|
| Item limit | Fixed capacity vs weight limit |
| Equipment slots | Which slots exist for this game? |
| Stack sizes | Max per item type |
| Pickup flow | Auto-pickup vs confirmation prompt |
| Loot sources | Chest scenes, enemy drops, shops |
| Persistence | What saves — full inventory or just key items? |
