$('#loginForm').submit((event) => {
    event.preventDefault();

    var username = $("#username").val()
    var password = $("#password").val()

    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const url = 'https://f-uck-backend-qy7vmzm5bq-as.a.run.app/user';
    
    let request = new Request(url, {
        cache: 'default',
        method: 'POST',
        body: formData,
    });

    fetch(request)
        .then((response) => {
            if (response.status != 200) {
                throw new Error("Bad Server Response");
            }
            return response.text();
        })
        .then((data) => {
            data = JSON.parse(data)
            localStorage.setItem("token", data.access_token)
            console.log(data.access_token)
            location.href = 'post.html'
        });

})

$('#registerForm').submit((event) => {
    event.preventDefault();

    var display_name = $("#display_name").val()
    var username = $("#username").val()
    var password = $("#password").val()
    var input = document.querySelector('input[type="file"]')

    let formData = new FormData();
    formData.append('display_name', display_name);
    formData.append('username', username);
    formData.append('password', password);
    formData.append('display_image', input.files[0])


    const url = 'https://f-uck-backend-qy7vmzm5bq-as.a.run.app/register';
    
    let request = new Request(url, {
        cache: 'default',
        method: 'POST',
        body: formData,
    });

    fetch(request)
        .then((response) => {
            if (response.status != 201) {
                throw new Error("Bad Server Response");
            }
            return response.text();
        })
        .then((data) => {
            data = JSON.parse(data)
            console.log(data)
            if (confirm("Register Success please login !!")) {
                location.href = 'login.html'
            }
        });
})
