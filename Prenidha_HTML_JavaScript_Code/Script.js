const PAT = '2efdeb7e08574af883ab3597f535e889';
const USER_ID = 'clarifai';
const APP_ID = 'main';
const MODEL_ID = 'food-item-recognition';
const MODEL_VERSION_ID = '1d5fd481e0cf4826aa72ec3ff049e044';

const calorieMapping = {
    "apple": 52,
    "banana": 89,
    "orange": 47,
    "pizza": 266,
    "burger": 295,
    "salad": 33,
    "sandwich": 200,
    // Add more mappings as needed
};

async function getCaloriesFromImage(imageData) {
    const url = `https://api.clarifai.com/v2/models/${MODEL_ID}/versions/${MODEL_VERSION_ID}/outputs`;

    const raw = JSON.stringify({
        "user_app_id": {
            "user_id": USER_ID,
            "app_id": APP_ID
        },
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": imageData
                    }
                }
            }
        ]
    });

    const requestOptions = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Authorization': 'Key ' + PAT
        },
        body: raw
    };

    const response = await fetch(url, requestOptions);
    const data = await response.json();
    return data;
}

function calculateTotalCalories(foodItems) {
    let totalCalories = 0;
    foodItems.forEach(item => {
        const calories = calorieMapping[item.name.toLowerCase()];
        if (calories) {
            totalCalories += calories;
        }
    });
    return totalCalories;
}

function uploadImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    const imagePreview = document.getElementById('imagePreview');
    const results = document.getElementById('results');

    if (file) {
        const reader = new FileReader();
        reader.onload = async function (e) {
            const imageData = e.target.result.split(',')[1]; // Base64 part of the data URL
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;

            // Call Clarifai API
            try {
                const clarifaiData = await getCaloriesFromImage(imageData);
                const foodItems = clarifaiData.outputs[0].data.concepts;
                let resultHTML = 'Identified Foods:<br>';
                foodItems.forEach(item => {
                    resultHTML += `${item.name}: ${item.value * 100}%<br>`;
                });

                const totalCalories = calculateTotalCalories(foodItems);
                resultHTML += `<br>Total Estimated Calories: ${totalCalories} kcal`;
                results.innerHTML = resultHTML;
            } catch (error) {
                results.innerHTML = `Error: ${error.message}`;
            }
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please select an image file');
    }
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const loginError = document.getElementById('loginError');

    // Simple authentication (replace with actual authentication logic)
    if (username === 'user' && password === 'password') {
        loginError.textContent = '';
        document.getElementById('homePage').classList.add('hidden');
        document.getElementById('trackerPage').classList.remove('hidden');
    } else {
        loginError.textContent = 'Invalid username or password';
    }
}

function logout() {
    document.getElementById('homePage').classList.remove('hidden');
    document.getElementById('trackerPage').classList.add('hidden');
}
