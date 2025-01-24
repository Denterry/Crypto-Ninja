extends Node2D

@onready var limit = get_node("Limit")
@onready var interval = get_node("Interval")

var is_pressed = false
var is_dragging = false
var cur_position = Vector2(0, 0)
var prev_position = Vector2(0, 0)

var game_over = false

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Ensure timers are stopped initially
	#limit.stop()
	#interval.stop()
	pass # Replace with function body.

func _input(event):
	# For coordinates to fit the local device screen
	event = make_input_local(event)
	if event is InputEventScreenTouch:
		if event.pressed:
			on_pressed(event.position)
		else:
			on_released()
	elif event is InputEventScreenDrag:
		on_drag(event.position)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	queue_redraw()  # Call _draw() for visual feedback
	if is_dragging and cur_position != prev_position and prev_position != Vector2(0, 0) and not game_over:
		# Perform raycasting to detect interactions
		var space_state = get_world_2d().get_direct_space_state()
		
		# Create a ray query
		var query = PhysicsRayQueryParameters2D.new()
		query.from = prev_position
		query.to = cur_position

		# Perform the raycast
		var result = space_state.intersect_ray(query)

		if result.size() > 0:
			# Call the `cut()` method of the collided object (e.g., token)
			if result.collider.has_method("cut"):
				result.collider.cut()

func on_pressed(position: Vector2) -> void:
	is_pressed = true
	prev_position = position
	limit.start()
	interval.start()

func on_released():
	is_pressed = false
	is_dragging = false
	limit.stop()
	interval.stop()
	prev_position = Vector2(0, 0)
	cur_position = Vector2(0, 0)

func on_drag(position: Vector2) -> void:
	cur_position = position
	is_dragging = true

func _on_interval_timeout() -> void:
	prev_position = cur_position  # Update previous position at regular intervals

func _on_limit_timeout() -> void:
	on_released()  # Automatically release touch if the time limit is exceeded

func _draw() -> void:
	if is_dragging and cur_position != prev_position and prev_position != Vector2(0, 0) and not game_over:
		draw_line(cur_position, prev_position, Color(1, 0 ,0), 10)
