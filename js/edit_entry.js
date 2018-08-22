"use strict"
const url = 'https://diarydeploy.herokuapp.com/api/v1/entries'

let token = localStorage.getItem("token")
let get_id = localStorage.getItem("id")
let get_title = localStorage.getItem("title")
let get_content = localStorage.getItem("content")
let get_date = localStorage.getItem("date")

document.getElementById("edit_entry"),addEventListener("submit" ,editEntry)
document.getElementById("editTitle").value  = get_title
document.getElementById("editDate").innerHTML  = get_date
document.getElementById("editContent").value  = get_content

function editEntry(){
    let title = document.getElementById("editTitle").value
    let content = document.getElementById("editContent").value 
   
    if (get_id){
        if(!token){
            window.location = "./index.html"

        }
        fetch(url+"/"+get_id, {
            method:"PUT",
            headers: {
                "content-type": "application/json",
                "Authorization": "Bearer "+token
            },
            body:JSON.stringify({
                title:title,
                content:content
              
            })
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
                if (data["message"]=="the update was successfully"){
                    alert("Your entry has been updated!")
                    window.location = "./view_content.html"
                }
                else{
                    document.getElementById('add_entry_error').innerHTML = data["message"]
                }
        }   
        })
    }
    else{
        window.location = "./404.html" 
                
    }
}


