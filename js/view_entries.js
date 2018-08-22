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
                                <td ><a onClick="getEntry('${id}')" href="view_content.html">${entry.title}</a></td>
                                <td >${entry.date}</td>
                                <td>
                                    <form action="view_content.html">
                                        <button onClick="getEntry('${id}')" class ="button-small"type="submit" >view</button>
                                    </form>
                                </td>
                                <td>
                                    <form action="#">
                                        <button class="button-danger"  type="submit" >delete</button>
                                    </form>
                                </td>
                            <tr>
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
                            <form class="text" action="edit_content.html">
                                <button onClick="storeEntry('${entry.title}','${entry.content}','${entry.date}')"style="padding: 5px 20px;"type="submit" >edit</button>
                            </form>
                            <form class="text"action="#">
                                <button  class="button-danger" " type="submit" >delete</button>
                            </form>    
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
                    console.log(entries)
                    console.log(entries.length)
                   
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
    }
    else{
        window.location = "./index.html"
    }


}