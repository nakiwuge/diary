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
                        document.getElementById("view_id").innerHTML += `   
                            <tr>
                                <td ><a href="#">${entry.title}</a></td>
                                <td >${entry.date}</td>
                                <td>
                                    <form action="#">
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