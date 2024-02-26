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

    try {
      // Need to find GPT4ALL api endpoint
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
      }

      const responseData = await response.json();
      console.log(responseData); // Add this line to log the response data

      // Update chat history with the response
      setChatHistory([
        ...chatHistory,
        newMessage,
        { text: responseData.reply, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Failed to send message:", error);
      // Optionally handle the error in UI
    }
  };

  function clearChat(){
    const parent = document.getElementById("chatHistory");
    const children = parent.children;
    Array.from(children).forEach(function(child) {
      child.remove();
  }); 
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
    <div className="chat-section flex flex-col h-96 bg-purple rounded-xl shadow-2xl p-6">
      <div className="flex-grow overflow-auto mb-4 p-4 bg-white rounded-xl shadow-inner" id="chatHistory">
        {chatHistory.map((chat, index) => (
          <div key={index} className={`message ${chat.sender}`}>
            {chat.text}
          </div>
        ))}
      </div>
      <div className="flex border-t border-gray-200 pt-4">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-grow p-3 border border-gray-300 rounded-l-xl focus:outline-none  focus:border-transparent"
          placeholder="Type your message..."
          style={{ resize: "none" }}
        />
        <button
          onClick={sendMessage}
          className="bg-[#401486] text-white p-3 rounded-r-xl shadow-md hover:bg-purple-700  focus:ring-4 focus:ring-purple-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:text-gold hover:scale-105"
        >
          Send
        </button>
      </div>
      <div className="flex justify-evenly my-2.5">
        <button onClick={clearChat}
          className="bg-[#401486] text-white p-3 rounded-xl shadow-md focus:outline-none focus:ring-4 focus:ring-purple-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:text-gold transform hover:scale-105"
          >
          Clear Chat
        </button>
        <button onClick={saveChat}
          className="bg-[#401486] text-white p-3 rounded-xl shadow-md focus:outline-none focus:ring-4 focus:ring-purple-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:text-gold transform hover:scale-105"

        >
          Save Chat
        </button>
      </div>
    </div>
  );
}

export default ChatBot;