// Variables to hold the scores and the correct answer
let correctAnswer = '';
let correctScore = 0;
let incorrectScore = 0;

// Function to handle image clicks for guessing
function handleImageClick(event) {
    const clickedImageFilename = event.target.getAttribute('data-filename');
    if (clickedImageFilename === correctAnswer) {
        correctScore += 1;
        alert('Correct! +1 point');
    } else {
        incorrectScore -= 1;
        alert('Wrong! -1 point');
    }
    // Update the score display
    document.getElementById('correctScore').innerText = `Correct: ${correctScore}`;
    document.getElementById('incorrectScore').innerText = `Incorrect: ${incorrectScore}`;
}

document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display available images
    fetch('/get_images')
    .then(response => response.json())
    .then(images => {
        const imageContainer = document.getElementById('imageContainer');
        images.forEach(image => {
            // Create img element
            const imgElement = document.createElement('img');
            // Adjust the image source to use url_for
            imgElement.src = `/static/images/${image}`;
            imgElement.classList.add('thumbnail');  
            imgElement.setAttribute('data-filename', image);
            imgElement.addEventListener('click', handleImageClick);      
            // Append to image container
            imageContainer.appendChild(imgElement);
        });
    });

    // Handle image prediction
    document.getElementById('predictForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Make sure you are accessing the property 'prediction' of the object
            document.getElementById('prediction').innerText = data.prediction;
        });
    });

    // Define the predict function
    window.predict = function() {
        const imageInput = document.getElementById('imageInput');
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
    
        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Accessing the prediction property from the response object
            document.getElementById('prediction').innerText = data.prediction;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('prediction').innerText = 'Failed to predict.';
        });
    };

    window.randomPredict = function() {
        document.getElementById('prediction').innerText = 'Predicting...';
        fetch('/predict_random')
        .then(response => response.json())
        .then(data => {
            document.getElementById('prediction').innerText = data.prediction;
            correctAnswer = data.filename; // Store the correct answer
        })
        .catch(error => {
            console.error('Error during random prediction:', error);
            document.getElementById('prediction').innerText = 'Error predicting.';
        });
    };

    // New function to highlight the correct answer
    window.revealAnswer = function() {
        const images = document.getElementsByTagName('img');
        for (let img of images) {
            if (img.getAttribute('data-filename') === correctAnswer) {
                img.style.border = '5px solid green';
                break;
            }
        }
    };

});