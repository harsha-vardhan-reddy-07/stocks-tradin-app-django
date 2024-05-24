import React, { createContext, useState } from 'react';
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const GeneralContext = createContext();

const GeneralContextProvider = ({children}) => {

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [usertype, setUsertype] = useState('');



  const navigate = useNavigate();

  const login = async () =>{

    try{

      const loginInputs = { "email": email, "password":password}
        await axios.post('http://localhost:6001/login', loginInputs)
        .then( async (res)=>{

            console.log(res.data._id);
            
            localStorage.setItem('userId', res.data._id);
            localStorage.setItem('userType', res.data.usertype);
            localStorage.setItem('username', res.data.username);
            localStorage.setItem('email', res.data.email);
            localStorage.setItem('balance', res.data.balance);

            if(res.data.usertype === 'customer'){
                navigate('/home');
            } else if(res.data.usertype === 'admin'){
                navigate('/admin');
            }
        }).catch((err) =>{
            console.log(err);
            alert("Login failed");
        });

    }catch(err){
        console.log(err);
    }
  }

  
  const inputs = {"username":username, "email":email, "usertype": usertype, "password": password};

  const register = async () =>{

    try{
        await axios.post('http://localhost:6001/register', inputs,{
          // headers: {
          // //   'Content-Type': 'application/json',
          // // },
        })
        .then( async (res)=>{
            console.log(res.data._id);
            localStorage.setItem('userId', res.data._id);
            localStorage.setItem('userType', res.data.usertype);
            localStorage.setItem('username', res.data.username);
            localStorage.setItem('email', res.data.email);
            localStorage.setItem('balance', res.data.balance);

            if(res.data.usertype === 'customer'){
                navigate('/home');
            } else if(res.data.usertype === 'admin'){
                navigate('/admin');
            }

        }).catch((err) =>{
            console.log(err);
            alert("Registration failed");
        });

    }catch(err){
        console.log(err);
    }
  }



  const logout = async () =>{
    
    localStorage.clear();
    for (let key in localStorage) {
      if (localStorage.hasOwnProperty(key)) {
        localStorage.removeItem(key);
      }
    }
    
    navigate('/');
  }



  return (
    <GeneralContext.Provider value={{login, register, logout, username, setUsername, email, setEmail, password, setPassword, usertype, setUsertype}} >{children}</GeneralContext.Provider>
  )
}

export default GeneralContextProvider