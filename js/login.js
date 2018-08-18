"use strict"
const loginurl = "https://diarydeploy.herokuapp.com/api/v1/auth/login"

document.getElementById("login").addEventListener("submit", login)

//login function
function login(e){
    e.preventDefault()

    let email = document.getElementById("login_email").value
    let password = document.getElementById("login_password").value

    fetch(loginurl, {
        method: 'POST',
        headers: {
            'Content-type':'application/json'
        },
        body:JSON.stringify({
            email:email,
            password:password
        })
    })
        .then((res)=>res.json())
        .then((data)=>{
            console.log(data)
            if (data["message"]=="you have been logged in"){
                window.location = './home.html'
                localStorage.setItem('token', data['token']) 
            }
            else{
                document.getElementById('login_error').innerHTML = data['message']
            }
        })
}

