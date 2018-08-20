"use strict"
const url = 'https://diarydeploy.herokuapp.com/api/v1/entries'

document.getElementById("add_entry").addEventListener("submit", addEntry)

function addEntry(e){
    e.preventDefault()

    let title = document.getElementById("add_title").value
    let content = document.getElementById("add_content").value
    let token = localStorage.getItem("token")

    if (token){

        fetch(url, {
            method:"POST",
            headers:{
                "content-type":"application/json",
                "Authorization":"Bearer "+token
            },
            body:JSON.stringify({
                title:title,
                content:content
            })

        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log(data)
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
                if (data["message"]=="entry has been added successfully"){
                    alert("The entry has been added")
                    window.location = "./home.html"
                }
                else{
                    document.getElementById('add_entry_error').innerHTML = data["message"]
                }
        }   
        })
    }
    else{
        window.location = "./index.html"
    }
}