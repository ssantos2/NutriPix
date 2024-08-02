Steps to Execute & View App
----------------------------
Clone the repository and navigate to the 'Prenidha_HTML_JavaScript_Code' folder.
Click Open the Html file to view the app in the browser
Enter username - user
Enter password - password
Click Login button

Click Choose Image 
Upload a food image

Rough calorie Estimate will be displayed

Note: The Calorie count is not accurate as this is a demo of how the app can look like in terms of UI and integrating the API. The AI Api to be used is yet to be finalized and code has to be improvised.


Setup & Instructions:
---------------------
This setup should allow you to upload an image, send it to Clarifai for analysis, and display the identified food items along with their probabilities. 

This simple app uses the following technologies:
- HTML: Updated to include labels and structure more suitable for mobile.
- CSS: Styled for mobile responsiveness with better touch targets.
- JavaScript: Integrates the Clarifai API call and processes the response for calorie calculation.
This should give your application a mobile-friendly design while keeping the functionality intact.

Clarifai API (Clarifai: Provides a range of image recognition models, including a food model that can identify food items in an image i.e Clarifai Food Model)
Clarifai itself doesn't provide calorie information directly, but it can identify food items in images. To fully estimate calories, you might need additional logic to map identified foods to calorie counts using a nutrition database. Here's a more detailed integration example using Clarifai's Food Model, with the addition of mapping identified foods to their calorie values.

Prerequisites 
-------------
Steps done to Use Clarifai Food Model

Note: You dont need to perform these steps as it has already been done and API Key is provided in code

1. Sign Up and Get API Key:
- Clarifai API Key: Sign up at Clarifai, create an application, and get your API key.
- Integrate Clarifai API in JavaScript

2. Nutrition Database: You need a database or API to map food items to their calorie values. For simplicity, we'll use a static mapping in this example.

Explanation
------------
-Clarifai Request Setup: The provided Clarifai request code is integrated into the getCaloriesFromImage function.
-Image Upload Handling: The uploadImage function handles the image upload, reads the image file as a Base64 string, and sends it to Clarifai.
-Response Processing: The response from Clarifai is processed to identify food items and calculate the total calories using the calorieMapping.

-Calorie Mapping: A static object calorieMapping is created to map identified food items to their calorie values.
-getCaloriesFromImage: This function sends the image to Clarifai's Food Model API and returns the identified food items.
-calculateTotalCalories: This function calculates the total calories based on the identified food items and the calorie mapping.
-uploadImage: This function handles the image upload, displays the image preview, and calls the Clarifai API. It also processes the response to calculate and display the total estimated calories.




