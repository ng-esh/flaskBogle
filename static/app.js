$(document).ready(function() {
    let score = 0;
    let highScore = 0; // Track the highest score
    let gamesPlayed = 0; // Track the number of games played
    let timeLeft = 60;
    const timerElement = $('#timer');

    // Function to reset game state
    function resetGame() {
        score = 0;
        timeLeft = 60;
        $('#score').text(`Score: ${score}`);
        $('#timer').text(`Time left: ${timeLeft} seconds`);
        $('#message').text(""); // Clear messages
        $('#guess-form button').prop('disabled', false); // Enable form button
    }

    // Start the countdown timer
    const timerInterval = setInterval(function() {
        timeLeft -= 1;
        timerElement.text(`Time left: ${timeLeft} seconds`);

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            $('#guess-form button').prop('disabled', true);
            $('#message').text("Time's up!");

            // Send score and games played to the server
            gamesPlayed += 1; // Increment the number of games played
            if (score > highScore) {
                highScore = score; // Update highest score if needed
            }

            axios.post('/post-score', {
                score: score,
                gamesPlayed: gamesPlayed,
                highScore: highScore
            });
        }
    }, 1000);

    $('#guess-form').on('submit', function(event) {
        event.preventDefault();
        const guess = $(this).find('input[name="guess"]').val();

        axios.post('/check-word', { word: guess }) // Ensure the word is sent as JSON
            .then(response => {
                const result = response.data.result;

                if (result === "ok") {
                    const wordScore = guess.length;
                    score += wordScore;
                    $('#score').text(`Score: ${score}`);
                    $('#message').text("Valid word!");
                } else if (result === "not-on-board") {
                    $('#message').text("The word is not on the board.");
                } else {
                    $('#message').text("Not a valid word.");
                }
            });
    });

    // Reset game when the page is loaded
    resetGame();
});
