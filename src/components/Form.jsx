import React from "react"
import Logo from "../assets/logoo.svg"
export default function Form(){
    return(
        <div className="flex flex-wrap justify-center">
            <form action="post">
            <img src={Logo} alt="HSU Logo"/>
                <input 
                    type="text" 
                    name="username" 
                    id="username" 
                    placeholder="Username"
                    className="w-full my-3 border border-black rounded-md" 
                    />
                <input type="text" name="password" id="password" placeholder="Password" className="w-full my-3 border border-black rounded-md" />
                <br />
                <section className="flex flex-wrap justify-evenly">
                <button type="submit">Submit</button>
                <a href="forgotPassword.html">Forgot Password?</a>
                </section>
            </form>
        </div>
    )
}