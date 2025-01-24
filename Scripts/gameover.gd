extends Control

var canTouch = false

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.

func start():
	show()
	get_node("AnimationPlayer").play("GameOver")
	get_node("Timer").start()

## Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta: float) -> void:
	#pass

func _on_timer_timeout() -> void:
	canTouch = true
	get_node("Label2").show()

func _input(event):
	if event is InputEventScreenTouch and canTouch:
		get_tree().reload_current_scene()
