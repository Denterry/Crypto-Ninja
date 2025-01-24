extends RigidBody2D

@onready var shape = get_node("CollisionShape2D")
@onready var sprite = get_node("Sprite2D")

signal score
signal life  # Signal emitted when the scam token is cut

var is_cut = false  # Tracks if the token has already been cut

# Called when the node enters the scene tree for the fsirst time.
func _ready() -> void:
	randomize()

# Generates the scam token at a specific position with initial velocity and rotation
func generate(initial_pos: Vector2) -> void:
	global_position = initial_pos
	var initial_vel = Vector2(0, randf_range(-1000, -800))
	
	# Adjust trajectory based on position (left or right side of the screen)
	if initial_pos.x < 640:
		initial_vel = initial_vel.rotated(deg_to_rad(randf_range(0, -30)))
	else:
		initial_vel = initial_vel.rotated(deg_to_rad(randf_range(0, 30)))
	
	linear_velocity = initial_vel
	angular_velocity = randf_range(-10, 10)

# Handles cutting the scam token
func cut() -> void:
	if is_cut:
		return
	is_cut = true

	# Emit a signal to decrease a life or penalize the player
	emit_signal("life")

	# Switch to kinematic mode to stop physics interactions
	freeze_mode = RigidBody2D.FREEZE_MODE_KINEMATIC
	set_freeze_mode(RigidBody2D.FREEZE_MODE_KINEMATIC)

	# Disable further collisions
	shape.disabled = true

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if global_position.y > 800:
		queue_free()
