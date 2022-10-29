function changeConfirmation(e) {
    // Get the snackbar DIV
    var x = document.getElementById("changeConfirmation");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

submit.click(function(e){
    e.preventDefault();
    changeConfirmation();
  });