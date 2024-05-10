// content.js

// Listen for changes in the chatbox
document.addEventListener('input', async function(event) {
    const inputElement = event.target;
    
    // Check if the input element is the chatbox
    if (inputElement && inputElement.getAttribute('role') === 'textbox') {
      // Read the text from the chatbox
      const message = inputElement.innerText;
  
      // Send the message to background script for encryption
      chrome.runtime.sendMessage({ message }, function(response) {
        // Replace the original message with the encrypted one
        inputElement.innerText = response.encryptedMessage;
      });
    }
  });
  