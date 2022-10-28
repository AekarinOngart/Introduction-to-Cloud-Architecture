$(document).ready(() => {

    console.log(localStorage.getItem('token'))
    var token = localStorage.getItem('token')
     
    const url = 'https://f-uck-backend-qy7vmzm5bq-as.a.run.app/post_list';    

    let request = new Request(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer '+token, 
        },
    });
    
    fetch(request)
        .then((response) => {
            return response.text();
        })
        .then((data) => {
            data = JSON.parse(data)

            data.posts.forEach(post => {
                console.log(data)
                var postCard = `<div class="row d-flex align-items-center justify-content-center mt-4">
                <div class="col-12 col-md-12 col-lg-8 col-xl-9">
                  <div class="card">
                    <div class="d-flex justify-content-between p-2 px-3">
                      <div class="d-flex flex-row align-items-center">
                        <div class="user-image">
                            <img id="displayImage" src="${post.owner_post.display_image}" title="User Image">
                        </div>
                        <div class="d-flex flex-column ml-2">
                          <span class="font-weight-bold">${post.owner_post.display_name}</span>
                        </div>
                      </div>
                    </div>
                    <img src="${post.image}" class="img-fluid" />
                    <div class="p-2">
                      <p class="text-justify">
                        ${post.message}
                      </p>
                      <hr />
                      <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex flex-row icons d-flex align-items-center">
                          <i class="fa fa-heart"></i>
                        </div>
                      </div>
                      <hr />
                    </div>
                  </div>
                </div>
              </div>` 
            $("#postContainer").append(postCard)
            });
        });
    
    const url_info = 'https://f-uck-backend-qy7vmzm5bq-as.a.run.app/user';    

    let request2 = new Request(url_info, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer '+token, 
        },
    });
        
    fetch(request2).then((response) => { return response.text() }).then((data) => {
        data = JSON.parse(data)
        console.log(data)
        $('#displayName').text(data.display_name)
        $("#displayImage").attr("src", data.display_image);
    })
});






      






    
