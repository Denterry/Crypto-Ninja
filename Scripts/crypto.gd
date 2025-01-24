extends RigidBody2D

@onready var shape = get_node("CollisionShape2D")
@onready var sprite0 = get_node("Sprite2D")
@onready var body1 = get_node("LeftBody")
@onready var body2 = get_node("RightBody")
@onready var sprite1 = get_node("LeftBody/Sprite2D")
@onready var sprite2 = get_node("RightBody/Sprite2D")

# State variables
var did_cut = false  # To prevent multiple cuts

# Signals
signal score
signal life

# Crypto properties
#var token_type = "frax"  # Example: "bitcoin", "ethereum", "scam"
#var score_value = 10  # Score for this token

# Called when the node enters the scene tree for the first time.
func _ready():
	randomize()
	print("Crypto script initialized!")

# Generate initial position and velocity
func generate(initial_pos):
	global_position = initial_pos
	var initial_velocity = Vector2(0, randf_range(-1000, -800))

	# Adjust trajectory based on spawn position
	if initial_pos.x < 640:  # Screen's left half
		initial_velocity = initial_velocity.rotated(deg_to_rad(randf_range(0, -30)))
	else:  # Screen's right half
		initial_velocity = initial_velocity.rotated(deg_to_rad(randf_range(0, 30)))

	# Assign initial velocity and rotation
	linear_velocity = initial_velocity
	angular_velocity = randf_range(-10, 10)

# Cutting logic
func cut():
	if did_cut:
		return
	did_cut = true
	
	# Emit score signal
	emit_signal("score")

	# Disable the main body
	freeze_mode = RigidBody2D.FREEZE_MODE_KINEMATIC  # Disable physics for the main crypto
	sprite0.queue_free()  # Remove the original sprite
	shape.queue_free()  # Remove the collision shape

	# Activate and split the two halves
	body1.freeze_mode = RigidBody2D.FREEZE_MODE_STATIC
	body2.freeze_mode = RigidBody2D.FREEZE_MODE_STATIC

	# Apply impulses to make the halves fly apart
	body1.apply_impulse(Vector2.ZERO, Vector2(-100, 0).rotated(rotation))
	body2.apply_impulse(Vector2.ZERO, Vector2(100, 0).rotated(rotation))

	# Add angular velocity for spinning effect
	body1.angular_velocity = angular_velocity
	body2.angular_velocity = angular_velocity

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if global_position.y > 800:  # Check if the crypto has fallen below the screen
		emit_signal("life")
		queue_free()
	if body1.global_position.y > 800 and body2.global_position.y > 800:
		queue_free()
