import { AES, lib } from "crypto-js";

// Listen for message from content script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    const encryptedMessage = encryptMessage(request.message);
    sendResponse({ encryptedMessage });    // Send the encrypted message back to content script
});

function encryptMessage(message) {
    const secretKey = generateSecureKey(); //key generation for AES encryption
    const encrypted = AES.encrypt(message, secretKey).toString();    // Encrypt the message using AES encryption

    return encrypted;
}
function generateSecureKey() {
    const key = lib.WordArray.random(16); // 128 bits key length
    return key;
}