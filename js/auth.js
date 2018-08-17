"use strict"
const signupurl = 'https://diarydeploy.herokuapp.com/api/v1/auth/signup'

//signup function
function signUp(e){
    e.preventDefault();

    let username = document.getElementById('username').value
    let email = document.getElementById('email').value
    let password = document.getElementById('password').value
    let confirm_password = document.getElementById('confirm_password').value

    fetch(signupurl, {
        method: 'POST',
        headers: {
            'Accept':'application/json, text/plain, */*',
            'Content-type':'application/json'
        },
        body:JSON.stringify({
            username:username,
            email:email,
            password:password,
            confirm_password:confirm_password
        })
    })
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
            if (data['message'] == "the registration was successful"){

               window.location = './index.html'  
            }
            else{
                document.getElementById('error').innerHTML = data['message']
          
            }
            
        })
        .catch((err) => console.log(err))
}

document.getElementById('signup').addEventListener('submit', signUp)
