'use strict';

const loginForm=document.querySelector('form');

loginForm.addEventListener('submit',(e)=>{
    e.preventDefault()
    const username=loginForm.username.value;
    const password=loginForm.password.value;
    const formData={
        'username':username,
        'password':password
    }

    fetch("http://127.0.0.1:8000/api/users/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body:JSON.stringify(formData),
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.access){
            localStorage.setItem("token", data.access);
            window.location = "http://127.0.0.1:5500/index.html";
        }
        else{
            alert("username OR password did not match");
        }
    })
    .catch((err)=>{
        console.log(err);
    })


    loginForm.reset()
});
