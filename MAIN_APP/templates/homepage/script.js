var counter = 1;
setInterval(function(){
  document.getElementById('radio' + counter).checked = true;
  counter++;
  if(counter > 4){
    counter = 1;
  }
}, 5000);






const productContainers = [...document.querySelectorAll('.product-container')];
        const nxtBtn = [...document.querySelectorAll('.nxt-btn')];
        const preBtn = [...document.querySelectorAll('.pre-btn')];

        productContainers.forEach((item, i) => {
            let containerDimensions = item.getBoundingClientRect();
            let containerWidth = containerDimensions.width;

            nxtBtn[i].addEventListener('click', () => {
                item.scrollLeft += containerWidth;
            })

            preBtn[i].addEventListener('click', () => {
                item.scrollLeft -= containerWidth;
            })
        })

        let subMenu = document.getElementById("subMenu");
        let subTab = document.getElementById("subTab");
        let subFilter = document.getElementById("subFilter");
        
        function toggleMenu() {
            subMenu.classList.toggle("open-menu");
        }
    
        function toggleTab() {
            subTab.classList.toggle("open-tab");
        }
    
        function toggleFilter() {
            subFilter.classList.toggle("open-filter");
        }