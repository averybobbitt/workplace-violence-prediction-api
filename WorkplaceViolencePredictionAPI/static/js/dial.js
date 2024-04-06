const changeNum = () => {
    const randomNum = Math.round(Math.random() * 100);
    const degrees = Math.round((randomNum / 100) * 180);
    const root = document.querySelector(":root");
    let title = document.querySelector(".loader__title");
  
    let currentNumber = title.innerText;
    
    setInterval(() => {
       if (currentNumber < randomNum) {
        currentNumber++;
        title.innerText = currentNumber;
      } else if (currentNumber > randomNum) {
        currentNumber--;
        title.innerText = currentNumber;
      }
    }, 3);
  
    root.style.setProperty("--rotation", `${degrees}deg`);
  };
  
  
  setInterval(() => {
    changeNum();
  }, 2000);
  
  