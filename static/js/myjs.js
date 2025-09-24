 document.addEventListener("DOMContentLoaded",function(){
        const navLinks=document.querySelectorAll(".nav-link");
        const currentPath=window.location.pathname; //取得目前的路徑名稱
        console.log(currentPath)
        console.log(navLinks)

        navLinks.forEach(function(link){
          const linkPath=link.getAttribute('href')
          console.log(linkPath)          
          if(linkPath === currentPath){
            //比對目前的路徑與所有的路徑,若有相同,則該路徑的超連結,套用active class
            link.classList.add('active');  
          }else{
            link.classList.remove("active");
          }
        })
      })