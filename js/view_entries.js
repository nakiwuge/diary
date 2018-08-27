"use strict"
const url = 'https://diarydeploy.herokuapp.com/api/v1/entries'
let token = localStorage.getItem("token")
let options = {
    method: "GET",
    headers: {
        "content-type": "application/json",
        "Authorization": "Bearer "+token
    }}

function getEntry(n){
    
    localStorage.setItem("id", n)
}

function storeEntry(x,y,z){
    
    localStorage.setItem("title", x)
    localStorage.setItem("content", y)
    localStorage.setItem("date", z)
}
function userDetails(){
    
    fetch("https://diarydeploy.herokuapp.com/api/v1/user",options)
    .then((res) => res.json())
    .then((data) => {
        let user = data['user']
        if (user){
            document.getElementById("username-id").innerHTML =`
            <strong>Username: </strong>${user["username"]}`
            document.getElementById("email-id").innerHTML =`
            <strong>Username: </strong>${user["email"]}`
        }
        
    })  

}
function cannotEdit(){
    let get_id = localStorage.getItem("id")
    fetch(url+"/"+get_id+"/expired",options)
    .then((res) => res.json())
    .then((data) => {
        console.log(data)
        let msg = data["message"]
        if (msg == "Sorry you cannot modify this entry because it's past 24 hours"){
            alert(data["message"])
        }
        else{
            window.location = "./edit_content.html"
        }
    })
    
}

function viewEntries(){

    if (token){
        fetch(url, options)
        .then((res) => res.json())
        .then((data) => {
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
                let entries=data["entries"]
                if (entries){
                    document.getElementById("myEntries").innerHTML = "My Entries"
                    entries.forEach(entry => {
                        let id = entry.Entry_id
                        document.getElementById("view_id").innerHTML += ` 
                            <tr>  
                                <td ><a onClick="getEntry('${id}')" href="view_content.html">${entry.title}</a></td>
                                <td >${entry.date}</td>
                                <td>
                                    <form action="view_content.html">
                                        <button onClick="getEntry('${id}')" class ="button-small"type="submit" >view</button>
                                    </form>
                                </td>
                                <td>
                                    <form action="#">
                                        <button onClick="deleteEntry()" class="button-danger"  type="submit" >delete</button>
                                    </form>
                                </td>
                            </tr>
                    ` 
                    })
                }
                else{
                    document.getElementById('no_entry').innerHTML = `
                    You have no entries. Please click Add entry to add an entry.
                    `
                }
            }
        })
    }
    else{
        window.location = "./index.html"
    }
}

function viewContent(){
    
    let get_id = localStorage.getItem("id")
  
    if (get_id){
        if(!token){
            window.location = "./index.html"

        }
        fetch(url+"/"+get_id, options)
        .then((res) => res.json())
        .then((data) => {
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
                let entry=data["entry"][0]
                if (entry){
                    document.getElementById("content_id").innerHTML = `
                        <h2 >${entry.title} </h2>
                        <div>
                            <p >${entry.date}</p> 
                            <p>${entry.content}</p>  
                           
                            <button class="text" onClick="cannotEdit(); storeEntry('${entry.title}','${entry.content}','${entry.date}'); "style="padding: 5px 20px;"type="submit" >edit</button>
                           
                            <buttonclass="text" onClick="deleteEntry()"  class="button-danger" " type="submit" >delete</button>
                                
                        </div>  
                    `   
                }else{
                    window.location = "./404.html" 
                }
              
            }
        })
    }
    else{
        window.location = "./404.html" 
                
    }
}
function deleteEntry(){
    let get_id = localStorage.getItem("id")
    fetch(url+"/"+get_id, options = {
        method: "DELETE",
        headers: {
            "content-type": "application/json",
            "Authorization": "Bearer "+token
        }})
    .then((res) => res.json())
    .then((data) => {
        if (data){
            console.log(data)
            alert(data['message'])
            window.location = "./home.html"
            }
        else{
            console.log("not working") 
            }
        })
}

function viewProfile(){

    if (token){
        fetch(url, options)
        .then((res) => res.json())
        .then((data) => {
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
               
                let entries=data["entries"]
                if (entries){
                    document.getElementById("no_of_entries").innerHTML =`
                    <strong>Total Number of entries: </strong>${entries.length}` 
                }
                else{
                    document.getElementById('no_entry').innerHTML = `
                    You have no entries. Please click Add entry to add an entry.
                    `
                }
            }
        })
        .then(userDetails())
    }
    else{
        window.location = "./index.html"
    }


}
