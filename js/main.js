"use strict"
function emptyLocalStorage(){ 

    localStorage.clear()
}
function checkToken(){
    let token = localStorage.getItem("token")
    if (!token){
        window.location = "./index.html"
    }
}