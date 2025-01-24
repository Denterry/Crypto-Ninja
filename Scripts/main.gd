extends Node2D

@onready var tokens = get_node("Tokens")

var lido = preload("res://Scenes/LIDO.tscn")

var scam = preload("res://Scenes/SCAM.tscn")

# Game state
var score = 0
var lives = 3

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Initialize UI
	# update_ui()
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

# Timer callback for generating tokens
func _on_Generator_timeout():
	if lives <= 0:
		return  # Stop spawning tokens if the game is over

	# Spawn between 1 and 3 tokens
	for i in range(randi_range(1, 3)):
		# Randomly select a token type
		var type = randi_range(0, 2)
		var token_instance
		match type:
			0: token_instance = lido.instance()
			1: token_instance = scam.instance()
#
		# Set initial position and add to scene
		token_instance.generate(Vector2(randf_range(300, 980), 800))

		token_instance.connect("life", self, "dec_life")

		if type != 8:
			token_instance.connect("score", self, "inc_score")

		tokens.add_child(token_instance)

		## Connect token signals
		#token_instance.connect("token_missed", self, "_on_token_missed")
		#if type != 4:  # Exclude scam tokens from scoring
			#token_instance.connect("token_collected", self, "_on_token_collected")

func dec_life():
	lives -= 1
	# update_ui()

	# Update UI color for remaining lives
	if lives == 2:
		get_node("Control/Scam3").set_modulate(Color(1, 0 ,0))
	elif lives == 1:
		get_node("Control/Scam2").set_modulate(Color(1, 0 ,0))
	elif lives == 0:
		get_node("Control/Scam1").set_modulate(Color(1, 0 ,0))
		get_node("InputProcessor").gameOver = true
		get_node("GameOverScreen").start()

func inc_score():
	if lives == 0: return
	score += 1
	get_node("Control/Balance").set_text(str(score))

## Increase score when a token is collected
#func _on_token_collected(score_value):
	#if lives == 0:
		#return  # Prevent scoring after the game is over
	#score += score_value
	#update_ui()
#
## Update the UI for score and lives
#func update_ui():
	#ui_control.get_node("Label").text = "Score: %d" % score
	#ui_control.get_node("LivesLabel").text = "Lives: %d" % lives
#
## End the game
#func game_over():
	#print("Game Over! Final Score: %d" % score)
	#ui_control.get_node("GameOverScreen").start()
	#ui_control.get_node("InputProcessor").game_over = true
