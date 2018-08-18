"use strict"
const url = 'https://diarydeploy.herokuapp.com/api/v1/entries'

function viewEntries(){
    let token = localStorage.getItem("token")
  
    if (token){
        fetch(url,{
            method: "GET",
            headers: {
                "content-type": "application/json",
                "Authorization": "Bearer "+token
            }

        })
        .then((res) => res.json())
        .then((data) => {
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
                console.log(data)
                let entries=data["entries"]
                if (entries){
                    entries.forEach(entry => {
                        let get_id = localStorage.setItem("id",entry.entry_id)
                        document.getElementById("view_id").innerHTML += `   
                            <tr>
                                <td ><a onClick=${get_id} href="view_content.html">${entry.title}</a></td>
                                <td >${entry.date}</td>
                                <td>
                                    <form action="view_content.html">
                                        <button class ="button-small"type="submit" >view</button>
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
}

function viewContent(){
    let token = localStorage.getItem("token")
  
    if (token){
        fetch(url,{
            method: "GET",
            headers: {
                "content-type": "application/json",
                "Authorization": "Bearer "+token
            }

        })
        .then((res) => res.json())
        .then((data) => {
            if (data["msg"]=="Token has expired"){
                window.location = "./index.html"
            }
            else{
                console.log(data)
                let entries=data["entries"]
                if (entries){
                    
                    document.getElementById("view_title").innerHTML = entries
                        
                   
                   
                }
                else{
                    document.getElementById('no_entry').innerHTML = `
                    You have no entries. Please click Add entry to add an entry.
                    `
                }
            }
        })
    }
}
