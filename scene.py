class Scene:
    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class SceneManager:
    def __init__(self):
        self._stack = []
        self.should_quit = False

    @property
    def active(self):
        return len(self._stack) > 0

    def push(self, scene):
        if self._stack:
            self._stack[-1].on_exit()
        scene.on_enter()
        self._stack.append(scene)

    def pop(self):
        if self._stack:
            self._stack.pop().on_exit()
            if self._stack:
                self._stack[-1].on_enter()

    def replace(self, scene):
        if self._stack:
            self._stack.pop().on_exit()
        scene.on_enter()
        self._stack.append(scene)

    def quit(self):
        self.should_quit = True

    def handle_event(self, event):
        if self._stack:
            self._stack[-1].handle_event(event)

    def update(self, dt):
        if self._stack:
            self._stack[-1].update(dt)

    def draw(self, surface):
        if self._stack:
            self._stack[-1].draw(surface)