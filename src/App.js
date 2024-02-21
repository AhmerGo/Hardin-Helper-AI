import React from "react";
import Header from "./components/Header";
import ChatBot from "./components/ChatBot";
import Navbar from "./components/Navbar";

function App() {
  return (
    <div className="bg-purple-200 min-h-screen flex flex-col">
      <Header />
      <Navbar />
      <div className="bg-white rounded-lg shadow-lg p-6 m-4">
        <h1 className="text-4xl font-extrabold text-purple mb-6 text-center">
          Welcome to the Student Chat Interface
        </h1>
        <p className="text-gray-800 text-xl mb-8 text-center">
          Here you can interact with our AI chatbot.
        </p>
        <ChatBot />
      </div>
    </div>
  );
}

export default App;
