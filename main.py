from time import sleep
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.clock import Clock


# Main Ping widget
class Pong_Game(Widget):
    game_over = False
    result = StringProperty('')
    ball = ObjectProperty(None)
    left_paddle = ObjectProperty(None)
    right_paddle = ObjectProperty(None)

    # Method to give initial velocity for serving
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        sleep(0.1)

    # Method to update momonet of ball per second
    def update(self, fps):

        self.ball.Moment()

        # Bouncing from boundries of top and bottom
        if (self.ball.y < 0 or self.ball.y > self.height - 40):
            self.ball.velocity_y *= -1

        # Handling left boundary
        if self.ball.x < self.x:

            # Adding score to right paddle
            self.right_paddle.score += 1
            # subtracting score of own
            self.left_paddle.score -= 1

            # Checking for Winner
            if self.right_paddle.score == 5:
                self.result = "Blue Wins!"
                self.game_over = True
                Clock.unschedule(self.update)
            elif self.left_paddle.score == 5:
                self.result = "Red Wins!"
                self.game_over = True
                Clock.unschedule(self.update)

            # if there no winner
            if not self.game_over:
                # Changing direction of ball in x-direction and serving from center
                self.serve_ball(vel=(4, 0))

        # Handling right boundary
        if self.ball.x > self.width - 40:

            # Adding score to left paddle
            self.left_paddle.score += 1
            # subtracting score of own
            self.right_paddle.score -= 1

            # Checking for Winner
            if self.right_paddle.score == 5:
                self.result = "Blue Wins!"
                self.game_over = True
                Clock.unschedule(self.update)
            elif self.left_paddle.score == 5:
                self.result = "Red Wins!"
                self.game_over = True
                Clock.unschedule(self.update)

            # if there no winner
            if not self.game_over:
                # Changing direction of ball in x-direction and serving from center
                self.serve_ball(vel=(-4, 0))

        # Checking collision with paddle
        self.left_paddle.bounce_from_paddle(self.ball)
        self.right_paddle.bounce_from_paddle(self.ball)

    # Motion of paddles
    def on_touch_move(self, touch):
        if touch.x < self.width / 4:
            self.left_paddle.center_y = touch.y

        if touch.x > self.width * (3 / 4):
            self.right_paddle.center_y = touch.y


class PongBall(Widget):
    # Initialing velocity of ball
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def Moment(self):
        # Current Position of ball in vector form
        self.pos = Vector(*self.velocity) + self.pos


class Pongpadle(Widget):
    # Initializing score as zero
    score = NumericProperty(0)

    # Method that cares the collision between paddle and ball
    def bounce_from_paddle(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            # Incresing speed by 1.1 times after collision
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


# Using MDApp
class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.event = None
        self.title = "Ping Pong Game"
        self.icon = "pingpong.ico"
        super().__init__(**kwargs)

    def build(self):
        game = Pong_Game()

        # To serve ball initially
        game.serve_ball()

        # Clock which call update function 60 times per second
        self.event = Clock.schedule_interval(game.update, 1.0 / 60.0)

        return game


# Main Function
if __name__ == '__main__':
    MainApp().run()
