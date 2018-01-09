
import os

current_path = os.path.dirname(__file__)
settings = dict(
	debug = True,
	static_path = os.path.join(current_path, 'static'),
	template_path = os.path.join(current_path, 'template'),
	)