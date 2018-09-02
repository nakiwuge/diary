"use strict"
const url = 'https://diarydeploy.herokuapp.com/api/v1/entries/notify'
document.getElementById("reminder").addEventListener("submit" ,addReminder)

function addReminder(e){
    e.preventDefault()
    let title = document.getElementById("reminder_title").value 
    let start_date = document.getElementById("from").value
    let end_date = document.getElementById("to").value  
    let token = localStorage.getItem("token")
   
    if(!token){
        window.location = "./index.html"

    }
    fetch(url, {
        method:"POST",
        headers: {
            "content-type": "application/json",
            "Authorization": "Bearer "+token
        },
        body:JSON.stringify({

            title:title,
            start_date:start_date,
            end_date:end_date
            
        })
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data)
        

        if (data["msg"]=="Token has expired"){
            window.location = "./index.html"
        }
        else{
            
            if (data["message"]=="The reminder has been added"){
                alert("Your reminder has been added")
                window.location = "./home.html"
            }
            else{
                document.getElementById('reminder_error').innerHTML = data["message"]
            }
    }   
    })
}





