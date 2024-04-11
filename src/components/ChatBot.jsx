import React, { useState, useEffect, useRef } from "react";
import logo_white from "../assets/HSU_logo.webp";
function ChatBot() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const chatHistoryRef = useRef(null);
  useEffect(() => {
    // Scroll to the bottom of the chat history container when chat history updates
    chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
  }, [chatHistory]);


  const sendMessage = async () => {
    if (message.trim() === "") {
      // Optionally handle empty message case
      return;
    }
    document.getElementById("sendButton").disabled = true;
    // Update chat history with the new message
    const newMessage = { text: message, sender: "You" };
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
        { text: responseData.reply, sender: "HossBot" },
      ]);
      document.getElementById("loading").classList.add("hidden");
    } catch (error) {
      console.error("Failed to send message:", error);
      // Optionally handle the error in UI
      document.getElementById("loading").classList.add("hidden");
    }
  };

  function clearChat() {
    const parent = document.getElementById("chatHistory");
    const children = parent.children;
    Array.from(children).forEach(function (child) {
      child.classList.add("hidden");
    });
  }

  function clearInput() {
    let input = document.getElementById("input-box");
    input.value = "";
  }

  window.addEventListener("beforeunload", (ev)=>{
    ev.preventDefault();
    saveChat(0);
  })

  
  

  function saveChat(rating) {
    var userInput = document.querySelectorAll("[class*='message You']");
    alert(userInput[0].textContent);
    var botInputs = document.querySelectorAll("[class*='message HossBot']");
    alert(rating);
    userInput[0].classList.remove("message");
    document.getElementById("sendButton").disabled = false;
    document.getElementById("rating").classList.add("hidden");
    // const userInputs = Array.from(
    //   document.querySelectorAll(".message.You")
    // ).map((input) => input.textContent);
    // const botInputs = Array.from(document.querySelectorAll(".message.HossBot")).map(
    //   (input) => input.textContent
    // );

    // fetch("http://localhost:5000/save_chat", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({
    //     user_inputs: userInputs,
    //     bot_inputs: botInputs,
    //   }),
    // })
    //   .then((response) => {
    //     if (!response.ok) {
    //       throw new Error(`HTTP error! Status: ${response.status}`);
    //     }
    //     return response.json();
    //   })
    //   .then((data) => {
    //     console.log("Chat saved successfully:", data);
    //   })
    //   .catch((error) => {
    //     console.error("Failed to save chat:", error);
    //   });
  }

  return (

      <div className="w-full xsml:w-full flex justify-center items-center bg-hsu bg-center bg-no-repeat h-screen">
        <div className="chat-section w-3/4  h-3/4 xsml:w-full relative  flex flex-col bg-purple rounded-xl shadow-2xl p-6 ">
          <div className="w-full flex justify-between mb-6">
            {/* contains buttons on top of chat area */}
            <div className="w-1/4 rounded">
              <a href="https://www.hsutx.edu/">
              <img src={logo_white} alt="" />
              </a>
            </div>
              <button onClick={clearChat}
                className="bg-[#401486] text-white p-3 rounded-xl shadow-md focus:outline-none transition duration-300 ease-in-out transform hover:text-gold transform hover:scale-105"
                >
                Clear Chat
              </button>
          </div>
            <div className="h-1/2 mb-4 p-4 bg-white rounded-xl shadow-inner overflow-auto" id="chatHistory" ref={chatHistoryRef}>
              {chatHistory.map((chat, index) => (
                <div key={index} className={`message ${chat.sender} ${chat.sender ==='You' ? 'rounded-r-lg': 'rounded-l-lg ml-auto'} rounded-b-lg  bg-[#D8D8D8] text-purple w-fit  flex`}>
                <b>{chat.sender}:</b> <br />
                {chat.text}
                <br />
              </div>
              ))}
              <div id="loading" className="text-right rtl:text-right hidden">
                  <div role="status">
                    HossBot is typing...
                  </div>
              </div>
              <div id="rating" className="text-right rtl:text-right ">
              <p>Was this chat helpful, not, or inappropriate</p>
              <button id="thumbsUpBtn" className="thumbs-up" onClick={() =>saveChat(1)}>👍</button>
              <button id="thumbsDownBtn" className="thumbs-down" onClick={() =>saveChat(2)}>👎</button>
              <button id="inappropriateBtn" className="inappropriate" onClick={() =>saveChat(3)}>❗</button>
              </div>

            </div>
            <div className="flex border-t border-gray-200 pt-4">
              <textarea
                id="input-box"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                  if(document.getElementById("sendButton").disabled == false){
                    if (e.key === "Enter"){
                      e.preventDefault();
                      sendMessage();
                      clearInput();
                    }
                  }
                  }}
                className="flex-grow p-3 border border-gray-300 rounded-l-xl focus:outline-none  focus:border-transparent"
                placeholder="Type your message..."
                style={{ resize: "none" }}
              />
              <button
                id="sendButton"
                onClick={sendMessage}
                className="bg-[#401486] text-white p-3 rounded-r-xl shadow-md hover:bg-purple-700 transition duration-300 ease-in-out transform hover:text-gold hover:scale-105"
              >
                Send
              </button>
            </div>
            <div className="flex justify-evenly my-2.5">
              {/* <button onClick={saveChat}
                className="bg-[#401486] text-white p-3 rounded-xl shadow-md focus:outline-none transition duration-300 ease-in-out transform hover:text-gold transform hover:scale-105"
                >
                Save Chat
              </button> */}
            </div>
          </div>
      </div>

  );
}

export default ChatBot;
