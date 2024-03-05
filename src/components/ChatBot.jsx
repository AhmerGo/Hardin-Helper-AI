import React, { useState } from "react";

function ChatBot() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  
  const sendMessage = async () => {
    if (message.trim() === "") {
      // Optionally handle empty message case
      return;
    }

    // Update chat history with the new message
    const newMessage = { text: message, sender: "user" };
    setChatHistory([...chatHistory, newMessage]);

    setMessage("");
    document.getElementById("loading").classList.remove("hidden");
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Auth Headers
        },
        body: JSON.stringify({ user_input: message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        document.getElementById("loading").classList.add("hidden");
      }

      const responseData = await response.json();
      console.log(responseData); // Add this line to log the response data

      // Update chat history with the response
      setChatHistory([
        ...chatHistory,
        newMessage,
        { text: responseData.reply, sender: "bot" },
      ]);
      document.getElementById("loading").classList.add("hidden");
    } catch (error) {
      console.error("Failed to send message:", error);
      // Optionally handle the error in UI
      document.getElementById("loading").classList.add("hidden");
    }
  };

  function clearChat(){
    const parent = document.getElementById("chatHistory");
    const children = parent.children;
    Array.from(children).forEach(function(child) {
      child.remove();
  }); 
  }

  function clearInput(){
    let input = document.getElementById("input-box");
    input.value = "";
  }


  function saveChat(){
    const userInputs = document.querySelectorAll(".message.user");
    const botInputs = document.querySelectorAll(".message.bot");
    Array.from(userInputs).forEach(function(input) {
      // Replace this wit database stuff later and include another function for bot inputs
      alert(input.textContent);
    }); 
  }



  return (
      <div className="chat-section relative  flex flex-col h-96 bg-purple rounded-xl shadow-2xl p-6 ">
        <div className="flex-grow overflow-auto mb-4 p-4 bg-white rounded-xl shadow-inner" id="chatHistory">
          {chatHistory.map((chat, index) => (
            <div key={index} className={`message ${chat.sender}`}>
              {chat.sender}:{chat.text}
              <br />
            </div>
          ))}
          <div id="loading" class="text-right rtl:text-right hidden">
              <div role="status">
                <svg aria-hidden="true" class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                  <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
          </div>
        </div>
        <div className="flex border-t border-gray-200 pt-4">
          <textarea
            id="input-box"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter"){
                e.preventDefault();
                sendMessage();
                clearInput();
              }
              }}
            className="flex-grow p-3 border border-gray-300 rounded-l-xl focus:outline-none  focus:border-transparent"
            placeholder="Type your message..."
            style={{ resize: "none" }}
          />
          <button
            onClick={sendMessage}
            className="bg-[#401486] text-white p-3 rounded-r-xl shadow-md hover:bg-purple-700 transition duration-300 ease-in-out transform hover:text-gold hover:scale-105"
          >
            Send
          </button>
        </div>
        <div className="flex justify-evenly my-2.5">
          <button onClick={clearChat}
            className="bg-[#401486] text-white p-3 rounded-xl shadow-md focus:outline-none transition duration-300 ease-in-out transform hover:text-gold transform hover:scale-105"
            >
            Clear Chat
          </button>
          <button onClick={saveChat}
            className="bg-[#401486] text-white p-3 rounded-xl shadow-md focus:outline-none transition duration-300 ease-in-out transform hover:text-gold transform hover:scale-105"

          >
            Save Chat
          </button>
        </div>
      </div>
  );
}

export default ChatBot;
