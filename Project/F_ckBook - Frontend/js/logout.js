$("#logout").click(() => {
 
    localStorage.setItem("token", "")
    location.href = "/login.html"

})