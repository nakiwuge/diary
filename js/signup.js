"use strict"
const signupurl = 'https://diarydeploy.herokuapp.com/api/v1/auth/signup'

document.getElementById('signup').addEventListener('submit', signUp)

//signup function
function signUp(e){
    e.preventDefault()

    let username = document.getElementById('signup_username').value
    let email = document.getElementById('signup_email').value
    let password = document.getElementById('signup_password').value
    let confirm_password = document.getElementById('signup_confirm_password').value

    fetch(signupurl, {
        method: 'POST',
        headers: {
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
                document.getElementById('signup_error').innerHTML = data['message']
          
            }
            
        })
        .catch((err) => console.log(err))
}



