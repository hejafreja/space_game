WHITE = (255, 255, 255)


class Score:
    """This class represents player's score, handling score updates, smooth transitions,
    drawing, and resetting."""

    def __init__(self, font):
        """
        Initializes score object with a font and sets initial score to zero.
        :param font: The font used to display the score
        """
        self.font = font
        self.displayed_score = 0  # The score currently shown on screen (for smooth transitions)
        self.target_score = 0  # The actual score

    def change_score(self, points):
        """Adjusts the target score by a given number of points, ensuring it does not fall below zero."""
        self.target_score += points
        if self.target_score < 0:
            self.target_score = 0  # Prevents negative scores

    def update(self):
        """Updates the displayed score one by one to approach the target score with a smooth transition."""
        if self.displayed_score < self.target_score:
            self.displayed_score += 1
        elif self.displayed_score > self.target_score:
            self.displayed_score -= 1

    def draw(self, screen):
        """Renders and displays the current score on the bottom right of the screen."""
        score_text = self.font.render("SCORE: " + str(self.displayed_score), True, WHITE)
        screen.blit(score_text, (610, 562))

    def reset(self):
        """Resets both the displayed score and the target score to zero."""
        self.displayed_score = 0
        self.target_score = 0
