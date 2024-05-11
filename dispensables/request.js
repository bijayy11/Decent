// Function to upload data to Flask server
function uploadData() {
    // Create FormData object to store form data
    var formData = new FormData();
    
    // Get file input element and append selected file to FormData
    var imageFile = document.getElementById('imageFileInput').files[0];
    formData.append('image_path', imageFile);
    
    // Get username and public key from input fields
    var username = document.getElementById('usernameInput').value;
    var publicKey = document.getElementById('publicKeyInput').value;
    
    // Append username and public key to FormData
    formData.append('username', username);
    formData.append('public_key', publicKey);

    // Send POST request to Flask server
    fetch('/store', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from server
        console.log(data);
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error);
    });
}
