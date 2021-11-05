'use strict';

const projectUrl = "http://127.0.0.1:8000/api/projects/";
let token = localStorage.getItem("token");

const loginBtn=document.querySelector('.login');
const logoutBtn = document.querySelector(".logout");
if(token){
    loginBtn.remove();
}
else{
    logoutBtn.remove();
}

logoutBtn.addEventListener('click',e=>{
    e.preventDefault()
    localStorage.removeItem('token');
    window.location = "http://127.0.0.1:5500/login.html";
})



const makeCard=(projects)=>{
    const card=document.querySelector('.card');
    card.innerHTML='';

    for(let project of projects){
        
        card.innerHTML += `
        <div class='inner-card'>

        <div class='img-container'><img src="http://127.0.0.1:8000${
          project.featured_image
        }" alt=""></div>
        <div class='card-text'>
        <div class='title'><h3>${project.title}</h3></div>
        <div class='vote-btn'><span class='vote-btn-span' data-vote='up' data-project=${project.id}>&#43;</span> <span class='vote-btn-span' data-vote='down' data-project=${project.id}>&#8722;</span></div>
        <div class='vote-ratio'>${project.vote_ratio}% Positive feedback</div>
        <div class='description'>${project.description.slice(0, 200)}</div>
        </div>
        
        </div>

        `;

    }

}


const getProjects=()=>{
    fetch(projectUrl)
    .then((res)=>{
        return res.json();
    })
    .then((data)=>{
        makeCard(data)
    })
    .catch((e)=>{
        console.log(e);
    })
}

getProjects()


document.addEventListener('click',function(e){
    if(e.target && e.target.classList.contains('vote-btn-span')){
        let vote=e.target.dataset.vote;
        let project=e.target.dataset.project
        
          fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`,{
              method:'POST',
              headers:{
                  'Content-Type':'application/json',
                  Authorization:`Bearer ${token}`
              },
              body:JSON.stringify({value:vote})
          })
          .then(res=>res.json())
          .then(data=>{
            
              getProjects()
          })
    }
})