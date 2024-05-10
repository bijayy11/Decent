document.addEventListener("DOMContentLoaded", () => {
    const messageForm = document.getElementById("messageForm");
    const messageInput = document.getElementById("messageInput");
    const resultDiv = document.getElementById("result");
  
    messageForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      
      const message = messageInput.value.trim();
  
      if (message !== "") {
        // Send message to background script for encryption/decryption
        const encryptedResult = await sendMessageToBackground({ type: "ENCRYPT", text: message });
        resultDiv.textContent = `Encrypted Message: ${encryptedResult.encryptedMessage}`;
        
        // For decryption, uncomment the following lines
        // const decryptedResult = await sendMessageToBackground({ type: "DECRYPT", text: encryptedResult.encryptedMessage });
        // resultDiv.textContent = `Decrypted Message: ${decryptedResult.decryptedMessage}`;
      } else {
        resultDiv.textContent = "Please enter a message.";
      }
    });
  });
  
  async function sendMessageToBackground(message) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(message, (response) => {
        resolve(response);
      });
    });
  }
  